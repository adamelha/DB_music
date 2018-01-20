**Sign Up**
----
  Adds a user into the Users database.

* **URL**

  /signUp

* **Method:**

  `POST`

* **HTTP Headers**
	
	* **username:** A new user name
	* **password:** Password of the new user
	
*  **URL Params**

   None

* **Data Params**

   None

* **Success Response:**

  * **Code:** 200 OK <br />
 
* **Error Response:**

  * **Code:** 409 CONFLICT <br />
	**Content:** `{ error : "User already exists" }`

**Log In**
----
  Validates user credentials. If ok, client should store them locally and send the headers in every request.

* **URL**

  /login

* **Method:**

  `OPTIONS`

* **HTTP Headers**
	
	* **username:** username
	* **password:** password
	
*  **URL Params**

   None

* **Data Params**

   None

* **Success Response:**

  * **Code:** 200 OK <br />
 
* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
	**Content:** `{ error : "User and password do not match an existing user" }`
	
**Get Songs Table**
----
  Returns the table of all the songs depending on a filter and number of pages to display.
  Currently does not check user for debugging simplicity.
  NOTE: in filters JSON in the Data Params  

* **URL**

  /songs

* **Method:**

  `POST`

* **HTTP Headers**
	
	* **username:** username
	* **password:** password
	
*  **URL Params**
	
	None
   
* **Data Params**

   ```javascript
   {
	'entries_per_page' : <int: How many song entries you wish receive>,
	'page_index' : <int: the page number you wish to receive>
	'filters' : {
				'name' : '<song name>',
				'album' : '<album name>',
				'artist' : '<artist name>',
				'lyrics' : '<CURRENTLY DOES NOTHING! a substring of the lyrics of a song. If it exists in a song, that song will be in the results>'
			  }
   }
   ```

* **Success Response:**

  * **Code:** 200 OK <br />
    **Content:**
	```javascript
	{
		'list' : [
					{ 'song': '<song name>', 'artist': '<artist name>', 'album': '<album name>', 'lyrics': <song lyrics id (actual lyrics in future> },
					{ 'song': '<song name>', 'artist': '<artist name>', 'album': '<album name>', 'lyrics': <song lyrics id (actual lyrics in future> },
					{ 'song': '<song name>', 'artist': '<artist name>', 'album': '<album name>', 'lyrics': <song lyrics id (actual lyrics in future> },
					{ 'song': '<song name>', 'artist': '<artist name>', 'album': '<album name>', 'lyrics': <song lyrics id (actual lyrics in future> },
					...
				]
	}
	```
* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
	**Content:** `{ error : "User and password do not match an existing user" }`