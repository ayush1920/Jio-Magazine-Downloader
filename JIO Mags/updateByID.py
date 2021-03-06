# update or make database as per issue ID
import requests as handler
import os
import json
import sys
import sqlite3
from shutil import copyfile
def downloadData(magID):
    url = geturl(magID)
    headers = getheaders()
    data  = handler.get(url, headers = headers)
    data = json.loads(data.text)
    data = data['result']['items']
    return data

def geturl(magID):
    host = "http://jionewsapi.media.jio.com"
    magUrl  = "/magazines/apis/v1.1/issues?magId="+magID+"&limit=100&offset=0&imageSize=3"
    return host + magUrl

def getheaders():

    # replace accesstoken by user's token [Delete before uploading]
    # access token loacaion root/data/data/com.jioxpressnews/shared_pref/jionews_preference.xml -> string name access_token
    # format JN:ms:user: < Unique code>
    f = open("access_token.txt","r")
    accesstoken = f.read()
    f.close()
    headers = {"Content-Type" : "application/json",
    "accesstoken" : accesstoken,
    "devicetype" : "phone",
    "os" : "android",
    "version": "3.1.1",
    "Host" : "jionewsapi.media.jio.com",
    "Connection" : "Keep-Alive",
    "Accept-Encoding" : "gzip",
    "User-Agent" : "okhttp/3.14.1"}
    return headers

def createDatabase(databasename,tablename, param):
    connection = sqlite3.connect(databasename)
    crsr = connection.cursor()
    sql_command = "CREATE TABLE IF NOT EXISTS "+tablename+"("
    for _ in param.keys():
        sql_command = sql_command+ _ +" "+param[_]+",\n"
    sql_command = sql_command[:-2:1]+")"
    crsr.execute(sql_command) 
    connection.commit()
    connection.close()
    
def droptable(tablename):
    connection = sqlite3.connect(databasename)
    crsr = connection.cursor()
    sql_command = "DROP TABLE IF EXISTS "+tablename+";"
    crsr.execute(sql_command) 
    connection.commit()
    connection.close()
    
def addJSONData(databasename,tablename,param,data):
    connection = sqlite3.connect(databasename)
    crsr = connection.cursor()
    
    for dataValue in data:
        sql_command = "INSERT INTO "+tablename+" VALUES("
        for _ in param:
            temp = param[_]
            fieldType = temp[0]
            JsonName = temp[1]
            fieldData = dataValue[JsonName]
            if fieldType =="TEXT":
                sql_command = sql_command + "\""+str(fieldData)+"\","
            else:
                 sql_command = sql_command + str(fieldData)+","
        sql_command = sql_command[:-1:1] + ")"
        crsr.execute(sql_command) 
    connection.commit()
    connection.close()

def addPageInfo(magID,tablename,databasename):
    param = {"ImageURL":"TEXT", "Title":"TEXT", "Subtitle":"TEXT", "MagazineID":"TEXT","IssueID":"TEXT","IssueDate":"TEXT"} 
    createDatabase(databasename,tablename, param)
    text = "TEXT"
    params = {"ImageURL":(text,"image_url"), "Title":(text,"title"), "Subtitle": (text,"subtitle"), "MagazineID":(text,"magazine_id"), "IssueID":(text,"issue_id"),"IssueDate":(text,"issue_date")}
    data = downloadData(magID)
    addJSONData(databasename,tablename,params,data)

def updateData(tablename,magID,databasename):
    addPageInfo(magID,tablename,databasename)

"Main code starts:"


def startDownload(magID,inp):
# initialise databasename
    databasename = magID+".db"
    tablename = "main"
    if not os.path.isdir("web\\database"):
        os.mkdir("web\\database")
    # check if database file exists
    if os.path.exists("web\\database\\"+databasename):
        # Remove comment to access from command line
        # inp = int(input("database already exist.\nPress 1 to dropdatabase.\nPress 2 to load data from database.\nInput:"))
        # setting default input to "always update".
        if(inp  == 1):
            updateData(tablename,magID,databasename)
            os.remove("web\\database\\"+databasename)
            os.system("cp "+databasename+" web\\database\\"+databasename)
            os.remove(databasename)
            print(" \(ᵔᵕᵔ)/")
        elif(inp == 2):
            print(" \(ᵔᵕᵔ)/")
        else:
            print("Input error.\nExiting ...")
    else:
        updateData(tablename,magID,databasename)
        os.system("cp "+databasename+" web\\database\\"+databasename)
        os.remove(databasename)
