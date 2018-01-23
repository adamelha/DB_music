import MySQLdb as mdb
from app_config.config import CONFIG
import musixmatch
from vohLyrics.voh import get_lyrics

def clear_db():
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)

        # clear the DB by removing all existing DB tables
        cur.execute("DROP TABLE IF EXISTS Playlists")
        cur.execute("DROP TABLE IF EXISTS Tracks")
        cur.execute("DROP TABLE IF EXISTS Albums")
        cur.execute("DROP TABLE IF EXISTS Artists")
        cur.execute("DROP TABLE IF EXISTS Users")

        return


def populate_users_table():
    initial_user_names = ['admin', 'user1', 'user2']
    initial_user_passwords = ['admin_pass', 'user1_pass', 'user2_pass']

    with con:
        cur = con.cursor(mdb.cursors.DictCursor)

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

def populate_artists_table():

    with con:
        cur = con.cursor(mdb.cursors.DictCursor)

        # creating an object that can access the musixmatch API
        MusixMatch = musixmatch.Musixmatch()
        
        # add to the DB the 100 top Artists in the US, UK and IL
        for country in ['US']:
            jsonobj = MusixMatch.chart_artists(1, 3, country)
            for artist in jsonobj["message"]["body"]["artist_list"]:
                print("Inserting artist")
                #insert this record to the DB if and only if it's not already there
                sql_cmd = u'''
                        INSERT INTO Artists (artist_id, artist_name)
                        SELECT * FROM (SELECT {} AS artist_id, "{}" AS artist_name) AS tmp
                        WHERE NOT EXISTS (SELECT artist_id FROM Artists WHERE artist_id = {})
                        '''.format(artist["artist"]["artist_id"], artist["artist"]["artist_name"].replace('"', ''),
                                   artist["artist"]["artist_id"])
                try:
                    cur.execute(sql_cmd)
                except Exception as e:
                    print ("Artist insersion failed: {}".format(str(e)))
        return

def populate_albums_table():

    with con:
        cur = con.cursor(mdb.cursors.DictCursor)

        # creating an object that can access the musixmatch API
        MusixMatch = musixmatch.Musixmatch()

        # add to the DB all the Albums of all the Artists in the DB
        cur.execute('SELECT artist_id FROM Artists')
        artistsList = cur.fetchall()
        for artist in artistsList:
            jsonobj = MusixMatch.artist_albums_get(artist["artist_id"], 1, 1, 3)
            for album in jsonobj["message"]["body"]["album_list"]:
                print("Inserting album")
                #insert this record to the DB if and only if it's not already there
                sql_cmd = u'''
                        INSERT INTO Albums (album_id, album_name, artist_id, track_count)
                        SELECT * FROM (SELECT "{}" AS album_id, "{}" AS album_name, "{}" AS artist_id, "{}" AS track_count) AS tmp
                        WHERE NOT EXISTS (SELECT album_id FROM Albums WHERE album_id = "{}")
                        '''.format(album["album"]["album_id"], album["album"]["album_name"].replace('"', ''),
                                   artist["artist_id"], album["album"]["album_track_count"], album["album"]["album_id"])
                try:
                    cur.execute(sql_cmd)
                except Exception as e:
                    print ("Album insersion failed: {}".format(str(e)))
        return

def populate_tracks_table():

    with con:
        cur = con.cursor(mdb.cursors.DictCursor)

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

                print("Inserting track")
                #insert this record to the DB if and only if it's not already there
                sql_cmd = u'''
                        INSERT INTO Tracks (track_id, track_name, track_length, track_pos_in_album, album_id, artist_id)
                        SELECT * FROM (SELECT "{}" AS track_id, "{}" AS track_name, "{}" AS track_length,
                                              "{}" AS track_pos_in_album, "{}" AS album_id, "{}" AS artist_id) AS tmp
                        WHERE NOT EXISTS (SELECT track_id FROM Tracks WHERE track_id = "{}")
                        '''.format(track["track"]["track_id"], track["track"]["track_name"].replace('"', ''),
                                   track["track"]["track_length"], track_pos_in_album, album["album_id"],
                                   album["artist_id"], track["track"]["track_id"])
                try:
                    cur.execute(sql_cmd)
                except Exception as e:
                    print ("Track insersion failed: {}".format(str(e)))
        return

def populate_lyrics_table():

    with con:
        cur = con.cursor(mdb.cursors.DictCursor)

        # add to the DB lyrics for all the tracks (if such exist in the api lyrics.voh
        cur.execute('''SELECT track_id, track_name, artist_name
                       FROM Artists, Tracks
                       WHERE Artists.artist_id = Tracks.artist_id''')
        tracksList = cur.fetchall()

        for track in tracksList:

                #call lyrics.voh to get the track lirics
                lyrics = get_lyrics(track['artist_name'] ,track["track_name"])

                #insert this record to the DB if and only if it's not already there
                sql_cmd = '''
                        INSERT INTO Lyrics (track_id, lyrics)
                        VALUES ("{}", "{}")'''.format(track['track_id'], lyrics.replace('"', ''))
                try:
                    cur.execute(sql_cmd)
                except Exception as e:
                    print ("Lyrics insersion failed: {}".format(str(e)))

        return

def populate_playlists_table():

    with con:
        cur = con.cursor(mdb.cursors.DictCursor)

        # Create Albums table
        sql_cmd = '''CREATE TABLE Playlists
                    (
                    user_id int NOT NULL,
                    playlist_name varchar(200) NOT NULL,
                    track_id int NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES Users(user_id)
                    )
                    '''
        cur.execute(sql_cmd)

        # index the (user_id, playlist_name) colomns to implement efficient search of playlists
        cur.execute("CREATE INDEX Playlist ON Playlists(user_id, playlist_name)")


if __name__ == '__main__':
    con = mdb.connect(CONFIG['mysql']['host'], CONFIG['mysql']['user'], CONFIG['mysql']['pass'],
                      use_unicode=True, charset='utf8')
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute('USE {}'.format(CONFIG['mysql']['database']))

    #clear_db()
    populate_users_table()
    populate_artists_table()
    populate_albums_table()
    populate_tracks_table()
    populate_lyrics_table()
    populate_playlists_table()
