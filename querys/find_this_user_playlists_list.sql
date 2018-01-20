SELECT playlist_name, COUNT(*) AS track_count
FROM Playlists
WHERE user_id = {user_id}
GROUP BY user_id, playlist_name