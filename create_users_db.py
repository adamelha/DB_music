import MySQLdb as mdb
from app_config.config import CONFIG
import musixmatch
from vohLyrics.voh import get_lyrics

'''
This file creates a simple mysql users database.
IMPORTANT: Make sure that app_config/config.py is configured according to your mysql server credentials!

The database created is called DbMysql23 and will look like so:
Table: Users:
    user_id     user_name    user_password
    1           admin        admin_pass
    2           user1        user1_pass
    1           user2        user2_pass
'''

def create_db():
    initial_user_names = ['admin', 'user1', 'user2']
    initial_user_passwords = ['admin_pass', 'user1_pass', 'user2_pass']

    con = mdb.connect(CONFIG['mysql']['host'], CONFIG['mysql']['user'], CONFIG['mysql']['pass'],
                    use_unicode = True, charset = 'utf8')

    # Create the database
    sql_cmd = 'CREATE DATABASE IF NOT EXISTS {}'.format(CONFIG['mysql']['database'])
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute(sql_cmd)
        cur.execute('USE {}'.format(CONFIG['mysql']['database']))

        # Drop the table if it already exists - start from clean
        cur.execute("DROP TABLE IF EXISTS Users")

        # Create Users table
        sql_cmd = '''CREATE TABLE IF NOT EXISTS Users
                    (
                    user_id int NOT NULL AUTO_INCREMENT,
                    user_name varchar(20) NOT NULL,
                    user_password varchar(20) NOT NULL,
                    PRIMARY KEY (user_id),
                    CHECK (user_id>0)
                    )
                    '''
        cur.execute(sql_cmd)

        # Populate the Users table
        for i in range(0, len(initial_user_names)):
            sql_cmd = '''
                    INSERT INTO Users (user_name, user_password)
                    SELECT * FROM (SELECT "{}" AS user_name, "{}" AS user_password) AS tmp
                    WHERE NOT EXISTS (SELECT user_name FROM Users WHERE user_name = "{}")
                    '''.format(initial_user_names[i], initial_user_passwords[i], initial_user_names[i])

            print (sql_cmd)
            cur.execute(sql_cmd)

        # Print the data
        cur.execute('SELECT * FROM Users LIMIT 10')
        rows = cur.fetchall()
        for row in rows:
            print ('user_id: {}, user_name: {}, user_password: {}'.format(row['user_id'], row['user_name'],
                                                                         row['user_password']))

    return

def create_artists_table():

    con = mdb.connect(CONFIG['mysql']['host'], CONFIG['mysql']['user'], CONFIG['mysql']['pass'],
                    use_unicode = True, charset = 'utf8')

    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute('USE {}'.format(CONFIG['mysql']['database']))

        # Drop the table if it already exists - start from clean
        cur.execute("DROP TABLE IF EXISTS Artists")

        # Create Artists table
        sql_cmd = '''CREATE TABLE IF NOT EXISTS Artists
                    (
                    artist_id int NOT NULL,
                    artist_name varchar(200) NOT NULL,
                    PRIMARY KEY (artist_id)
                    )
                    '''
        cur.execute(sql_cmd)

        # creating an object that can access the musixmatch API
        MusixMatch = musixmatch.Musixmatch()
        
        # add to the DB the 100 top Artists in the US, UK and IL
        for country in ['US', 'UK', 'IL', 'AU', 'AT' ,'BG', 'GR', 'IT', 'ES', 'SE']:
            jsonobj = MusixMatch.chart_artists(1, 50, country)
            for artist in jsonobj["message"]["body"]["artist_list"]:

                #insert this record to the DB if and only if it's not already there
                sql_cmd = '''
                        INSERT INTO Artists (artist_id, artist_name)
                        SELECT * FROM (SELECT "{}" AS artist_id, "{}" AS artist_name) AS tmp
                        WHERE NOT EXISTS (SELECT artist_id FROM Artists WHERE artist_id = "{}")
                        '''.format(artist["artist"]["artist_id"], artist["artist"]["artist_name"].replace('"', ''),
                                   artist["artist"]["artist_id"])
                try:
                    cur.execute(sql_cmd)
                except Exception as e:
                    print ("Artist insersion failed: {}".format(str(e)))
        return

