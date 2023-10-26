import os
from flask import Flask, jsonify
from flask_cors import cross_origin,CORS
import logging
from pymongo import MongoClient
from cryptography.fernet import Fernet;
app=Flask(__name__,static_folder='./build',static_url_path='/')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'



#Encryption
def encrypt(input,Shift=5, Shifter=-1):
    if '!' in input or " " in input:
        return "Invalid"
    inputs=list(input)
    inputs.reverse()
    size = len(inputs)
    for i in range(0,size):
        if Shifter == 1:
             if inputs[i] == '~' and Shift!=0 :
                inputs[i]='"'
                newshift = Shift-1
                inputs[i]=chr(ord(inputs[i]) + newshift)
             else:    
                inputs[i]=chr(ord(inputs[i]) + Shift)
        if Shifter== -1:
            if inputs[i] == '"' and Shift!=0 :
                inputs[i]='~'
                newshift = Shift-1
                inputs[i]=chr(ord(inputs[i]) - newshift)
            else:
                inputs[i]=chr(ord(inputs[i]) - Shift)
    mystring="".join(inputs)
    return(mystring)

#Decryption
def decrypt(input,Shift=5, Shifter=-1):
    if '!' in input or " " in input:
        return "Invalid"
    inputs=list(input)
    size = len(inputs)
    for i in range(0,size):
        if Shifter == -1:
             if inputs[i] == '~' and Shift!=0 :
                inputs[i]='"'
                newshift = Shift-1
                inputs[i]=chr(ord(inputs[i]) + newshift)
             else:    
                inputs[i]=chr(ord(inputs[i]) + Shift)
        if Shifter== 1:
            if inputs[i] == '"' and Shift!=0 :
                inputs[i]='~'
                newshift = Shift-1
                inputs[i]=chr(ord(inputs[i]) - newshift)
            else:
                inputs[i]=chr(ord(inputs[i]) - Shift)
    inputs.reverse()
    mystring="".join(inputs)
    return(mystring)


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
        token=encrypt(Pass)
        if(token=='Invalid'):
            errorM = {"error": "Error: Invalid Password", "code": 404}
            client.close()
            return jsonify(errorM), 404
        projectlist=[]
        CreateUser = { "Username": User, "Password": token, "Projects":projectlist }
        collection.insert_one(CreateUser)
        client.close()
        successM= {'name': 'Success', 'code': 200}
        return jsonify(successM),200
    else:
        client.close()
        failM=errorM = {"error": "Error: Username Is Already In Use. Please Try Again", "code": 404}
        return jsonify(errorM), 404


@app.route('/login/<User>/<Pass>')
@cross_origin()
def login_check(User,Pass):
    Client= client =MongoClient("mongodb+srv://teamteamname1:BVGIa4PacDjqmSK6@cluster0.cvqgis3.mongodb.net/?retryWrites=true&w=majority")
    db = Client["Users"]
    collection=db["Users,Passwords,Projects"]
    if(collection.find_one({"Username": User})!=None):

        userlist=collection.find_one({"Username": User})
        token=(userlist['Password'])
        decrypttoken=decrypt(token)

       
        print(token)
        print(decrypttoken)
        if(decrypttoken==Pass):
            successM= {'name': 'Success', 'code': 200}
            return jsonify(successM),200
        else:
            client.close()
            failM=errorM = {"error": "Error: Invalid Username Or Password", "code": 404}
            return jsonify(errorM), 404
    else:
        failM=errorM = {"error": "Error: Invalid Username Or Password", "code": 404}
        return jsonify(errorM), 404
@app.route('/')

@app.route('/signup')
@app.route('/login')
@cross_origin()
def index():
    return app.send_static_file('index.html')
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)