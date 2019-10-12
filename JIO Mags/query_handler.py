# fetch query from database
import sqlite3
import os
import sys
import time

def query(databasename,accessTableName,queryParam):
    connection = sqlite3.connect(databasename) 
    crsr = connection.cursor()
    sql_statement = "SELECT * FROM "+accessTableName+" WHERE "
    if queryParam!=None:
        for _ in (queryParam):
            sql_statement = sql_statement + _+"="+queryParam[_]+",\n"
        sql_statement = sql_statement[:-2:1]+";"
    else:
        sql_statement = "SELECT * FROM "+accessTableName+";"
    crsr.execute(sql_statement)
    query = crsr.fetchall()
    connection.close()
    return query
