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
  Validates user credentials. If ok, client should store them locally and send the headers in every request

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