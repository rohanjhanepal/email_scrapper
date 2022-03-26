from selenium import webdriver
import re
import csv
#from email_validator import validate_email, EmailNotValidError
from datetime import datetime as dt
from time import sleep
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
chromedriver_location = "C:\\chromedriver"
print("You must have chromedriver placed in c drive")
try:
    driver = webdriver.Chrome(chromedriver_location)
except:
    print("please update chromedriver version or get one if you dont have")


def validate(email):
    try:
        if(re.search(regex,email) or ('.com.' in email)):  
            return email 
        else:  
            return None  
    except:
        return None
    
def GetSites(link): #Scrap from a page of google
    #driver = webdriver.Chrome(chromedriver_location)
    global driver
    try:
        page = driver.get(link)
        all_links=[]
        for i in range(0,10):
            try:
            #datalist = driver.find_elements_by_xpath('//*[@id="rso"]/div[{}]/div/div[1]/a'.format(i))
                datalist = driver.find_elements_by_xpath('//*[@id="rso"]/div/div[{}]/div/div/div[1]/a'.format(i))  
                all_links.append(str(datalist[0].get_attribute('href')))
            except:
                pass
            
    except:
        driver.quit()
        driver = webdriver.Chrome(chromedriver_location)
    #driver.quit()
    return all_links

def Scrap(link): #Scrap from a website
    #driver = webdriver.Chrome(chromedriver_location)
    if(('https:' not in link) and ('http:' not in link)):
        link = 'https://'+ link
    page = driver.get(link)
    dataList = driver.find_elements_by_tag_name('a')
    final = []
    for i in dataList:
        val = i.get_attribute('href')
        try:
            if('@' in val):
                if(('mailto:' in val) or ('mail:' in val)):
                    val = val.split(':')[1]
                if(('+' in val)):
                    val = val.split('+')[1]
                final.append(val)
        except:
            pass
    try:
        doc = driver.page_source
        txts = re.findall(r'[\w\.-]+@[\w\.-]+',doc)
        
        final.extend(txts)
    except:
        pass
    #driver.close()
    return final

final=[]


def LinkToEmail(link , pages=10):
    global final , driver
    for j in range(0,pages):
         
        all_links = GetSites(link)
        i=0
        while(i<len(all_links)):
            sleep(2)
            try:
                list_emails = Scrap(all_links[i])
                sleep(1)
                final.extend(list_emails)
                print(all_links[i])
                i = i+1
            except:
                driver = webdriver.Chrome(chromedriver_location)
                i = i+1
                continue
            print("Emails From This site------------------>{}".format(len(list(set(list_emails)))))
            print("Emails Total -------------------------->{}".format(len(list(set(final)))))
        driver.get(link)
        
        try:
            next = driver.find_element_by_xpath('//*[@id="pnnext"]')
            link = next.get_attribute('href')
        except:
            pass
    final = list(set(final))
    final = [i for i in set(final) if validate(i)!=None]
    return list(set(final))

def SetFileName():
    p = dt.now()
    name = p.strftime("%Y_%m_%d_%I_%M_%S")
    return name

def Save(row_list , filename=SetFileName()): #takes list of emails and file name to save on to
    filename = filename+'.csv'
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for i in row_list:
            writer.writerow([i])


user_choice = ""
while True:
    link=input('Enter Link of first page of google please \nor press q and the enter to quit\n>>')
    if(link == 'q'):
        driver.quit()
        break
    try:
        LinkToEmail(link , pages =20)
        print("done")
    except:
        print("some error occoured")
    print("saving ... ")
    
    Save(list(set(final)))
    print("saved")
    print("total emails scrapped: " , len(list(set(final))))
    final = []
    break
    
    
