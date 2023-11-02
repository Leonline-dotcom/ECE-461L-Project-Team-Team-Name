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
# @app.route('/appPage/checkOut_hardware<projectID>/<int:qty>', methods=['POST'])
# def checkOut_hardware(projectId, qty):
#     Client = MongoClient("mongodb+srv://teamteamname1:BVGIa4PacDjqmSK6@cluster0.cvqgis3.mongodb.net/?retryWrites=true&w=majority")
#     db = Client["Users"]
#     collection=db["Projects"]
#     project = collection.find_one({"_id": projectId})
    
#     if project is None:
#         return jsonify({"message": "Project not found"}), 404
#     available_qty = project.get("hardware_qty", 0)

#     if available_qty < qty:
#         return jsonify({"message": f"Not enough hardware avaliable for {project['name']}"})
    
#     new_qty = available_qty - qty 
#     collection.update_one({"_id": projectId}, {"$set": {"hardware_qty": new_qty}}) #only max of 200 change later

#     return jsonify({"message": f"{qty} hardware checked out from {project['name']}"})


# @app.route('/appPage/checkIn_hardware<projectID>/<int:qty>')
# def checkIn_hardware(projectId, qty):
#     Client = MongoClient("mongodb+srv://teamteamname1:BVGIa4PacDjqmSK6@cluster0.cvqgis3.mongodb.net/?retryWrites=true&w=majority")
#     db = Client["Users"]
#     collection=db["Projects"]
#     project = collection.find_one({"_id": projectId})

#     if project is None:
#         return jsonify({"message": "Project not found"}), 404

#     new_qty = project.get("hardware_qty", 0) + qty
#     collection.update_one({"_id": projectId}, {"$set": {"hardware_qty": new_qty}})

#     return jsonify({"message": f"{qty} hardware checked in to {project['name']}"})

# #add project

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

# #get user
# #add project
# #return all if successful
# #return project id does not exist

# @app.route('/appPage/returnExistingProject')
# def find_existing_project(projectId):
#     existing_project = collection.find_one({"projectId": projectId})
#     return existing_project

@app.route('/appPage/searchProject/<projectID>')
def add_exisitng_project_to_user(projectID):
    client = MongoClient("mongodb+srv://teamteamname1:BVGIa4PacDjqmSK6@cluster0.cvqgis3.mongodb.net/?retryWrites=true&w=majority")
    db = client["Users"]
    ProjectCollection = db["Projects"]

    if(ProjectCollection.find_one({"ProjectID": projectID})!=None):
        return jsonify({"code":200}),200
    else:
        return jsonify({"code":404}),404

#     if not name:
#         return jsonify({"message": "Project name is required"}), 400

#     existing_project = find_existing_project(name)

#     if existing_project:
#         user = collection.find_one({"_id": User}) #change to match database formatting
#         if "projectid" not in user: 
#             user["projects"] = []
#         user["projects"].append(existing_project)   #add project to user
#         collection.update_one({"_id": User}, {"$set": user}) #update collection
#         return jsonify({"message": "Project added to user's projects"})
#     else:
#         return jsonify({"message": "Project not found"}), 404

@app.route('/')

@app.route('/signup')
@app.route('/login')
@app.route('/appPage')
@cross_origin()
def index():
    return app.send_static_file('index.html')
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)
