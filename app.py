from flask import Flask,render_template,jsonify,json,request
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
Exceptions. Move to separate file?
'''
class UserNotExistException(Exception):
    pass
class UserExistsException(Exception):
    pass



'''
Get an sql command and return all the rows
'''
def execute_sql_command_fetch_all(cmd):
    print("Executing sql command:")
    print(cmd)
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute(cmd)
        return cur.fetchall()

'''
Get an sql command raise exception if failed
'''
def execute_sql_command_no_fetch(cmd):
    print("Executing sql command:")
    print(cmd)
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute(cmd)


'''
Validate user based on credentials in the JSON in the body of the request
If the username and password do not match (or not exist) raise a UserNotExistException
Returns the user id
'''
def validate_user(request):
    try:
        userName = request.json['username']
        password = request.json['password']
        if userName is None or password is None:
            raise Exception()

        sql_cmd = '''
                    SELECT user_id, user_name, user_password
                    FROM Users
                    WHERE user_name='{}' AND user_password='{}'
                    '''.format(userName, password)

        rows = execute_sql_command_fetch_all(sql_cmd)

        if len(rows) != 1:
            raise Exception()

    except Exception as e:
        print (str(e))
        raise UserNotExistException("User and password do not match an existing user")

    return rows[0]['user_id']

'''
Assert that a username in a request does not exist in the Users DB.
If it does, raise a UserExistsException
'''
def validate_user_does_not_exist(request):
    try:
        userName = request.json['username']
        if userName is None:
            raise Exception()

        sql_cmd = '''
                    SELECT user_name
                    FROM Users
                    WHERE user_name='{}'
                    '''.format(userName)

        rows = execute_sql_command_fetch_all(sql_cmd)

        if len(rows) > 0:
            raise Exception()
    except Exception as e:
        print (str(e))
        raise UserExistsException("User already exists")

'''
Insert a user into the database only if the user does not exist.
Otherwise return user exists error
'''
@application.route("/signUp",methods=['POST'])
def signUp():
    print ('signup!!!!')
    try:
        validate_user_does_not_exist(request)
        userName = request.json['username']
        password = request.json['password']

        print ('Will now add the following user to the DB')
        print ('userName = {}, password = {}'.format(userName, password))

        sql_cmd = '''
                INSERT INTO Users (user_name, user_password)
                VALUES ('{}','{}')
                '''.format(userName, password)

        with con:
            cur = con.cursor(mdb.cursors.DictCursor)

            print ('executing the following sql command:')
            print (sql_cmd)

            cur.execute(sql_cmd)

            # Print the data for debug purposes
            cur.execute('SELECT * FROM Users LIMIT 30')
            rows = cur.fetchall()
            for row in rows:
                print ('user_id: {}, user_name: {}, user_password: {}'.format(row['user_id'], row['user_name'],
                                                                             row['user_password']))

    except Exception as e:
        if isinstance(e, UserExistsException):
            return Response(json.dumps({'error': "User already exists"}), status=409)
        else:
            return Response(json.dumps({'error': str(e)}), status=500)

    return Response(status=200)

'''
Log in to an account.
Retuns 200 if user-password combination exists.
'''
@application.route("/login",methods=['OPTIONS'])
def login():
    print ('login!!!')
    try:
        validate_user(request)

    except Exception as e:
        if isinstance(e, UserNotExistException):
            return Response(json.dumps({'error': str(e)}), status=401)
        else:
            return Response(json.dumps({'error': str(e)}), status=500)

    return Response(status=200)

@application.route("/songs",methods=['POST'])
def getTrackList():
    print ('songs!!!!')
    try:
        order_field_mapping = {'name' : 'track_name', 'album' : 'album_name', 'artist' : 'artist_name'}

        user_id = validate_user(request)

        print (request)
        json_data = request.get_json()
        print (json_data)

        entries_per_page = json_data['entries_per_page']
        page_index = json_data['page_index']

        if entries_per_page is None or not isinstance(entries_per_page, int)\
                or page_index is None or not isinstance(page_index, int):
            raise Exception("Bad entries_per_page or page_index")

        offset = page_index * entries_per_page

        # Make sure 'filters' is a key in the JSON
        if(not 'filters' in json_data):
            raise Exception("filters key not in json")

        filters = json_data['filters']
        #json_data = {'artist_name' : "", 'album_name' : "", 'only_if_has_lyrics' : 1}

        # artist name to filter by, if an empty string is recived no filtering by artist will be made
        if ('song' in filters):
            track_name = 'track_name = "{}" and '.format(filters['song'])
        else:
            track_name = ""

        # artist name to filter by, if an empty string is recived no filtering by artist will be made
        if ('artist' in filters):
            artist_name = 'artist_name = "{}" and '.format(filters['artist'])
        else:
            artist_name = ""

        # album name to filter by, if an empty string is recived no filtering by album will be made
        if ('album' in filters):
            print('yes')
            album_name = 'album_name = "{}" and '.format(filters['album'])
            print (album_name)
        else:
            print('no')
            album_name = ""

        # if set, query will only retrive tracks that has available lyrics
        if 'only_if_has_lyrics' in filters and filters['only_if_has_lyrics'] == 1:
            only_if_has_lyrics = 'lyrics_id <> 0 and '
        else:
            only_if_has_lyrics = ""

        print ('Get a tracks list filtered by artist name and/or album name')

        # Check wheather displaying a playlist or not
        if 'playlist_name' in json_data:

            sql_cmd = '''
                    SELECT PlaylistTracks.track_name AS track_name, album_name, artist_name, PlaylistTracks.lyrics_id as lyrics_id
                    FROM Artists, Albums, (SELECT Tracks.*
                                            FROM Playlists, Tracks
                                            WHERE user_id = {} and playlist_name = "{}" and Playlists.track_id = Tracks.track_id) AS PlaylistTracks
                    WHERE {}{}{}{}PlaylistTracks.artist_id = Artists.artist_id and PlaylistTracks.album_id = Albums.album_id
                    '''.format(user_id, json_data['playlist_name'], track_name, artist_name, album_name, only_if_has_lyrics)
        else:
            sql_cmd = '''
                    SELECT track_name, album_name, artist_name, lyrics_id
                    FROM Tracks, Artists, Albums
                    WHERE {}{}{}{}Tracks.artist_id = Artists.artist_id and Tracks.album_id = Albums.album_id
                    ORDER BY {} {}
                    '''.format(track_name, artist_name, album_name, only_if_has_lyrics, order_field_mapping[json_data['field']], json_data['order'])


        tracks = execute_sql_command_fetch_all(sql_cmd)
        #print (tracks)
        # Create dictionary for response JSON

        resp_dict = { 'list' : [], 'total_rows' : len(tracks)}
        print('offset is '.format(offset))
        for i in range(offset, offset + entries_per_page):
            if i >= len(tracks):
                break

            dict = {'song' : tracks[i]['track_name'],
                    'artist' : tracks[i]['artist_name'],
                    'album' : tracks[i]['album_name'],
                    'lyrics' : tracks[i]['lyrics_id']
                    }

            # Append entry to response
            resp_dict['list'].append(dict)

        print('Returning the following list')
        print(resp_dict)

    except Exception as e:
        return Response(json.dumps({'error': repr(e)}), status=401)

    return Response(json.dumps(resp_dict), status=200)


@application.route("/albums",methods=['POST'])
def getAlbumsList():
    print ('albums!!!!')
    try:
        order_field_mapping = {'name': 'album_name', 'artist': 'artist_name', 'number_of_songs': 'track_count'}
        print (request)
        json_data = request.get_json()
        print (json_data)

        entries_per_page = json_data['entries_per_page']
        page_index = json_data['page_index']

        if entries_per_page is None or not isinstance(entries_per_page, int) \
                or page_index is None or not isinstance(page_index, int):
            raise Exception("Bad entries_per_page or page_index")

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


        print ('Get a tracks list filtered by artist name and/or album name')

        sql_cmd = '''
                    SELECT album_name, track_count, artist_name
                    FROM Albums, Artists
                    WHERE {}{}{}Albums.artist_id = Artists.artist_id
                    ORDER BY {} {}
                    '''.format(album_name, artist_name, track_count,
                               order_field_mapping[json_data['field']], json_data['order'])

        tracks = execute_sql_command_fetch_all(sql_cmd)
        # print (tracks)
        # Create dictionary for response JSON

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

    except Exception as e:
        return Response(json.dumps({'error': repr(e)}), status=401)

    return Response(json.dumps(resp_dict), status=200)


@application.route("/artists",methods=['POST'])
def getArtistsList():
    print ('albums!!!!')
    try:
        order_field_mapping = {'name': 'artist_name', 'number_of_songs': 'artist_track_count'}
        print (request)
        json_data = request.get_json()
        print (json_data)

        entries_per_page = json_data['entries_per_page']
        page_index = json_data['page_index']

        if entries_per_page is None or not isinstance(entries_per_page, int) \
                or page_index is None or not isinstance(page_index, int):
            raise Exception("Bad entries_per_page or page_index")

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

        print ('Get a tracks list filtered by artist name and/or album name')

        sql_cmd = '''
                    SELECT artist_name, artist_track_count
                    FROM (
                        SELECT artist_name, count(artist_id) as artist_track_count
                        FROM (
                                SELECT Tracks.artist_id, artist_name, track_id
                                FROM Tracks, Artists
                                WHERE Tracks.artist_id = Artists.artist_id
                            ) AS x
                        GROUP BY artist_id
                        ) AS y
                    {}
                    ORDER BY {} {}
                    '''.format(where, order_field_mapping[json_data['field']], json_data['order'])

        tracks = execute_sql_command_fetch_all(sql_cmd)
        # print (tracks)
        # Create dictionary for response JSON

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

    return Response(json.dumps(resp_dict), status=200)


@application.route("/addToPlaylist",methods=['POST'])
def addToPlaylist():
    try:
        user_id = validate_user(request)
        print (user_id)
        print (request)
        json_data = request.get_json()
        print (json_data)

        if json_data['track_id'] is None or json_data['playlist_name'] is None:
            raise Exception('Missing parameters in body of request')

        sql_cmd = '''
                    INSERT INTO Playlists
                    values({}, "{}", {})
                    '''.format(user_id, json_data['playlist_name'], json_data['track_id'])

        execute_sql_command_no_fetch(sql_cmd)

    except Exception as e:
        return Response(json.dumps({'error': str(e)}), status=401)

    return Response(status=200)


@application.route("/removeFromPlaylist",methods=['POST'])
def removeFromPlaylist():
    try:
        user_id = validate_user(request)

        print (request)
        json_data = request.get_json()
        print (json_data)

        if json_data['track_id'] is None or json_data['playlist_name'] is None:
            raise Exception('Missing parameters in body of request')

        sql_cmd = '''
                    DELETE FROM Playlists
                    WHERE user_id={} AND playlist_name="{}" AND track_id={}
                    '''.format(user_id, json_data['playlist_name'], json_data['track_id'])

        execute_sql_command_no_fetch(sql_cmd)

    except Exception as e:
        return Response(json.dumps({'error': str(e)}), status=401)

    return Response(status=200)

@application.route("/removePlaylist",methods=['POST'])
def removePlaylist():
    try:
        user_id = validate_user(request)

        print (request)
        json_data = request.get_json()
        print (json_data)

        if json_data['playlist_name'] is None:
            raise Exception('Missing parameters in body of request')

        sql_cmd = '''
                    DELETE FROM Playlists
                    WHERE user_id={} AND playlist_name="{}"
                    '''.format(user_id, json_data['playlist_name'])

        execute_sql_command_no_fetch(sql_cmd)

    except Exception as e:
        return Response(json.dumps({'error': str(e)}), status=401)

    return Response(status=200)


@application.route("/playlists",methods=['POST'])
def getPlaylists():
    print ('playlists!!!!')
    try:
        order_field_mapping = {'name': 'playlist_name', 'number_of_songs': 'track_count'}
        user_id = validate_user(request)

        print (request)
        json_data = request.get_json()
        print (json_data)

        entries_per_page = json_data['entries_per_page']
        page_index = json_data['page_index']

        if entries_per_page is None or not isinstance(entries_per_page, int) \
                or page_index is None or not isinstance(page_index, int):
            raise Exception("Bad entries_per_page or page_index")

        offset = page_index * entries_per_page

        sql_cmd = '''
                    SELECT playlist_name, COUNT(*) AS track_count
                    FROM Playlists
                    WHERE user_id = {}
                    GROUP BY user_id, playlist_name
                    ORDER BY {} {}
                    '''.format(user_id, order_field_mapping[json_data['field']], json_data['order'])

        playlists = execute_sql_command_fetch_all(sql_cmd)

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
    con = mdb.connect(CONFIG['mysql']['host'], CONFIG['mysql']['user'], CONFIG['mysql']['pass'])
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute('USE {}'.format(CONFIG['mysql']['database']))

    application.run(host=CONFIG['webserver']['ip'], port=CONFIG['webserver']['port'])

