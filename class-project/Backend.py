import os
from flask import Flask, request, jsonify
from flask_cors import cross_origin,CORS
import logging
from pymongo import MongoClient
from cryptography.fernet import Fernet;
app=Flask(__name__,static_folder='./build',static_url_path='/')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

#define database
Client = MongoClient("mongodb+srv://teamteamname1:BVGIa4PacDjqmSK6@cluster0.cvqgis3.mongodb.net/?retryWrites=true&w=majority")
db = Client["Users"]
collection=db["Users,Passwords,Projects"]

Client= client =MongoClient("mongodb+srv://teamteamname1:BVGIa4PacDjqmSK6@cluster0.cvqgis3.mongodb.net/?retryWrites=true&w=majority")
db = Client["Users"]
collection=db["Users,Passwords,Projects"]


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
            print('error')
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
        errorM = {"error": "Error: Username Is Already In Use. Please Try Again", "code": 404}
        return jsonify(errorM), 404


@app.route('/login/<User>/<Pass>')
@cross_origin()
def login_check(User,Pass):
    Client = client = MongoClient("mongodb+srv://teamteamname1:BVGIa4PacDjqmSK6@cluster0.cvqgis3.mongodb.net/?retryWrites=true&w=majority")
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

#checkout 
@app.route('/appPage/checkOut_hardware<projectID>/<int:qty>', methods=['POST'])
def checkOut_hardware(projectId, qty):
    Client = MongoClient("mongodb+srv://teamteamname1:BVGIa4PacDjqmSK6@cluster0.cvqgis3.mongodb.net/?retryWrites=true&w=majority")
    db = Client["Users"]
    collection=db["Projects"]
    project = collection.find_one({"_id": projectId})
    
    if project is None:
        return jsonify({"message": "Project not found"}), 404
    available_qty = project.get("hardware_qty", 0)

    if available_qty < qty:
        return jsonify({"message": f"Not enough hardware avaliable for {project['name']}"})
    
    new_qty = available_qty - qty 
    collection.update_one({"_id": projectId}, {"$set": {"hardware_qty": new_qty}}) #only max of 200 change later

    return jsonify({"message": f"{qty} hardware checked out from {project['name']}"})


@app.route('/appPage/checkIn_hardware<projectID>/<int:qty>')
def checkIn_hardware(projectId, qty):
    Client = MongoClient("mongodb+srv://teamteamname1:BVGIa4PacDjqmSK6@cluster0.cvqgis3.mongodb.net/?retryWrites=true&w=majority")
    db = Client["Users"]
    collection=db["Projects"]
    project = collection.find_one({"_id": projectId})

    if project is None:
        return jsonify({"message": "Project not found"}), 404

    new_qty = project.get("hardware_qty", 0) + qty
    collection.update_one({"_id": projectId}, {"$set": {"hardware_qty": new_qty}})

    return jsonify({"message": f"{qty} hardware checked in to {project['name']}"})

#add project

@app.route('/add_projects', methods=['POST'])
def add_project():
    data = request.get_json() # change this based on how font end passes name
    name = data.get("name")

    if not name:
        return jsonify({"message": "Project name is a required field"}), 400
    
    new_project = {
        "name": name,
        "hardware_qty": 0 
    }

    result = collection.insert_one(new_project)
    #change maybe? not sure if you need to pass in a project id or the name is the id
    return jsonify({"message": "Project added sucessfully", "inserted_id": str(result.inserted_id)})


@app.route('/appPage', methods=['GET'])
def get_projects():
    projects = list(collection.find({}, {"_id": 0}))
    return jsonify({"project": projects})

#get user
#add project
#return all if successful
#return project id does not exist

@app.route('/appPage/returnExistingProject')
def find_existing_project(projectId):
    existing_project = collection.find_one({"projectId": projectId})
    return existing_project

@app.route('/appPage/search_Project')
def add_exisitng_project_to_user():
    data = request.get_json()
    User = data.get("User")
    name = data.get("projectId")# could be replaced with /appPage/. . ./<projectId>?

    if not name:
        return jsonify({"message": "Project name is required"}), 400

    existing_project = find_existing_project(name)

    if existing_project:
        user = collection.find_one({"_id": User}) #change to match database formatting
        if "projectid" not in user: 
            user["projects"] = []
        user["projects"].append(existing_project)   #add project to user
        collection.update_one({"_id": User}, {"$set": user}) #update collection
        return jsonify({"message": "Project added to user's projects"})
    else:
        return jsonify({"message": "Project not found"}), 404
