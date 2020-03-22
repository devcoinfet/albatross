import requests
from bs4 import BeautifulSoup
import re
import string
import random
import cv2
import sys
from base64 import decodestring
from PIL import *
#import ImageEnhance
from pytesseract import *



#cracking tor russian Drug Forum captchas for fun and profit than we can scan them and look for juicy stuff :)
#forget the exact site this was but mod it to your liking so you can mess with tor related asshats use only for research please dont harm people
#you find a bug good for you just be a professional this just lowers the bar with them hiding over tor as we can reach it via code now
#im 100% not the first to do it and probably isnt even that great just my take on it code probably isnt all mine i stackoverflow way too much sorry for not documenting most is mine

class Darknet_Osint:
    def __init__(self,name):
        self.osint_intel = []
        self.name = name

    def id_generator(self,size=6, chars=string.ascii_uppercase + string.digits):
        generated_id = ''.join(random.choice(chars) for _ in range(size))
        return  generated_id


    
    def way_to_captcha_crack(self,image_b64):
        file_start = id_generator()
        file_path = file_start +"_captcha.png"
        try:
            base64JustDataTxt = image_b64.replace("data:image/jpeg;base64,", "")
            print(base64JustDataTxt)
            with open(file_path,"wb") as f:
               f.write(decodestring(base64JustDataTxt))
        except:
           pass
    

   
    def extract_form_fields(self,soup):
        "Turn a BeautifulSoup form in to a dict of fields and default values"
        fields = {}
        image_b64 = ""
    
        for input in soup.findAll('input'):
            unu =""
        
        images = soup.findAll('img')
        for image in images:
            image_b64 = image['src']
            #print(image['src'])
        return image_b64


    def intel_grabber(self,url):
          
        session = requests.session()
        session.proxies = {}
        session.proxies['http'] = 'socks5h://localhost:9050'
        session.proxies['https'] = 'socks5h://localhost:9050'
    
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'referrer': str(url),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Pragma': 'no-cache',
        }
        try:
           r = session.get(str(url),headers=headers,timeout=5,verify=False)
           print(r.headers)
           print(r.text)
           captcha_token = re.findall('captcha_image" value="(.+)">',r.text)
           if captcha_token:

              soup = BeautifulSoup(r.text, "html.parser")
              image_b64 = extract_form_fields(soup)
              print("Succesfully Extracted Image:  "+str(image_b64)) 
              print("Succesfully Extracted Cpatcha Token:"+str(captcha_token))
              local_dict = {"Image_B64":str(image_b64),"Captcha_Token":str(captcha_token),"CSRF_TOKEN":r.cookies['csrftoken']}
              self.osint_intel.append(local_dict)
              try:
                 self.way_to_captcha_crack(image_b64)
              except:
                  pass
           else:
              CSRF_token = re.findall('csrfmiddlewaretoken" value="(.+)">',r.text)
              soup = BeautifulSoup(r.text, "html.parser")
              image_b64 = extract_form_fields(soup)
              print("Succesfully Extracted Image:  "+str(image_b64)) 
              print("Succesfully Extracted Cpatcha Token:"+str(captcha_token))
              local_dict = {"Image_B64":str(image_b64),"Captcha_Token":str(captcha_token),"CSRF_TOKEN":r.cookies['csrftoken']}
              self.osint_intel.append(local_dict)
              try:
                 self.way_to_captcha_crack(image_b64)
              except:
                  pass
        except:
            pass

  
        print(r.cookies)


def main():
    Target = sys.argv[1]
    Dark_Osint = Darknet_Osint(Target)
    try:
        Dark_Osint.intel_grabber(Target)
    except:
        pass
    for items in Dark_Osint.osint_intel:
        print(str(items))


main()
