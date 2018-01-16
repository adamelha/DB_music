#from pymongo import MongoClient
#from bson.objectid import ObjectId
from flask import Flask,render_template,jsonify,json,request
#from fabric.api import *
import MySQLdb as mdb
from app_config.config import CONFIG

application = Flask(__name__)

'''
ADAM:
This file runs the flask server.
IMPORTANT: Make sure that app_config/config.py is configured according to your mysql server credentials!

Currenly I added the Sign up button that opens a form for a new user and adds him to the DB.
A bit buggy but works...

The default is port 5000 so to access the server open your browser to http://localhost:5000/
'''


#client = MongoClient('localhost:27017')
#db = client.MachineData

# ADAM: This was added by me
# If you press the signup button a pop up will pop, after filling the form and pressing Sign Up!
# then the user will be inserted into our mysql database. database name is proj_db, table is Users
@application.route("/signUp",methods=['POST'])
def signUp():
    print ('signup!!!!')
    try:
        json_data = request.json['info']
        userName = json_data['username']
        password = json_data['password']

        print ('Will now add the following user to the DB')
        print ('userName = {}, password = {}'.format(userName, password))

        sql_cmd = '''
                INSERT INTO Users (user_name, user_password)
                VALUES ('{}','{}')
                '''.format(userName, password)


        with con:
            cur = con.cursor(mdb.cursors.DictCursor)
            cur.execute('USE proj_db')

            print ('executing the following sql command:')
            print (sql_cmd)

            cur.execute(sql_cmd)

            # Print the data
            cur.execute('SELECT * FROM Users LIMIT 30')
            rows = cur.fetchall()
            for row in rows:
                print ('user_id: {}, user_name: {}, user_password: {}'.format(row['user_id'], row['user_name'],
                                                                             row['user_password']))

        return jsonify(status='OK', message='User inserted successfully')

    except Exception as e:
        return jsonify(status='ERROR',message=str(e))

# ADAM: This is the main route, it show list.htm
@application.route('/')
def showMachineList():
    return render_template('list.html')



# ADAM: The following (until __main__) are machine functions we should get rid of (or keep meanwhile as reference code)
@application.route("/addMachine", methods=['POST'])
def addMachine():
    try:
        json_data = request.json['info']
        deviceName = json_data['device']
        ipAddress = json_data['ip']
        userName = json_data['username']
        password = json_data['password']
        portNumber = json_data['port']

        print ('insert machine!!!')

        return jsonify(status='OK', message='inserted successfully')

    except Exception as e:
        return jsonify(status='ERROR', message=str(e))


@application.route('/getMachine', methods=['POST'])
def getMachine():
    try:
        print ('getMachine!!!')
        machineId = request.json['id']
        machineDetail = {
            'device': machine['device'],
            'ip': machine['ip'],
            'username': machine['username'],
            'password': machine['password'],
            'port': machine['port'],
            'id': str(machine['_id'])
        }
        return json.dumps(machineDetail)
    except Exception as e:
        return str(e)


@application.route('/updateMachine', methods=['POST'])
def updateMachine():
    try:
        print ("updateMachine!!!")
        machineInfo = request.json['info']
        machineId = machineInfo['id']
        device = machineInfo['device']
        ip = machineInfo['ip']
        username = machineInfo['username']
        password = machineInfo['password']
        port = machineInfo['port']

        return jsonify(status='OK', message='updated successfully')
    except Exception as e:
        return jsonify(status='ERROR', message=str(e))


@application.route("/getMachineList", methods=['POST'])
def getMachineList():
    try:

        print ('getMachineList!!!')

        machineList = []

    except Exception as e:
        return str(e)
    return json.dumps(machineList)


@application.route("/execute", methods=['POST'])
def execute():
    try:
        print ('execute!!!')

        machineInfo = request.json['info']
        ip = machineInfo['ip']
        username = machineInfo['username']
        password = machineInfo['password']
        command = machineInfo['command']
        isRoot = machineInfo['isRoot']

        env.host_string = username + '@' + ip
        env.password = password
        resp = ''
        with settings(warn_only=True):
            if isRoot:
                resp = sudo(command)
            else:
                resp = run(command)

        return jsonify(status='OK', message=resp)
    except Exception as e:
        print ('Error is ' + str(e))
        return jsonify(status='ERROR', message=str(e))


@application.route("/deleteMachine", methods=['POST'])
def deleteMachine():
    try:
        print ('deleteMachine!!!')

        machineId = request.json['id']

        return jsonify(status='OK', message='deletion successful')
    except Exception as e:
        return jsonify(status='ERROR', message=str(e))

# ADAM: The main, takes the config from the config file and connects to the mysql server
# Then runs the server
if __name__ == "__main__":
    con = mdb.connect('localhost', CONFIG['mysql']['user'], CONFIG['mysql']['pass'])
    application.run(host='0.0.0.0')

