from flask import Flask, render_template, request, jsonify,abort
# from flask_mysqldb import MySQL
import MySQLdb
import json

from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap

app = Flask(__name__)
#MYSQL CONFIG
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'hanif'
# app.config['MYSQL_PASSWORD'] = 'hanfix0013'
# app.config['MYSQL_DB'] = 'HG'
# mysql = MySQL(app)
#MQTT CONFIG
app.config['MQTT_BROKER_URL'] = 'localhost'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False
mqtt = Mqtt(app)
socketio = SocketIO(app)
bootstrap = Bootstrap(app)




#data = '{"id" : 3}'
#y = json.loads(data)
#x = y["id"]
#print x
coba = []
@app.route('/', methods=['POST', 'GET'])
def hello():
    if request.method == "POST":

        #Input data to database
        details = request.form
        dataid = details["fid"]
        jenis = details['fjenis']
        nama = details['fnama']
        asal = details['fasal']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO dataTanaman(id, jenis, nama, asal) VALUES (%s, %s, %s, %s)", (dataid, jenis, nama, asal))
        mysql.connection.commit()
        cur.close()
        print rv
    return render_template('index.html')
    

@app.route('/<int:index>', methods=['GET'])
def get_plants(index):
    #SQL to JSON
    cur = mysql.connection.cursor()

    #cari berdasar id
    sql = "SELECT * FROM dataTanaman WHERE id LIKE '%d'" %(index)
    print sql 
    cur.execute(sql)
    rv = cur.fetchall()
    payload = []
    content = {}
    for result in rv:
        content = {'id': result[0], 'jenis': result[1], 'nama': result[2], 'asal': result[3]}
        payload.append(content)
        content = {}
        print payload
        print type(content)
    return jsonify(payload)


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe("home/garden/publish")
    print ("Client " + str(client))
    print ("UserData " + str(userdata))
    print ("Flags " + str(flags))
    print ("RC " + str(rc))
    print "Konected"
    mqtt.publish('home/garden/subscribe', data )



@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    
    topic=message.topic,
    payload=message.payload.decode()
    print "================================="
    print "Topic " + str(topic[0])    
    print "Message " + str(payload)
    y = json.loads(str(payload))
    x = y["id"]
    print "Connecting database"
    query = "SELECT * FROM dataTanaman WHERE id = "+str(x)
    db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                            user="hanif",         # your username
                            passwd="hanfix0013",  # your password
                            db="HG")
    print "Curson"
    cursor = db.cursor()
    print "Execute"
    print query
    cursor.execute(query)
    
    print "fetchall"
    rv = cursor.fetchall()
    data = json.dumps(rv)
    print data
    payload = []
    content = {}
    for result in rv:
        content = {'id': result[0], 'jenis': result[1], 'nama': result[2], 'asal': result[3]}
        payload.append(content)
        content = {}
        print payload
        print type(content)
    cursor.close()
    db.close
    x = json.dumps(payload)
    print "mqtt publish"
    mqtt.publish('home/garden/subscribe', x)
        



    




if __name__ == '__main__':
    app.run(host='localhost', port=5001, debug=True)