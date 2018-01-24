# Software Documentation

## Creating the database (one time only, already done)
- In the root of this project, run `python CREATE-DB-SCRIPT.py`.
- This will take a couple hours since a very large database is built from 2 different external sites.

## Running the app
- cd into the source directory: `cd SRC/APPLICATION-SOURCE-CODE`
- Configure app_config/config.py according to the credentials of the MySQL server you are using (just configure "user" and "pass"). It is currently configured to run on NOVA.
- From the configuration you may also configure the webserver ip. DO NOT CHANGE the port from 4000 since the client uses it.
- If this is the first time running the app, create the users database: `python create_users_db.py`
- Run the server: `python app.py`
- Open your browser to http://localhost:4000/
- Now you may browse the app.

## Code Structure
The code has several parts