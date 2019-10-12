# download and decrypt PDF file
import urllib
import urllib.request
import sys
import os
import base64decoding
import PDFdecrypt
import time
import progressbar
global bar,downloaded
bar = 0
downloaded = 0
format_custom_text = progressbar.FormatCustomText(
' Downloading: %(current)d Bytes of %(total)d Bytes',
dict(
    total = 0,
    current = 0,
    ),
)

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

def get_progress(count, block_size, total_size):
    global downloaded
    downloaded += block_size
    percent = (downloaded*100)//total_size
    format_custom_text.update_mapping(current = downloaded, total= total_size)
    bar.update(percent)

def downloadFile(magid, issueid, link,content_key):
    url = link
    headers = {
        "Host": "jionewsweb.cdn.jio.com",
    "Connection" : "Keep-Alive",
    "Accept-Encoding" : "gzip",
    "User-Agent" : "okhttp/3.14.1"
        }
    opener = urllib.request.build_opener()
    opener.addheaders = [("Host", "jionewsweb.cdn.jio.com"),("Connection" , "Keep-Alive"),("Accept-Encoding" , "gzip"),("User-Agent" , "okhttp/3.14.1")]
    urllib.request.install_opener(opener)
    if not os.path.isdir("web\\downloads"):
        os.mkdir("web\\downloads")
    if not os.path.isdir("web\\downloads\\" + magid):
        os.mkdir("web\\downloads\\" + magid)
    if not os.path.exists("web\\downloads\\"+magid+"\\"+issueid+".pdf"):
        print("Downloading - ",magid, issueid)
        startBar(100)
        resp = urllib.request.urlretrieve(url,"web\\downloads\\"+magid+"\\"+issueid+".pdf",reporthook = get_progress)
        bar.finish()
        print("Decoding File...")
        password = base64decoding.decode(content_key)
        PDFdecrypt.decrypt_pdf("web\\downloads\\"+magid+"\\"+issueid+".pdf","web\\downloads\\"+magid+"\\"+issueid+"dec.pdf",password)
        print("Moving file to folder")
        os.remove("web\\downloads\\"+magid+"\\"+issueid+".pdf")
        os.rename("web\\downloads\\"+magid+"\\"+issueid+"dec.pdf","web\\downloads\\"+magid+"\\"+issueid+".pdf")
    print("Loading ...")
    return "yes"
