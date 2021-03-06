-- First, drop the tables if they exist
DROP TABLE IF EXISTS Playlists;
DROP TABLE IF EXISTS Lyrics;
DROP TABLE IF EXISTS Tracks;
DROP TABLE IF EXISTS Albums;
DROP TABLE IF EXISTS Artists;
DROP TABLE IF EXISTS Users;

-- Create users table
CREATE TABLE Users
(
user_id int NOT NULL AUTO_INCREMENT,
user_name varchar(20) NOT NULL,
user_password varchar(20) NOT NULL,
PRIMARY KEY (user_id)
);

-- Create Artists table
CREATE TABLE Artists
(
artist_id int NOT NULL,
artist_name varchar(200) NOT NULL,
PRIMARY KEY (artist_id)
);

-- index the artist name colomn to implement efficient search of artists
CREATE INDEX artistName ON Artists(artist_name);

-- Create Albums table
CREATE TABLE Albums
(
album_id int NOT NULL,
album_name varchar(200) NOT NULL,
artist_id int NOT NULL,
track_count int NOT NULL,
PRIMARY KEY (album_id),
FOREIGN KEY (artist_id) REFERENCES Artists(artist_id)
);

-- index the album name colomn to implement efficient search of artists
CREATE INDEX albumName ON Albums(album_name);


-- Create Tracks table
CREATE TABLE Tracks
(
track_id int NOT NULL,
track_name varchar(200) NOT NULL,
track_length int NOT NULL,
track_pos_in_album int NOT NULL,
album_id int NOT NULL,
artist_id int NOT NULL,
PRIMARY KEY (track_id),
FOREIGN KEY (artist_id) REFERENCES Artists(artist_id),
FOREIGN KEY (album_id) REFERENCES Albums(album_id)
);

-- index the track name colomn to implement efficient search of tracks
CREATE INDEX trackName ON Tracks(track_name);

CREATE TABLE Playlists
(
user_id int NOT NULL,
playlist_name varchar(200) NOT NULL,
track_id int NOT NULL
);

-- index the user_id colomn to implement efficient search of playlist list of a given user
CREATE INDEX userPlaylists ON Playlists(user_id);

-- index the (user_id, playlist_name) colomns to implement efficient search of playlists
CREATE INDEX Playlist ON Playlists(user_id, playlist_name);

-- Create Lyrics table
CREATE TABLE Lyrics
(
track_id int NOT NULL,
lyrics TEXT NOT NULL,
PRIMARY KEY (track_id)
)ENGINE = MYISAM
;

-- Create the index for the full text lyrics search
CREATE FULLTEXT INDEX fulltextindex ON Lyrics(lyrics);
