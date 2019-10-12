# decrypt and save PDF file
from PyPDF2 import PdfFileReader, PdfFileWriter
import time
import progressbar

global bar
bar = 0

format_custom_text = progressbar.FormatCustomText(
    ' Decrypting: %(current)d out of %(total)d Pages',
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

def progressCheck(current,total):
    format_custom_text.update_mapping(current = current, total= total)
    bar.update(current)

def decrypt_pdf(input_path, output_path, password):
    print("If decryption takes too much time.\nOpen file in web/download folder with this password",password)
    with open(input_path, 'rb') as input_file, \
        open(output_path, 'wb') as output_file:
        reader = PdfFileReader(input_file)
        reader.decrypt(password)
        writer = PdfFileWriter()
        num_page = reader.getNumPages()
        print("Writing File may take a few minutes...\nPlease don't close the file")
        startBar(num_page)
        for i in range(num_page):
          writer.addPage(reader.getPage(i))
          progressCheck(i+1,num_page)
        bar.finish()
        writer.write(output_file)
        
