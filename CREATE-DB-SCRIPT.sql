-- Use our database

-- Create users table
CREATE TABLE IF NOT EXISTS Users
(
user_id int NOT NULL AUTO_INCREMENT,
user_name varchar(20) NOT NULL,
user_password varchar(20) NOT NULL,
PRIMARY KEY (user_id),
UNIQUE (user_name)
);

-- index the user id colomn to implement efficient search of users
--CREATE UNIQUE INDEX userId ON Users(user_id);

-- index the user name colomn to implement efficient search of users (used to find playlists)
--CREATE UNIQUE INDEX userName ON Users(user_name);


-- Create Artists table
CREATE TABLE Artists
(
artist_id int NOT NULL,
artist_name varchar(200) NOT NULL,
PRIMARY KEY (artist_id)
);

-- index the artist id colomn to implement efficient search of artists
CREATE UNIQUE INDEX artistId ON Artists(artist_id);

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

-- index the album id colomn to implement efficient search of albums
CREATE UNIQUE INDEX albumId ON Albums(album_id);

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

-- index the track id colomn to implement efficient search of tracks
CREATE UNIQUE INDEX trackId ON Tracks(track_id);

-- index the track name colomn to implement efficient search of tracks
CREATE INDEX trackName ON Tracks(track_name);

-- Create Lyrics table
CREATE TABLE Lyrics
(
track_id int NOT NULL,
lyrics TEXT NOT NULL,
PRIMARY KEY (track_id)
)ENGINE = MYISAM

;
