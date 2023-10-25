import os
from flask import Flask, jsonify
from flask_cors import cross_origin,CORS
import logging
from pymongo import MongoClient
from cryptography.fernet import Fernet;
app=Flask(__name__,static_folder='./build',static_url_path='/')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
#Sign Up Backend
@app.route('/signup/<User>/<Pass>')
@cross_origin()
def signup_check(User,Pass):
    print(User)
    print(Pass)

    Client= client =MongoClient("mongodb+srv://teamteamname1:BVGIa4PacDjqmSK6@cluster0.cvqgis3.mongodb.net/?retryWrites=true&w=majority")
    db = Client["Users"]
    collection=db["Users,Passwords,Projects"]
    
    if(collection.find_one({"Username": User})==None):
        key = Fernet.generate_key()
        f = Fernet(key)
        #arr turns string into byte
        arr = bytes(Pass, 'utf-8')
        #Fernet Encrypt seems like it only takes bytes
        token = f.encrypt(arr)
        projectlist=[]
        #Creates A User
        CreateUser = { "Username": User, "Password": token, "Projects":projectlist }
        collection.insert_one(CreateUser)
        client.close()
        successM= {'name': 'Success', 'code': 200}
        return jsonify(successM),200
    else:
        failM=errorM = {"error": "Error: Username Is Already In Use. Please Try Again", "code": 404}
        return jsonify(errorM), 404

@app.route('/')

@app.route('/signup')
@app.route('/login')
@cross_origin()
def index():
    return app.send_static_file('index.html')
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)