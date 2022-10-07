import mysql.connector

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='todo_db',
)
cur = db.cursor()


###############################################  INITIALIZATION  ######################################################


def alreadyExist():
    return ("Cela existe déjà ou est impossible !")


def alreadyDeleted():
    return ("Cela n'existe pas ou est impossible !")


def createTables():
    i=0
    if i<1:
        cur.execute("CREATE TABLE IF NOT EXISTS lists (id INT AUTO_INCREMENT PRIMARY KEY, asso VARCHAR(255), title VARCHAR(255), description VARCHAR(255))")
        cur.execute("CREATE TABLE IF NOT EXISTS tasks (id INT AUTO_INCREMENT PRIMARY KEY, listTitle VARCHAR(255), content VARCHAR(255))")
        i+=1


################################################  LIST FUNCTIONS  #####################################################


def fetchLists(userAsso):
    req = "SELECT title, asso FROM todo_db.lists WHERE (asso=%s)"
    cur.execute(req, userAsso)
    datas = cur.fetchall()
    return datas


def getList(getlistAsso, getlistTitle):
    req = "SELECT title, asso, description FROM todo_db.lists WHERE (title = '"+getlistTitle+"') AND (asso = '"+getlistAsso+"')"
    cur.execute(req)
    view = cur.fetchall()
    if view == []:
        return False
    else:
        return view[0]


def createList(addlistAsso, addlistTitle, addlistDesc):
    info = getList(addlistAsso, addlistTitle)
    if info is False:
        req = "INSERT INTO todo_db.lists (asso, title, description) VALUES (%s, %s, %s)"
        val = (addlistAsso, addlistTitle, addlistDesc)
        cur.execute(req, val)
    else:
        return alreadyExist()


# def editList(editlistAsso, editlistTitle, editlistDesc):
#     info = getList(editlistAsso, editlistTitle)
#     if info is False:
#         req = "UPDATE todo_db.lists SET (%s, %s, %s)(asso, title, description) VALUES "
#         val = (editlistAsso, editlistTitle, editlistDesc)
#         cursor.execute(req, val)
#     else:
#         return alreadyDeleted()

def delList(dellistAsso, dellistTitle):
    info = getList(dellistAsso, dellistTitle)
    if info is False:
        req = "DELETE FROM todo_db.lists WHERE (asso= %s, title= %s)"
        val = (dellistAsso, dellistTitle)
        cur.execute(req, val)
    else:
        return alreadyDeleted()


################################################  TASK FUNCTIONS  #####################################################
#functions are basically the same but not on with the same scope and variables.


def fetchTasks(userAsso, listTitle):
    req1 = "SELECT title FROM todo_db.lists WHERE (asso= %s) AND (title= %s)"
    val1 = (userAsso, listTitle)
    cur.execute(req1, val1)
    if cur.fetchone():
        req2 = "SELECT id, content FROM todo_db.tasks WHERE (listtitle= %s)"
        cur.execute(req2, [listTitle])
        data = cur.fetchall()
        return data[0]
    else:
        return alreadyDeleted()


def createTask(userAsso, listTitle, addcontent):
    req1 = "SELECT title FROM todo_db.lists WHERE (asso= %s) AND (title= %s)"
    val1 = (userAsso, listTitle)
    cur.execute(req1, val1)
    if cur.fetchone():
        req2 = "INSERT INTO todo_db.tasks (listTitle, content) VALUES (%s, %s)"
        val2 = (listTitle, addcontent)
        cur.execute(req2, val2)
    else:
        return "Vous devez d'abord créer une liste avec ce nom, pour cette asso !"


# def editTask(editlistAsso, editlistTitle, editlistDesc):
#     info = getList(editlistAsso, editlistTitle)
#     if info is False:
#         req = "UPDATE todo_db.tasks SET (alistTitle, content) VALUES (%s, %s, %s)"
#         val = (editlistAsso, editlistTitle, editlistDesc)
#         cursor.execute(req, val)
#     else:
#         return alreadyDeleted()

def delTask(listTitle, id):
    try:
        req = "DELETE FROM todo_db.tasks WHERE (listTitle= %s, id= %s)"
        val = (listTitle, id)
        cur.execute(req, val)
    except:
        return alreadyDeleted()


