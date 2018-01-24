import MySQLdb as mdb

'''
Exceptions.
'''
class UserNotExistException(Exception):
    pass
class UserExistsException(Exception):
    pass


'''
Get an sql command and return all the rows
'''
def execute_sql_command_fetch_all(con, cmd):
    print("Executing sql command:")
    print(cmd)
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute(cmd)
        return cur.fetchall()

'''
Get an sql command raise exception if failed
'''
def execute_sql_command_no_fetch(con, cmd):
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
def validate_user(con, request):
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
        rows = execute_sql_command_fetch_all(con, sql_cmd)

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
def validate_user_does_not_exist(con, request):
    try:
        userName = request.json['username']
        if userName is None:
            raise Exception()

        sql_cmd = '''
                    SELECT user_name
                    FROM Users
                    WHERE user_name='{}'
                    '''.format(userName)

        rows = execute_sql_command_fetch_all(con, sql_cmd)

        if len(rows) > 0:
            raise Exception()
    except Exception as e:
        print (str(e))
        raise UserExistsException("User already exists")


def signUp(con, userName, password):
    sql_cmd = '''
                INSERT INTO Users (user_name, user_password)
                VALUES ('{}','{}')
                '''.format(userName, password)

    with con:
        cur = con.cursor(mdb.cursors.DictCursor)

        print ('executing the following sql command:')
        print (sql_cmd)

        cur.execute(sql_cmd)

def getTrackList(con, json_data, user_id, track_name, artist_name, album_name, only_if_has_lyrics, order_field_mapping):

    # Check wheather displaying a playlist or not
    if 'filters' in json_data and 'playlist_name' in json_data['filters']:
        sql_cmd = '''
                        SELECT PlaylistTracks.track_id AS track_id, PlaylistTracks.track_name AS track_name, album_name, artist_name
                        FROM Artists, Albums, (SELECT Tracks.*
                                                FROM Playlists, Tracks
                                                WHERE user_id = {} and playlist_name = "{}" and Playlists.track_id = Tracks.track_id) AS PlaylistTracks
                        WHERE {}{}{}{}PlaylistTracks.artist_id = Artists.artist_id and PlaylistTracks.album_id = Albums.album_id
                        ORDER BY {} {}
                        '''.format(user_id, json_data['filters']['playlist_name'], track_name, artist_name, album_name,
                                   only_if_has_lyrics, order_field_mapping[json_data['field']], json_data['order'])
    else:
        sql_cmd = '''
                        SELECT track_id, track_name, album_name, artist_name
                        FROM Tracks, Artists, Albums
                        WHERE {}{}{}{}Tracks.artist_id = Artists.artist_id and Tracks.album_id = Albums.album_id
                        ORDER BY {} {}
                        '''.format(track_name, artist_name, album_name, only_if_has_lyrics,
                                   order_field_mapping[json_data['field']], json_data['order'])
    print('before filters')
    if 'filters' in json_data and 'lyrics' in json_data['filters']:
        sql_cmd = '''
                SELECT *
                FROM Lyrics, ( {} ) AS x
                WHERE lyrics.track_id = x.track_id AND MATCH(lyrics) AGAINST ('+{}*' in boolean mode)
                '''.format(sql_cmd, json_data['filters']['lyrics'].replace(' ', ' *'))

    tracks = execute_sql_command_fetch_all(con, sql_cmd)
    return tracks

def getAlbumsList(con, json_data, album_name, artist_name, track_count, order_field_mapping):
    sql_cmd = '''
                SELECT album_name, track_count, artist_name
                FROM Albums, Artists
                WHERE {}{}{}Albums.artist_id = Artists.artist_id
                ORDER BY {} {}
                '''.format(album_name, artist_name, track_count,
                           order_field_mapping[json_data['field']], json_data['order'])

    tracks = execute_sql_command_fetch_all(con, sql_cmd)
    return tracks

def getArtistsList(con, json_data, where, order_field_mapping):
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

    tracks = execute_sql_command_fetch_all(con, sql_cmd)
    return tracks

def addToPlaylist(con, json_data, user_id):
    sql_cmd = '''
                INSERT INTO Playlists
                values({}, "{}", {})
                '''.format(user_id, json_data['playlist_name'], json_data['track_id'])

    execute_sql_command_no_fetch(con, sql_cmd)

def removeFromPlaylist(con, json_data, user_id):
    sql_cmd = '''
                        DELETE FROM Playlists
                        WHERE user_id={} AND playlist_name="{}" AND track_id={}
                        '''.format(user_id, json_data['playlist_name'], json_data['track_id'])

    execute_sql_command_no_fetch(con, sql_cmd)

def removePlaylist(con, user_id, json_data):
    sql_cmd = '''
                DELETE FROM Playlists
                WHERE user_id={} AND playlist_name="{}"
                '''.format(user_id, json_data['playlist_name'])

    execute_sql_command_no_fetch(con, sql_cmd)

def getPlaylists(con, user_id, order_field_mapping, json_data):
    sql_cmd = '''
                        SELECT playlist_name, COUNT(*) AS track_count
                        FROM Playlists
                        WHERE user_id = {}
                        GROUP BY user_id, playlist_name
                        ORDER BY {} {}
                        '''.format(user_id, order_field_mapping[json_data['field']], json_data['order'])

    playlists = execute_sql_command_fetch_all(con, sql_cmd)

    return playlists

def searchPlaylists(con, json_data, user_id):
    sql_cmd = '''
                SELECT DISTINCT playlist_name FROM Playlists
                WHERE playlist_name LIKE "{}%" and user_id = {}
            '''.format(json_data['search'], user_id)

    playlists = execute_sql_command_fetch_all(con, sql_cmd)
    return playlists

def singleLyrics(con, json_data):
    sql_cmd = '''
                SELECT lyrics
                FROM Lyrics
                WHERE track_id = "{}"
            '''.format(json_data['filters']['track_id'])

    lyrics = execute_sql_command_fetch_all(con, sql_cmd)
    return lyrics