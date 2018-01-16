import MySQLdb as mdb
from app_config.config import CONFIG

'''
ADAM:
This file creates a simple mysql users database.
IMPORTANT: Make sure that app_config/config.py is configured according to your mysql server credentials!

The database created is called DbMysql23 and will look like so:
Table: Users:
    user_id     user_name    user_password
    1           admin        admin_pass
    2           user1        user1_pass
    1           user2        user2_pass
'''

def create_db():
    initial_user_names = ['admin', 'user1', 'user2']
    initial_user_passwords = ['admin_pass', 'user1_pass', 'user2_pass']

    con = mdb.connect(CONFIG['mysql']['host'], CONFIG['mysql']['user'], CONFIG['mysql']['pass'])

    # Create the database
    sql_cmd = 'CREATE DATABASE IF NOT EXISTS {}'.format(CONFIG['mysql']['database'])
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute(sql_cmd)
        cur.execute('USE {}'.format(CONFIG['mysql']['database']))

        # Drop the table if it already exists - start from clean
        cur.execute("DROP TABLE IF EXISTS Users")

        # Create Users table
        sql_cmd = '''CREATE TABLE IF NOT EXISTS Users
                    (
                    user_id int NOT NULL AUTO_INCREMENT,
                    user_name varchar(20) NOT NULL,
                    user_password varchar(20) NOT NULL,
                    PRIMARY KEY (user_id),
                    CHECK (user_id>0)
                    )
                    '''
        sql_cmd_foo = '''CREATE TABLE foo (
       bar VARCHAR(50) DEFAULT NULL
       ) ENGINE=MyISAM DEFAULT CHARSET=latin1
       '''
        cur.execute(sql_cmd)

        # Populate the Users table
        for i in range(0, len(initial_user_names)):
            sql_cmd = '''
                    INSERT INTO Users (user_name, user_password)
                    VALUES ('{}','{}')
                    '''.format(initial_user_names[i], initial_user_passwords[i])

            print (sql_cmd)
            cur.execute(sql_cmd)

        # Print the data
        cur.execute('SELECT * FROM Users LIMIT 10')
        rows = cur.fetchall()
        for row in rows:
            print ('user_id: {}, user_name: {}, user_password: {}'.format(row['user_id'], row['user_name'],
                                                                         row['user_password']))

    return


if __name__ == '__main__':
    create_db()