import gdown
from zipfile import ZipFile
import os

url = ''
with open('link_model.txt') as file:
    url = file.read()

os.makedirs('model')
output = 'model/model.zip'
gdown.download(url, output, quiet=False)


with ZipFile(output, 'r') as zipObj:
    # Extract all the contents of zip file in current directory
    zipObj.extractall()

os.remove(output)
