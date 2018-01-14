# DB_Music
## Running the app
- Clone this repo: `git clone https://github.com/adamelha/DB_music.git`
- Configure app_config/config.py according to the credentials of the MySQL server you are using (just configure "user" and "pass")
- If this is the first time running the app, create the users database: `python create_users_db.py`
- Run the server: `python app.py`
- Open your browser to http://localhost:5000/
- Now you can browse the app and create new users with the "Sign up" button.
- NOTE: wsgi.py, app.ini, and all the code with "machines" is residue from the boilerplate and left currently as reference code only.
