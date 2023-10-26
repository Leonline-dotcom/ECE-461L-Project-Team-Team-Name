from pymongo.mongo_client import MongoClient

connectionString = "mongodb+srv://david:SecretPassword1234@cluster0.3msmyxo.mongodb.net/?retryWrites=true&w=majority"

def connectToDB():
    client = MongoClient(connectionString)

    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    return client

def resetCluster():
    client = connectToDB()

    exclude_dbs = ['admin', 'local']
    
    for db_name in client.list_database_names():
        if db_name not in exclude_dbs:
            db = client[db_name]
            for collection_name in db.list_collection_names():
                db[collection_name].delete_many({})
    print("All collections in databases except 'admin' and 'local' have been emptied.")

def encrypt(inputText, N, D):
    if (D not in [-1, 1] or N < 1) or ("!" in inputText or " " in inputText):
        return "Invalid input"

    encryptedText = ""
    for char in reversed(inputText):
        if char == ' ' or char == '!':
            encryptedText += char
        else:
            shifted_char = chr(((ord(char) + 59 + (N * D)) % 93) + 34)
            encryptedText += shifted_char

    return encryptedText


def decrypt(encryptedText, N, D):
    if (D not in [-1, 1] or N < 1) or ("!" in encryptedText or " " in encryptedText):
        return "Invalid input"

    decryptedText = ""
    for char in reversed(encryptedText):
        if char == ' ' or char == '!':
            decryptedText += char
        else:
            shifted_char = chr(((ord(char) + 59 - (N * D)) % 93) + 34)
            decryptedText += shifted_char

    return decryptedText

def addNewUser(userid, password):
    client = connectToDB()

    db = client['Users']
    my_collection_name = "Users"
    my_collection = db[my_collection_name]
    encrypted_password = encrypt(password,3,1)
    my_collection.insert_one({"userid": userid, "password": encrypted_password})
    print(f"Added User {userid} with password {password} encrypted to {encrypted_password}")
    return

def initializeHWSets(size1,size2):

    client = connectToDB()

    initial_hwset1 = {
        "availability": size1,
        "capacity": size1
    }

    initial_hwset2 = {
        "availability": size2,
        "capacity": size2
    }

    client['Hardware']['HWSet1'].insert_one(initial_hwset1)
    client['Hardware']['HWSet2'].insert_one(initial_hwset2)

    print("Databases and collections have been initialized with the required documents.")
    return


def get_HWSet1_capacity():
    client = connectToDB()

    document = client['Hardware']['HWSet1'].find_one()
    if document:
        return document.get('capacity')
    else:
        print("No document found in HWSet1.")
        return None



def get_HWSet1_availability():
    client = connectToDB()
    
    document = client['Hardware']['HWSet1'].find_one()
    if document:
        return document.get('availability')
    else:
        print("No document found in HWSet1.")
        return None



def get_HWSet2_capacity():
    client = connectToDB()
    
    document = client['Hardware']['HWSet2'].find_one()
    if document:
        return document.get('capacity')
    else:
        print("No document found in HWSet2.")
        return None



def get_HWSet2_availability():
    client = connectToDB()
    
    document = client['Hardware']['HWSet2'].find_one()
    if document:
        return document.get('availability')
    else:
        print("No document found in HWSet2.")
        return None


def checkout_HWSet1(size):
    client = connectToDB()

    document = client['Hardware']['HWSet1'].find_one()
    if document:
        current_availability = document.get('availability')
        if size <= current_availability:
            client['Hardware']['HWSet1'].update_one({}, {"$inc": {"availability": -size}})
            return size
        else:
            client['Hardware']['HWSet1'].update_one({}, {"$set": {"availability": 0}})
            return current_availability
    else:
        print("No document found in HWSet1.")
        return None


def checkin_HWSet1(size):
    client = connectToDB()

    document = client['Hardware']['HWSet1'].find_one()
    if document:
        current_availability = document.get('availability')
        current_capacity = document.get('capacity')
        new_availability = current_availability + size
        if new_availability <= current_capacity:
            client['Hardware']['HWSet1'].update_one({}, {"$inc": {"availability": size}})
        else:
            client['Hardware']['HWSet1'].update_one({}, {"$set": {"availability": current_capacity}})


def checkout_HWSet2(size):
    client = connectToDB()

    document = client['Hardware']['HWSet2'].find_one()
    if document:
        current_availability = document.get('availability')
        if size <= current_availability:
            client['Hardware']['HWSet2'].update_one({}, {"$inc": {"availability": -size}})
            return size
        else:
            client['Hardware']['HWSet2'].update_one({}, {"$set": {"availability": 0}})
            return current_availability
    else:
        print("No document found in HWSet2.")
        return None


def checkin_HWSet2(size):
    client = connectToDB()

    document = client['Hardware']['HWSet2'].find_one()
    if document:
        current_availability = document.get('availability')
        current_capacity = document.get('capacity')
        new_availability = current_availability + size
        if new_availability <= current_capacity:
            client['Hardware']['HWSet2'].update_one({}, {"$inc": {"availability": size}})
        else:
            client['Hardware']['HWSet2'].update_one({}, {"$set": {"availability": current_capacity}})


def addProject(projectName):
    client = connectToDB()
    
    new_project = {
        "projectName": projectName,
        "Users": []
    }
    client['Projects']['Projects'].insert_one(new_project)
    print(f"Added Project {projectName}")

def addProjectUser(projectName, username):
    client = connectToDB()
    
    project_document = client['Projects']['Projects'].find_one({"projectName": projectName})
    if project_document:
        client['Projects']['Projects'].update_one({"projectName": projectName}, {"$push": {"Users": username}})
    else:
        print(f"Project {projectName} not found.")

def removeProjectUser(projectName, username):
    client = connectToDB()
    
    project_document = client['Projects']['Projects'].find_one({"projectName": projectName})
    if project_document:
        if username in project_document['Users']:
            # Removing the user from the project's Users array
            client['Projects']['Projects'].update_one({"projectName": projectName}, {"$pull": {"Users": username}})
            print(f"Removed {username} from {projectName}.")
        else:
            print(f"{username} is not in {projectName}.")
    else:
        print(f"Project {projectName} not found.")