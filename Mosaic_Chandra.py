'''
Python code to create a chandra mosaic....
1 - Web scrape all the images from the web presses by stepping though each year of the following: http://chandra.harvard.edu/photo/chronological.html
2 - Create Mosaic with the following code: https://github.com/codebox/mosaic
'''

import os
from bs4 import BeautifulSoup
import urllib.request


os.chdir('/home/user/Documents')

years = ['']
for i in range(10):
    years.append('0'+str(i))
for i in range(10,17):
    years.append(str(i))
outp1 = 'Photos/'
if os.path.isdir(os.getcwd()+'/'+outp1) == False:
    os.mkdir(outp1)
if os.path.isdir(os.getcwd()+'/'+outp1+'All') == False:
    os.mkdir(outp1+'All')
for year in years:
    url = "http://chandra.harvard.edu/photo/chronological"+year+".html"
    soup = BeautifulSoup(urllib.request.urlopen(url), "lxml") #lxml gets rid of error
    outfolder = outp1+year+'/'
    if os.path.isdir(os.getcwd() + '/' + outfolder) == False:
        os.mkdir(outfolder)
    imgs = soup.findAll("div", {"class":"page_box2"})
    for img in imgs:
            #imgUrl = img.a['href'].split("imgurl=")
            imgUrl = str(img.img['src'].split("imgurl=")[0])
            print(imgUrl)
            urllib.request.urlretrieve("http://chandra.harvard.edu"+imgUrl,outfolder+imgUrl.split("/")[-1])
            urllib.request.urlretrieve("http://chandra.harvard.edu" + imgUrl, os.getcwd()+'/'+outp1+'All/' + imgUrl.split("/")[-1])