def create_albums_table():

    con = mdb.connect(CONFIG['mysql']['host'], CONFIG['mysql']['user'], CONFIG['mysql']['pass'],
                    use_unicode = True, charset = 'utf8')
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute('USE {}'.format(CONFIG['mysql']['database']))

        # Drop the table if it already exists - start from clean
        cur.execute("DROP TABLE IF EXISTS Albums")

        # Create Albums table
        sql_cmd = '''CREATE TABLE IF NOT EXISTS Albums
                    (
                    album_id int NOT NULL,
                    album_name varchar(200) NOT NULL,
                    artist_id int NOT NULL,
                    track_count int NOT NULL,
                    PRIMARY KEY (album_id)
                    )
                    '''
        cur.execute(sql_cmd)

        # creating an object that can access the musixmatch API
        MusixMatch = musixmatch.Musixmatch()

        # add to the DB all the Albums of all the Artists in the DB
        cur.execute('SELECT artist_id FROM Artists')
        artistsList = cur.fetchall()
        for artist in artistsList:
            jsonobj = MusixMatch.artist_albums_get(artist["artist_id"], 1, 1, 50)
            for album in jsonobj["message"]["body"]["album_list"]:

                #insert this record to the DB if and only if it's not already there
                sql_cmd = '''
                        INSERT INTO Albums (album_id, album_name, artist_id, track_count)
                        SELECT * FROM (SELECT "{}" AS album_id, "{}" AS album_name, "{}" AS artist_id, "{}" AS track_count) AS tmp
                        WHERE NOT EXISTS (SELECT album_id FROM Albums WHERE album_id = "{}")
                        '''.format(album["album"]["album_id"], album["album"]["album_name"].replace('"', ''),
                                   album["album"]["artist_id"], album["album"]["album_track_count"],
                                   album["album"]["album_id"])
                try:
                    cur.execute(sql_cmd)
                except Exception as e:
                    print ("Album insersion failed: {}".format(str(e)))
        return

def create_tracks_table():

    con = mdb.connect(CONFIG['mysql']['host'], CONFIG['mysql']['user'], CONFIG['mysql']['pass'],
                    use_unicode = True, charset = 'utf8')
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute('USE {}'.format(CONFIG['mysql']['database']))

        # Drop the table if it already exists - start from clean
        cur.execute("DROP TABLE IF EXISTS Tracks")

        # Create Albums table
        sql_cmd = '''CREATE TABLE IF NOT EXISTS Tracks
                    (
                    track_id int NOT NULL,
                    track_name varchar(200) NOT NULL,
                    track_length int NOT NULL,
                    track_pos_in_album int NOT NULL,
                    album_id int NOT NULL,
                    artist_id int NOT NULL,
                    lyrics TEXT NOT NULL,
                    PRIMARY KEY (track_id)
                    )
                    '''
        cur.execute(sql_cmd)

        # creating an object that can access the musixmatch API
        MusixMatch = musixmatch.Musixmatch()

        # add to the DB all the tracks of all the albums in the DB
        cur.execute('''SELECT Artists.artist_id, artist_name, album_id, track_count
                       FROM Artists, Albums
                       WHERE Artists.artist_id = Albums.artist_id''')
        albumsList = cur.fetchall()
        for album in albumsList:
            jsonobj = MusixMatch.album_tracks_get(album["album_id"], 1, album["track_count"])
            track_pos_in_album = 0
            for track in jsonobj["message"]["body"]["track_list"]:

                # calculate the track position in the album
                track_pos_in_album += 1

                #call lyrics.voh to get the tracks lirics
                lyrics = get_lyrics(album['artist_name'] ,track["track"]["track_name"])

                #insert this record to the DB if and only if it's not already there
                sql_cmd = '''
                        INSERT INTO Tracks (track_id, track_name, track_length, track_pos_in_album, album_id, artist_id, lyrics)
                        SELECT * FROM (SELECT "{}" AS track_id, "{}" AS track_name, "{}" AS track_length,
                                              "{}" AS track_pos_in_album, "{}" AS album_id, "{}" AS artist_id, "{}" AS lyrics) AS tmp
                        WHERE NOT EXISTS (SELECT track_id FROM Tracks WHERE track_id = "{}")
                        '''.format(track["track"]["track_id"], track["track"]["track_name"].replace('"', ''),
                                   track["track"]["track_length"], track_pos_in_album,
                                   album["album_id"], album["artist_id"],
                                   lyrics.replace('"', ''), track["track"]["track_id"])
                try:
                    cur.execute(sql_cmd)
                except Exception as e:
                    print ("Track insersion failed: {}".format(str(e)))
        return

def create_playlists_table():

    con = mdb.connect(CONFIG['mysql']['host'], CONFIG['mysql']['user'], CONFIG['mysql']['pass'],
                    use_unicode = True, charset = 'utf8')
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute('USE {}'.format(CONFIG['mysql']['database']))

        # Drop the table if it already exists - start from clean
        cur.execute("DROP TABLE IF EXISTS Playlists")

        # Create Albums table
        sql_cmd = '''CREATE TABLE IF NOT EXISTS Playlists
                    (
                    user_id int NOT NULL,
                    playlist_name varchar(200) NOT NULL,
                    track_id int NOT NULL
                    )
                    '''
        cur.execute(sql_cmd)

        return

if __name__ == '__main__':
    create_db()
    create_artists_table()
    create_albums_table()
    create_tracks_table()
    create_playlists_table()
