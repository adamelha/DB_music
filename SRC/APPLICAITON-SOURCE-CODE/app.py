from flask import Flask,render_template,jsonify,json,request
from db_operations import db_operations as db
import MySQLdb as mdb
from app_config.config import CONFIG
from flask import Response
import os
from flask import send_from_directory

application = Flask(__name__)

'''
This file runs the flask server.
IMPORTANT: Make sure that app_config/config.py is configured according to your mysql server credentials!

The app will run on port 4000 browser to http://localhost:4000/
'''


'''
Insert a user into the database only if the user does not exist.
Otherwise return user exists error
'''
@application.route("/signUp",methods=['POST', 'OPTIONS'])
def signUp():
    print ('signup!!!!')
    try:
        db.validate_user_does_not_exist(con, request)
        userName = request.json['username']
        password = request.json['password']

        print ('Will now add the following user to the DB')
        print ('userName = {}, password = {}'.format(userName, password))

        db.signUp(con, userName, password)

    except Exception as e:
        if isinstance(e, db.UserExistsException):
            return Response(json.dumps({'error': "User already exists"}), status=409)
        else:
            return Response(json.dumps({'error': str(e)}), status=500)

    return Response(status=200 )

'''
Log in to an account.
Returns 200 if user-password combination exists.
'''
@application.route("/login",methods=['POST', 'OPTIONS'])
def login():
    print ('login!!!')
    try:
        db.validate_user(con, request)

    except Exception as e:
        if isinstance(e, db.UserNotExistException):
            return Response(json.dumps({'error': str(e)}), status=401)
        else:
            return Response(json.dumps({'error': str(e)}), status=500)

    return Response(status=200)

@application.route("/songs",methods=['POST'])
def getTrackList():
    print ('songs!!!!')
    try:
        order_field_mapping = {'name' : 'track_name', 'album' : 'album_name', 'artist' : 'artist_name'}

        user_id = db.validate_user(con, request)

        print (request)
        json_data = request.get_json()

        print (json_data)

        if not 'field' in json_data:
            json_data['field'] = 'album'
        if not 'order' in json_data:
            json_data['order'] = 'asc'

        entries_per_page = json_data['entries_per_page']
        page_index = json_data['page_index']

        if entries_per_page is None or not isinstance(entries_per_page, int)\
                or page_index is None or not isinstance(page_index, int):
            raise Exception("Bad entries_per_page or page_index")
        page_index -= 1
        offset = page_index * entries_per_page

        # Make sure 'filters' is a key in the JSON
        if(not 'filters' in json_data):
            raise Exception("filters key not in json")

        filters = json_data['filters']
        #json_data = {'artist_name' : "", 'album_name' : "", 'only_if_has_lyrics' : 1}

        # artist name to filter by, if an empty string is recived no filtering by artist will be made
        if ('name' in filters):
            track_name = 'track_name = "{}" and '.format(filters['name'])
        else:
            track_name = ""

        # artist name to filter by, if an empty string is recived no filtering by artist will be made
        if ('artist' in filters):
            artist_name = 'artist_name = "{}" and '.format(filters['artist'])
        else:
            artist_name = ""

        # album name to filter by, if an empty string is recived no filtering by album will be made
        if ('album' in filters):
            album_name = 'album_name = "{}" and '.format(filters['album'])
            print (album_name)
        else:
            album_name = ""

        # if set, query will only retrive tracks that has available lyrics
        if 'only_if_has_lyrics' in filters and filters['only_if_has_lyrics'] == 1:
            only_if_has_lyrics = 'lyrics_id <> 0 and '
        else:
            only_if_has_lyrics = ""

        tracks = db.getTrackList(con, json_data, user_id, track_name, artist_name, album_name, only_if_has_lyrics, order_field_mapping)

        resp_dict = { 'list' : [], 'total_rows' : len(tracks)}
        print('offset is '.format(offset))
        for i in range(offset, offset + entries_per_page):
            if i >= len(tracks):
                break

            dict = {'name' : tracks[i]['track_name'],
                    'track_id' : tracks[i]['track_id'],
                    'artist' : tracks[i]['artist_name'],
                    'album' : tracks[i]['album_name']
                    }

            # Append entry to response
            resp_dict['list'].append(dict)

        print('Returning the following list')
        print(resp_dict)

    except Exception as e:
        print repr(e)
        return Response(json.dumps({'error': repr(e)}), status=401)

    return Response(json.dumps(resp_dict, ensure_ascii=False), status=200)


