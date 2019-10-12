# upadate or make database as per Category

import requests as handler
import os
import json
import sys
import sqlite3

def downloadData(pagetype):
    url = geturl(pagetype)
    headers = getheaders()
    data  = handler.get(url, headers = headers)
    data = json.loads(data.text)
    print(pagetype,"Download completed .\n")
    data = data['result']['items']
    return data

def geturl(param):
    host = "http://jionewsapi.media.jio.com"
    magUrl  = "/magazines/apis/v1.1/magsbycategory?langIds=1%2C2&limit=50&offset=0&catId="+param
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
    
def addJSONData(databasename,tablename,param,data,pagetype):
    connection = sqlite3.connect(databasename)
    crsr = connection.cursor()
    
    for dataValue in data:
        # adding pageType value
        dataValue["page_type"] = pagetype
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

def addPageInfo(pagetype,tablename):
    param = {"PageType":"TEXT","ImageURL":"TEXT", "Title":"TEXT", "Subtitle":"TEXT", "MagazineID":"TEXT","IssueID":"TEXT"} 
    createDatabase(databasename,tablename, param)
    text = "TEXT"
    params = {"PageType":(text,"page_type"),"ImageURL":(text,"image_url"), "Title":(text,"title"), "Subtitle": (text,"subtitle"), "MagazineID":(text,"magazine_id"), "IssueID":(text,"issue_id")}
    data = downloadData(pagetype)
    addJSONData(databasename,tablename,params,data,pagetype)

def updateData(tablename):
    for count in range(1,19,1):
        addPageInfo(str(count),tablename)

"Main code starts:"

# initialise databasename
databasename = "database.db"
tablename = "Category_DATA"

# check if database file exists
if os.path.exists(databasename):
    try:
        # Remove comment to access from command line
        # inp = int(input("database already exist.\nPress 1 to dropdatabase.\nPress 2 to load data from database.\nInput:"))
        # setting default input to "always update".
        inp = 1
    except:
        print("Input error.\nExiting ...")
    if(inp  == 1):
            droptable(tablename)
            # load data // To add code
            updateData(tablename)
            print(" add code")
            print(" \(ᵔᵕᵔ)/")
    elif(inp == 2):
        print(" add code")
        print(" \(ᵔᵕᵔ)/")
    else:
        print("Input error.\nExiting ...")
else:
    updateData(tablename)
