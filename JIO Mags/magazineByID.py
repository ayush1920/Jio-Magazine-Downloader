# to get final pdf links

import requests as handler
import json
import os
import download_file
def downloadPDF(magid, issueID):
    f = open("access_token.txt","r")
    accesstoken =f.read()
    f.close()
    f = open("uuid.txt","r")
    uuid=  f.read()
    f.close()
    http = "http://"
    keys = {"issueId": issueID, "uuid": uuid}
    magdownloadurl =  "/download/apis/v1.1/mags/issues"
    length = str(11+len(issueID+uuid))
    headers ={
    "accesstoken" : accesstoken,
    "devicetype": "phone",
    "os": "android",
    "version": "3.1.1",
    "Content-Type" : "application/x-www-form-urlencoded",
    "Content-Length": length,
    "Host" : "jionewsapi.media.jio.com",
    "Connection" : "Keep-Alive",
    "Accept-Encoding" : "gzip",
    "User-Agent" : "okhttp/3.14.1"}

    # send request
    if not os.path.isdir("web\\downloads"):
        os.mkdir("web\\downloads")
    if not os.path.isdir("web\\downloads\\" + magid):
        os.mkdir("web\\downloads\\" + magid)
    if os.path.exists("web\\downloads\\"+magid+"\\"+issueID+".pdf"):
        return "yes"
    host  = headers['Host']
    url = http + host +magdownloadurl
    data = handler.post(url, headers = headers, data=keys)
    data = json.loads(data.text)
    data = data['result']
    page_count = data['page_count']
    subtitle = data['subtitle']
    content_key = data['content_key']
    link  = data['link']
    download_file.downloadFile(magid,issueID,link,content_key)