@application.route("/albums",methods=['POST', 'OPTIONS'])
def getAlbumsList():
    print ('albums!!!!')

    try:
        order_field_mapping = {'name': 'album_name', 'artist': 'artist_name', 'number_of_songs': 'track_count'}
        print (request)
        json_data = request.get_json()
        print (json_data)

        if not 'field' in json_data:
            json_data['field'] = 'name'
        if not 'order' in json_data:
            json_data['order'] = 'asc'

        entries_per_page = json_data['entries_per_page']
        page_index = json_data['page_index']

        if entries_per_page is None or not isinstance(entries_per_page, int) \
                or page_index is None or not isinstance(page_index, int):
            raise Exception("Bad entries_per_page or page_index")

        page_index -= 1
        offset = page_index * entries_per_page

        # Make sure 'filters' is a key in the JSON
        if (not 'filters' in json_data):
            raise Exception("filters key not in json")

        filters = json_data['filters']
        # json_data = {'artist_name' : "", 'album_name' : "", 'only_if_has_lyrics' : 1}

        # album name to filter by, if an empty string is received no filtering by artist will be made
        if ('name' in filters):
            album_name = 'album_name = "{}" and '.format(filters['name'])
        else:
            album_name = ""

        # artist name to filter by, if an empty string is recived no filtering by artist will be made
        if ('artist' in filters):
            artist_name = 'artist_name = "{}" and '.format(filters['artist'])
        else:
            artist_name = ""

        # track count name to filter in all the albums with more than the given number of songs.
        # If not in filter no filtering by album will be made
        if ('number_of_songs' in filters):
            track_count = 'track_count > {} and '.format(filters['number_of_songs'])
        else:
            track_count = ""

        tracks = db.getAlbumsList(con, json_data, album_name, artist_name, track_count, order_field_mapping)

        resp_dict = {'list': [], 'total_rows': len(tracks)}
        for i in range(offset, offset + entries_per_page):
            if i >= len(tracks):
                break

            dict = {'name': tracks[i]['album_name'],
                    'artist': tracks[i]['artist_name'],
                    'number_of_songs': tracks[i]['track_count']
                    }
            # Append entry to response
            resp_dict['list'].append(dict)

        print('Returning the following list')
        print(resp_dict)
        print('yes')
    except Exception as e:
        return Response(json.dumps({'error': repr(e)}), status=401)
    print('before return')
    return Response(json.dumps(resp_dict, ensure_ascii=False), status=200)


@application.route("/artists",methods=['POST', 'OPTIONS'])
def getArtistsList():
    print ('artists!!!!')

    try:
        order_field_mapping = {'name': 'artist_name', 'number_of_songs': 'artist_track_count'}
        print (request)
        json_data = request.get_json()
        print (json_data)

        if not 'field' in json_data:
            json_data['field'] = 'name'
        if not 'order' in json_data:
            json_data['order'] = 'asc'

        entries_per_page = json_data['entries_per_page']
        page_index = json_data['page_index']

        if entries_per_page is None or not isinstance(entries_per_page, int) \
                or page_index is None or not isinstance(page_index, int):
            raise Exception("Bad entries_per_page or page_index")
        page_index -= 1
        offset = page_index * entries_per_page

        # Make sure 'filters' is a key in the JSON
        if (not 'filters' in json_data):
            raise Exception("filters key not in json")

        filters = json_data['filters']

        # artist_name to filter by, if an empty string is received no filtering by artist will be made
        if ('name' in filters):
            artist_name = 'artist_name = "{}" and '.format(filters['name'])
        else:
            artist_name = ""

        # track count name to filter in all the albums with more than the given number of songs.
        # If not in filter no filtering by album will be made
        if ('number_of_songs' in filters):
            artist_track_count = 'artist_track_count > {} and '.format(filters['number_of_songs'])
        else:
            artist_track_count = ""

        # If both are empty, no need for where clause
        if artist_name == "" and artist_track_count == "":
            where = ""
        else:
            where = "WHERE "
            if artist_name != "":
                where += artist_name
            if artist_track_count != "":
                where += "and " + artist_track_count
            # Remove extra 'and'
            where = where[:-4]

        tracks = db.getArtistsList(con, json_data, where, order_field_mapping)

        resp_dict = {'list': [], 'total_rows': len(tracks)}
        for i in range(offset, offset + entries_per_page):
            if i >= len(tracks):
                break

            dict = {'name': tracks[i]['artist_name'],
                    'number_of_songs': tracks[i]['artist_track_count']
                    }
            # Append entry to response
            resp_dict['list'].append(dict)

        print('Returning the following list')
        print(resp_dict)

    except Exception as e:
        return Response(json.dumps({'error': str(e)}), status=401)

    return Response(json.dumps(resp_dict, ensure_ascii=False), status=200)


