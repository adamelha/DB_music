# The following API's are provided by this server:

- [Sign Up](#sign-up)
- [Log In](#log-in)
- [Get Songs Table (or playlist songs table)](#get-songs-table-or-playlist-songs-table-)
- [Get Artists Table](#get-artists-table)
- [Get Albums Table](#get-albums-table)
- [Remove Song from Playlist](#remove-song-from-playlist)
- [Search (Autocorrect) for Playlist](#search-autocorrect-for-playlist)
- [Add Song to New or Existing Playlist](#add-song-to-new-or-existing-playlist)
- [Get User Playlists](#get-user-playlists)
- [Remove Playlist](#remove-playlist)

## Sign Up
----
  Adds a user into the Users database.

* **URL**

  /signUp

* **Method:**

  `POST`

* **HTTP Headers**
	
	None
	
*  **URL Params**

   None

* **Data Params**

   ```javascript
   {
	'username' : '<username>',
	'password' : '<password>'
   }
   ```

* **Success Response:**

  * **Code:** 200 OK <br />
 
* **Error Response:**

  * **Code:** 409 CONFLICT <br />
  * **Content:** `{ error : "User already exists" }`

## Log In
----
  Validates user credentials. If ok, client should store them locally and send the headers in every request.

* **URL**

  /login

* **Method:**

  `OPTIONS`

* **HTTP Headers**
	
	None
	
*  **URL Params**

   None

* **Data Params**

   ```javascript
   {
	'username' : '<username>',
	'password' : '<password>'
   }
   ```

* **Success Response:**

  * **Code:** 200 OK <br />
 
* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
  *	**Content:** `{ error : "User and password do not match an existing user" }`
	
## Get Songs Table (or playlist songs table)
----
  Returns the table of all the songs depending on a filter and number of pages to display.
  * If 'playlist_name' is defined in the body - then display the songs from that playlist.
  * If 'playlist_name' is not defined in the body - then display from regular database
  
  NOTE: filters are in JSON in the Data Params  

* **URL**

  /songs

* **Method:**

  `POST`

* **HTTP Headers**
	
	None
	
*  **URL Params**
	
	None
   
* **Data Params**

   ```javascript
   {
    'username' : '<username>',
	'password' : '<password>',
	'entries_per_page' : <int: How many song entries you wish receive>,
	'page_index' : <int: the page number you wish to receive>
	'lyrics' : '<lyrics user wishes to search by>'
	'order' : '<"desc" or "asc" for descending or ascending order>',
	'field' : '<The field of which the data will be sorted>',
	'filters' : {
				'name' : '<song name>',
				'album' : '<album name>',
				'artist' : '<artist name>'
				'playlist_name' : '<name of a playlist belonging to the user>'
			  }
   }
   ```

* **Success Response:**

  * **Code:** 200 OK <br />
  * **Content:**
	```javascript
	{
		'list' : [
					{ 'song': '<song name>', 'track_id': <int track id in the DB>, 'artist': '<artist name>', 'album': '<album name>' },
					{ 'song': '<song name>', 'track_id': <int track id in the DB>, 'artist': '<artist name>', 'album': '<album name>' },
					{ 'song': '<song name>', 'track_id': <int track id in the DB>, 'artist': '<artist name>', 'album': '<album name>' },
					{ 'song': '<song name>', 'track_id': <int track id in the DB>, 'artist': '<artist name>', 'album': '<album name>' },
					...
				],
		'total_rows' : <int: The total number of entries passing the filter>
	}
	```
* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
	**Content:** `{ error : "User and password do not match an existing user" }`

## Get Artists Table
----
  Returns the table of all the artists depending on a filter and number of pages to display.
  Currently does not check user for debugging simplicity.
  NOTE: filters are in JSON in the Data Params  

* **URL**

  /artists

* **Method:**

  `POST`

* **HTTP Headers**
	
	None
	
*  **URL Params**
	
	None
   
* **Data Params**

   ```javascript
   {
    'username' : '<username>',
	'password' : '<password>',
	'entries_per_page' : <int: How many song entries you wish receive>,
	'page_index' : <int: the page number you wish to receive>,
	'order' : '<"desc" or "asc" for descending or ascending order>',
	'field' : '<The field of which the data will be sorted>',
	'filters' : {
				'name' : '<artist name>',
				'number_of_songs' : <int: will return all artists with more than number_of_albums albums>,
			  }
   }
   ```

* **Success Response:**

  * **Code:** 200 OK <br />
  * **Content:**
	```javascript
	{
		'list' : [
					{ 'name': '<artist name>', 'number_of_songs': <int: number of songs by this artist>},
					{ 'name': '<artist name>', 'number_of_songs': <int: number of songs by this artist>},
					{ 'name': '<artist name>', 'number_of_songs': <int: number of songs by this artist>},
					{ 'name': '<artist name>', 'number_of_songs': <int: number of songs by this artist>}
					...
				],
		'total_rows' : <int: The total number of entries passing the filter>
	}
	```
* **Error Response:**

  * **Code:** 500 INTERNAL ERROR <br />
  * **Content:** `{ error : "<An informative error string>" }`	
## Get Albums Table
----
  Returns the table of all the albums depending on a filter and number of pages to display.
  Currently does not check user for debugging simplicity.
  NOTE: filters are in JSON in the Data Params  

* **URL**

  /albums

* **Method:**

  `POST`

* **HTTP Headers**
	
	None
	
*  **URL Params**
	
	None
   
* **Data Params**

   ```javascript
   {
    'username' : '<username>',
	'password' : '<password>',
	'entries_per_page' : <int: How many song entries you wish receive>,
	'page_index' : <int: the page number you wish to receive>,
	'order' : '<"desc" or "asc" for descending or ascending order>',
	'field' : '<The field of which the data will be sorted>',
	'filters' : {
				'name' : '<album name>',
				'artist' : '<artist who released the album>',
				'number_of_songs' : <int: will return only the albums with at least this number of songs in it>
			  }
   }
   ```

* **Success Response:**

  * **Code:** 200 OK <br />
  * **Content:**
	```javascript
	{
		'list' : [
					{ 'name': '<album name>', 'artist': '<name of artist who released the album>', 'number_of_songs': <int: number of songs by this artist>},
					{ 'name': '<album name>', 'artist': '<name of artist who released the album>', 'number_of_songs': <int: number of songs by this artist>},
					{ 'name': '<album name>', 'artist': '<name of artist who released the album>', 'number_of_songs': <int: number of songs by this artist>},
					{ 'name': '<album name>', 'artist': '<name of artist who released the album>', 'number_of_songs': <int: number of songs by this artist>}
					...
				],
		'total_rows' : <int: The total number of entries passing the filter>
	}
	```
* **Error Response:**

  * **Code:** 500 INTERNAL ERROR <br />
  *	**Content:** `{ error : "<An informative error string>" }`
 
 
## Search (Autocorrect) for Playlist
----
  Returns an array of `{'playlist_id': <int: id>, 'playlist_name': '<playlist name>'}` where playlist_name is a sub string of an actual playlist of the user
  Used as autocorrect. when user wishes to add a song to one of his playlists, in the field of playlist that he chooses, each letter typed should trigger this API.

 * **URL**

  /searchPlaylist

* **Method:**

  `POST`

* **HTTP Headers**
	
	None
	
*  **URL Params**
	
	None
   
* **Data Params**

   ```javascript
   {
    'username' : '<username>',
	'password' : '<password>',
	'search' : '<substring of a playlist_name that belongs to username>'
   }
   ```

* **Success Response:**

  * **Code:** 200 OK <br />
  *  **Content:**
	```javascript
	{
		'list' : [
					{'name': '<playlist name that the search param in the response is a substring of>'},
					{'name': '<playlist name that the search param in the response is a substring of>'},
					{'name': '<playlist name that the search param in the response is a substring of>'},
					...
				],
	}
	```
* **Error Response:**

  * **Code:** 500 INTERNAL ERROR <br />
  *	**Content:** `{ error : "<An informative error string>" }`


## Add Song to New or Existing Playlist
----
  Adds a song to a user's playlist. This API is called after *Search (Autocorrect) for Playlist* API* when user decides on playlist.
  If the playlist does not exist, a new playlist with this song will be created.
  
 * **URL**

  /addToPlaylist

* **Method:**

  `POST`

* **HTTP Headers**
	
	None
	
*  **URL Params**
	
	None
   
* **Data Params**

   ```javascript
   {
    'username' : '<username>',
	'password' : '<password>',
	'playlist_name' : '<int: The name of the playlist chosen (existing or non existing>'
	'track_id' : <int: The id of the specific song the user chooses from the songs table (the /songs route)>
   }
   ```

* **Success Response:**

  * **Code:** 200 OK <br />
* **Error Response:**

  * **Code:** 500 INTERNAL ERROR <br />
  *	**Content:** `{ error : "<An informative error string>" }`


## Remove Song from Playlist
----
  Removes a song from an existing playlist.
  If all songs are removed, playlist will be deleted.

 * **URL**

  /removeSongFromPlaylist

* **Method:**

  `POST`

* **HTTP Headers**
	
	None
	
*  **URL Params**
	
	None
   
* **Data Params**

   ```javascript
   {
    'username' : '<username>',
	'password' : '<password>',
	'playlist_name' : '<name for the new playlist>',
	'track_id' : <int: The id of the specific song the user chooses from the songs table (the /songs route of a playlist display)>
   }
   ```

* **Success Response:**

  * **Code:** 200 OK <br />
  
* **Error Response:**

  * **Code:** 500 INTERNAL ERROR <br />
  *	**Content:** `{ error : "<An informative error string>" }`

  
## Remove Playlist
----
  Removes a users playlist including all the songs.

 * **URL**

  /removePlaylist

* **Method:**

  `POST`

* **HTTP Headers**
	
	None
	
*  **URL Params**
	
	None
   
* **Data Params**

   ```javascript
   {
    'username' : '<username>',
	'password' : '<password>',
	'playlist_name' : '<name of the playlist to be removed>'
   }
   ```

* **Success Response:**

  * **Code:** 200 OK <br />
  
* **Error Response:**

  * **Code:** 500 INTERNAL ERROR <br />
  *	**Content:** `{ error : "<An informative error string>" }`


## Get User Playlists
----
  This is called when the user wishes to display his playlists. The page will be a list of buttons representing each playlist.
  Returns a list of `{'name': '<playlist name>', 'number_of_songs' : <int: # songs in playlist>}` corresponding to the playlists that belong to the user.
  This way the playlists can be displayed in the same way as songs/artists/albums

 * **URL**

  /playlists

* **Method:**

  `POST`

* **HTTP Headers**
	
	None
	
*  **URL Params**
	
	None
   
* **Data Params**

   ```javascript
   {
    'username' : '<username>',
	'password' : '<password>',
	'entries_per_page' : <int: How many song entries you wish receive>,
	'page_index' : <int: the page number you wish to receive>,
	'order' : '<"desc" or "asc" for descending or ascending order>',
	'field' : '<The field of which the data will be sorted: "name" or "number_of_songs">'
   }
   ```

* **Success Response:**

  * **Code:** 200 OK <br />
  *  **Content:**
	```javascript
	{
		'list' : [
					{'name': '<playlist name corresponding to user>', 'number_of_songs' : <int: Number of songs in this playlist>},
					{'name': '<playlist name corresponding to user>', 'number_of_songs' : <int: Number of songs in this playlist>},
					{'name': '<playlist name corresponding to user>', 'number_of_songs' : <int: Number of songs in this playlist>},
					...
				]
		'total_rows' : <int: The total number of playlists for the user>
	}
	```
* **Error Response:**

  * **Code:** 500 INTERNAL ERROR <br />
  *	**Content:** `{ error : "<An informative error string>" }`

## Get Lyrics of Specific Song
----
  This is called when the user wishes to view the lyrics of a single song. Returns a JSON with the lyrics string (check out return code).

 * **URL**

  /singleLyrics

* **Method:**

  `POST`

* **HTTP Headers**
	
	None
	
*  **URL Params**
	
	None
   
* **Data Params**

   ```javascript
   {
    'username' : '<username>',
	'password' : '<password>',
	'filters' : {'track_id' : <int: track_id of the song from the songs page>}
   }
   ```

* **Success Response:**

  * **Code:** 200 OK <br />
  *  **Content:**
	```javascript
	{
		'lyrics' : '<The lyrics to the song with >'
	}
	```
* **Error Response:**

  * **Code:** 500 INTERNAL ERROR <br />
  *	**Content:** `{ error : "<An informative error string>" }`


