# to fetch data from database on return to html file [Images]

import sqlite3
import os
import sys
import query_handler
import urllib
import urllib.request
import time
import progressbar
databasename= "database.db"
accessTableName1 = "Category_DATA"
accessTableName2 = "Section_DATA"

format_custom_text = progressbar.FormatCustomText(
        ' Checking or downloading: %(current)d out of %(images)d Images',
        dict(
            images = 0,
            current = 0,
        ),
    )
global bar
bar = 0
def startBar(maxval):
    global bar
    bar = progressbar.ProgressBar(
    widgets=[progressbar.SimpleProgress(),
               format_custom_text,
        ' :: ',
              progressbar.Bar('█'), ' ',
        progressbar.ETA(), ' ',],
    max_value=maxval,
    ).start()

def checkDatabase():
    if not os.path.exists(databasename):
        import updateByCategory
        import updateBySection
    
def download_image(imagelink,magId,issueId):
    opener = urllib.request.build_opener()
    headers = [
        ("Host" , "jionewsweb.cdn.jio.com"),
        ("Connection", "Keep-Alive"),
        ("Accept-Encoding" , "gzip"),
        ("User-Agent", "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G950F Build/NRD90M)")
        ]
    opener.addheaders = headers
    urllib.request.install_opener(opener)
    url  = "http://jiomags.cdn.jio.com/content/entry/jiomags/content/" + imagelink
    urllib.request.urlretrieve(url,"web\\mag_images\\"+magId+"\\"+issueId+".jpg")

def checkImageAvailablity(magId, issueId,imagepath):
    if not os.path.isdir("web\\mag_images"):
        os.mkdir("web\\mag_images")
    if not os.path.isdir("web\\mag_images\\"+magId):
        os.mkdir("web\\mag_images\\"+magId)
    if not os.path.exists("web\\mag_images\\"+magId+"\\"+issueId+".jpg"):
        download_image(imagepath, magId,issueId)

def getPageData(pagenumber,datatype):
    checkDatabase()
    if(datatype=="1"):
        accessTableName = accessTableName1
    else:
        accessTableName = accessTableName2
    queryParam = {"PageType": pagenumber}
    data = query_handler.query(databasename, accessTableName, queryParam)
    lis=[]
    cnt = 1
    print("Downloading Images ...")
    startBar(len(data))
    for _ in data:
        image_link = _[1]
        magId = _[4]
        issueId = _[5]
        checkImageAvailablity(magId, issueId,image_link)
        lis.append([magId,issueId])
        format_custom_text.update_mapping(current = cnt, images = len(data))
        bar.update(cnt)
        cnt=cnt+1
    bar.finish()
    return lis