@application.route("/addToPlaylist",methods=['POST', 'OPTIONS'])
def addToPlaylist():
    try:
        user_id = db.validate_user(con, request)
        print (user_id)
        print (request)
        json_data = request.get_json()
        print (json_data)

        if json_data['track_id'] is None or json_data['playlist_name'] is None:
            raise Exception('Missing parameters in body of request')

        db.addToPlaylist(con, json_data, user_id)

    except Exception as e:
        return Response(json.dumps({'error': str(e)}), status=401)

    return Response(status=200)


@application.route("/removeFromPlaylist",methods=['POST', 'OPTIONS'])
def removeFromPlaylist():
    try:
        user_id = db.validate_user(con, request)

        print (request)
        json_data = request.get_json()
        print (json_data)

        if json_data['track_id'] is None or json_data['playlist_name'] is None:
            raise Exception('Missing parameters in body of request')

        db.removeFromPlaylist(con, json_data, user_id)

    except Exception as e:
        return Response(json.dumps({'error': str(e)}), status=401)

    return Response(status=200)

@application.route("/removePlaylist",methods=['POST', 'OPTIONS'])
def removePlaylist():
    try:
        user_id = db.validate_user(con, request)

        print (request)
        json_data = request.get_json()
        print (json_data)

        if json_data['playlist_name'] is None:
            raise Exception('Missing parameters in body of request')

        db.removePlaylist(con, user_id, json_data)


    except Exception as e:
        return Response(json.dumps({'error': str(e)}), status=401)

    return Response(status=200)


@application.route("/playlists",methods=['POST', 'OPTIONS'])
def getPlaylists():
    print ('playlists!!!!')
    try:
        order_field_mapping = {'name': 'playlist_name', 'number_of_songs': 'track_count'}
        user_id = db.validate_user(con, request)

        print (request)
        json_data = request.get_json()
        print (json_data)

        entries_per_page = json_data['entries_per_page']
        page_index = json_data['page_index']

        if entries_per_page is None or not isinstance(entries_per_page, int) \
                or page_index is None or not isinstance(page_index, int):
            raise Exception("Bad entries_per_page or page_index")

        offset = page_index * entries_per_page

        playlists = db.getPlaylists(con, user_id, order_field_mapping, json_data)

        resp_dict = {'list': [], 'total_rows': len(playlists)}
        for i in range(offset, offset + entries_per_page):
            if i >= len(playlists):
                break

            dict = {'name': playlists[i]['playlist_name'],
                    'number_of_songs': playlists[i]['track_count']
                    }
            # Append entry to response
            resp_dict['list'].append(dict)

        print('Returning the following list')
        print(resp_dict)

    except Exception as e:
        return Response(json.dumps({'error': str(e)}), status=401)

    return Response(json.dumps(resp_dict), status=200)


# This is the main route
@application.route('/')
def show_index():
    return render_template('index.html')

@application.route('/<string:page_name>/')
def render_static_page(page_name):
    return render_template('%s.html' % page_name)

# Workaroud: redirect to the static directory since client code does not call /static/... but a relative path
@application.route('/app/<path:filename>')
def serve_static_app(filename):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(os.path.join(root_dir, 'static', 'app'), filename)
@application.route('/assets/<path:filename>')
def serve_static_assets(filename):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(os.path.join(root_dir, 'static', 'assets'), filename)
@application.route('/fonts/<path:filename>')
def serve_static_fonts(filename):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(os.path.join(root_dir, 'static', 'fonts'), filename)
@application.route('/maps/<path:filename>')
def serve_static_maps(filename):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(os.path.join(root_dir, 'static', 'maps'), filename)
@application.route('/scripts/<path:filename>')
def serve_static_(filename):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(os.path.join(root_dir, 'static', 'scripts'), filename)
@application.route('/styles/<path:filename>')
def serve_static_styles(filename):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(os.path.join(root_dir, 'static', 'styles'), filename)

# The main, takes the config from the config file and connects to the mysql server
# Then runs the server
if __name__ == "__main__":
    # Connect to mysql before even running the server
    con = mdb.connect(CONFIG['mysql']['host'], CONFIG['mysql']['user'], CONFIG['mysql']['pass'])
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute('USE {}'.format(CONFIG['mysql']['database']))

    application.run(host=CONFIG['webserver']['ip'], port=CONFIG['webserver']['port'])

