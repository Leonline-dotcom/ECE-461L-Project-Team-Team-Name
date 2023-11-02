import os
from flask import Flask, request, jsonify
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


#checkout 
@app.route('/appPage/checkOut/<projectID>/<qty>/<HWSet>')
def checkOut_hardware(projectID, qty, HWSet):
    Client = MongoClient("mongodb+srv://teamteamname1:BVGIa4PacDjqmSK6@cluster0.cvqgis3.mongodb.net/?retryWrites=true&w=majority")
    db = Client["Users"]
    collection=db["Projects"]
    project = collection.find_one({"ProjectID": projectID})
    print(HWSet)
    HwQty=project.get(HWSet)
    print(HwQty)
    if(int(HwQty)+int(qty)<200):
        new_qty=int(HwQty)+int(qty)
        collection.update_one({"ProjectID": projectID}, {"$set": {HWSet: new_qty}})
        Client.close()
        return jsonify({'qty':new_qty,"code":200}),200
    else:
        collection.update_one({"ProjectID": projectID}, {"$set": {HWSet: 200}})
        Client.close()
        return jsonify({'qty':200,"code":200}),200



@app.route('/appPage/checkIn/<projectID>/<qty>/<HWSet>')
def checkIn_hardware(projectID, qty, HWSet):
    Client = MongoClient("mongodb+srv://teamteamname1:BVGIa4PacDjqmSK6@cluster0.cvqgis3.mongodb.net/?retryWrites=true&w=majority")
    db = Client["Users"]
    collection=db["Projects"]
    project = collection.find_one({"ProjectID": projectID})
    print(HWSet)
    HwQty=project.get(HWSet)
    print(HwQty)
    if(int(HwQty)-int(qty)>0):
        new_qty=int(HwQty)-int(qty)
        collection.update_one({"ProjectID": projectID}, {"$set": {HWSet: new_qty}})
        Client.close()
        return jsonify({'qty':new_qty,"code":200}),200
    else:
        collection.update_one({"ProjectID": projectID}, {"$set": {HWSet: 0}})
        Client.close()
        return jsonify({'qty':0,"code":200}),200



@app.route('/appPage/getHardware/<projectID>/<HWSet>')
def getHardware(projectID, HWSet):
    Client = MongoClient("mongodb+srv://teamteamname1:BVGIa4PacDjqmSK6@cluster0.cvqgis3.mongodb.net/?retryWrites=true&w=majority")
    db = Client["Users"]
    collection=db["Projects"]
    project = collection.find_one({"ProjectID": projectID})
    print(HWSet)
    HwQty=project.get(HWSet)
    Client.close()
    return jsonify({'qty':HwQty,"code":200}),200

@app.route('/appPage/addProject/<projectID>')
def add_project(projectID):
    print('hi')
    Client = client = MongoClient("mongodb+srv://teamteamname1:BVGIa4PacDjqmSK6@cluster0.cvqgis3.mongodb.net/?retryWrites=true&w=majority")
    db = Client["Users"]
    
    Projectcollection=db["Projects"]
    if(Projectcollection.find_one(projectID)):
       client.close()
       return jsonify({"message":"The Project Name"+projectID+"Is Not Available", "code":404 }),404
    else:
       
        
        CreateProject = { "ProjectID": projectID, "HWSet1": 0, "HWSet2":0 }
        Projectcollection.insert_one(CreateProject)
        client.close()
        return jsonify({"code":200 }),200

@app.route('/appPage/addProjectToUser/<projectID>/<Username>')
def addProjectToUser(projectID, Username):
    client = MongoClient("mongodb+srv://teamteamname1:BVGIa4PacDjqmSK6@cluster0.cvqgis3.mongodb.net/?retryWrites=true&w=majority")
    db = client["Users"]
    UserCollection = db["Users,Passwords,Projects"]

    User = UserCollection.find_one({"Username": Username})
    UserProjectList = User.get("Projects", [])  # Get the "Projects" field or an empty list
    UserProjectList.append(projectID)

    # Update the User document with the modified "Projects" list
    UserCollection.update_one({"Username": Username}, {"$set": {"Projects": UserProjectList}})
    client.close()
    return jsonify({"code":200 }),200



@app.route('/appPage/getprojects/<Username>')
def get_projects(Username):
    print('hi get project')
    client = MongoClient("mongodb+srv://teamteamname1:BVGIa4PacDjqmSK6@cluster0.cvqgis3.mongodb.net/?retryWrites=true&w=majority")
    db = client["Users"]
    UserCollection = db["Users,Passwords,Projects"]

    User = UserCollection.find_one({"Username": Username})
    UserProjectList = User.get("Projects", [])
    print(UserProjectList)
    client.close()
    return jsonify({"projectlist":UserProjectList,"code":200}),200


@app.route('/appPage/searchProject/<projectID>')
def add_exisitng_project_to_user(projectID):
    client = MongoClient("mongodb+srv://teamteamname1:BVGIa4PacDjqmSK6@cluster0.cvqgis3.mongodb.net/?retryWrites=true&w=majority")
    db = client["Users"]
    ProjectCollection = db["Projects"]

    if(ProjectCollection.find_one({"ProjectID": projectID})!=None):
        return jsonify({"code":200}),200
    else:
        return jsonify({"code":404}),404
@app.route('/appPage/leaveProject/<projectID>/<Username>')
def leave_project(projectID, Username):
    client = MongoClient("mongodb+srv://teamteamname1:BVGIa4PacDjqmSK6@cluster0.cvqgis3.mongodb.net/?retryWrites=true&w=majority")
    db = client["Users"]
    UserCollection = db["Users,Passwords,Projects"]
    update_query = {"$pull": {"Projects": projectID}}
    UserCollection.update_one({"Username": Username}, update_query)
    return jsonify({"code":200 }),200


@app.route('/')

@app.route('/signup')
@app.route('/login')
@app.route('/appPage')
@cross_origin()
def index():
    return app.send_static_file('index.html')
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)
