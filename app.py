#from pymongo import MongoClient
#from bson.objectid import ObjectId
from flask import Flask,render_template,jsonify,json,request
#from fabric.api import *
import MySQLdb as mdb
from app_config.config import CONFIG
from flask import Response
import os
from flask import send_from_directory

application = Flask(__name__)

'''
ADAM:
This file runs the flask server.
IMPORTANT: Make sure that app_config/config.py is configured according to your mysql server credentials!

The app will run on port 4000 browser to http://localhost:4000/
'''

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

class UserNotExistException(Exception):
    pass

'''
Validate user based on credentials in the HTTP request headers.
If the username and password do not match (or not exist) raise a UserNotExistException
'''
def validate_user(request):
    try:
        userName = request.headers['username']
        password = request.headers['password']
        sql_cmd = '''
                    SELECT user_name, user_password
                    FROM Users
                    WHERE user_name='{}' AND user_password='{}'
                    '''.format(userName, password)

        rows = execute_sql_command_fetch_all(sql_cmd)
        if len(rows) == 0:
            raise Exception()

    except Exception as e:
        print (str(e))
        raise UserNotExistException("User and password do not match an existing user")

# ADAM: This was added by me
# If you press the signup button a pop up will pop, after filling the form and pressing Sign Up!
# then the user will be inserted into our mysql database. database name is determined by CONFIG['mysql']['database'], table is Users
@application.route("/signUp",methods=['POST'])
def signUp():
    print ('signup!!!!')
    try:
        userName = request.headers['username']
        password = request.headers['password']

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

            # Print the data
            cur.execute('SELECT * FROM Users LIMIT 30')
            rows = cur.fetchall()
            for row in rows:
                print ('user_id: {}, user_name: {}, user_password: {}'.format(row['user_id'], row['user_name'],
                                                                             row['user_password']))

    except Exception as e:
        return Response(json.dumps({'error' : str(e)}), status=409)

    return Response(status=200)

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

def getTrackList():
    print ('getTracksByArtist!!!!')
    try:
        json_data = request.json['info']
        #json_data = {'artist_name' : "", 'album_name' : "", 'only_if_has_lyrics' : 1}
        
        # artist name to filter by, if an empty string is recived no filtering by artist will be made
        if (json_data['artist_name'] != ""):
            artist_name = 'artist_name = "{}" and '.format(json_data['artist_name'])
        else:
            artist_name = ""

        # album name to filter by, if an empty string is recived no filtering by album will be made
        if (json_data['album_name'] != ""):
            album_name = 'album_name = "{}" and '.format(json_data['album_name'])
        else:
            album_name = ""
            

        # if set, query will only retrive tracks that has available lyrics
        if(json_data['only_if_has_lyrics'] == 1):
            only_if_has_lyrics = 'lyrics_id <> 0 and '
        else:
            only_if_has_lyrics = ""

        print ('Get a tracks list filtered by artist name and/or album name')

        sql_cmd = '''
                SELECT track_name, album_name, artist_name, lyrics_id
                FROM Tracks, Artists, Albums
                WHERE {}{}{}Tracks.artist_id = Artists.artist_id and Tracks.album_id = Albums.album_id
                ORDER BY Tracks.artist_id, Tracks.album_id, track_pos_in_album
                '''.format(artist_name, album_name, only_if_has_lyrics)
        
        with con:
            cur = con.cursor(mdb.cursors.DictCursor)

            print ('executing the following sql command:')
            print (sql_cmd)

            cur.execute(sql_cmd)       
            tracks = cur.fetchall()

        return return_tracks_as_json

    except Exception as e:
        return jsonify(status='ERROR',message=str(e))

# ADAM: This is the main route
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

