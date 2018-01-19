**Sign Up**
----
  Adds a user into the Users database.

* **URL**

  /signUp

* **Method:**

  `POST`
  
*  **URL Params**

   None

* **Data Params**

   **Content:** 
	```json
	{
		info : {
					username : <user name>
					password : <password>
				}
	}
	```

* **Success Response:**

  * **Code:** 200 OK <br />
 
* **Error Response:**

  * **Code:** 409 CONFLICT <br />
	**Content:** `{ error : "User already exists" }`

