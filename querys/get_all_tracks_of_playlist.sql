SELECT PlaylistTracks.track_name, album_name, artist_name, PlaylistTracks.lyrics_id
FROM Artists, Albums, (SELECT Tracks.*
					    FROM Playlists, Tracks
					    WHERE user_id = {user_id} and playlist_name = {playlist_name} and Playlists.track_id = Tracks.track_id) AS PlaylistTracks
WHERE PlaylistTracks.artist_id = Artists.artist_id and PlaylistTracks.album_id = Albums.album_id