import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm 
import time 

def jsonADD(ANIME_NAME,ANIME_PLOT,ANIME_OTHER_NAMES,ANIME_RELEASED,ANIME_STATUS,ANIME_TYPE,ANIME_GENRE,ANIME_IMAGE,count):
    # time.sleep(0.01)
    # with open("animeAPI.json", "w") as txt:
    #     txt.write(" ".join('['))
    
    # example dictionary to save as JSON
    data = {
        "Aid": count,
        "Name": ANIME_NAME,
        "Plot": ANIME_PLOT,
        # "Other_Names": ANIME_OTHER_NAMES,
        "Released": ANIME_RELEASED,
        "Status": ANIME_STATUS,
        "Type": ANIME_TYPE,
        "Genre": ANIME_GENRE,
        "ImageURL":ANIME_IMAGE
        # "titles": ["The Unknown", "Anonymous"] # also lists!
    }
    
    if count!=0:
        with open("animeAPI.json", "a") as txt:
            txt.write(" ".join(', ')) #NORMAL WRITE/APPEND

    # # read file
    # with open('animeAPI.json', 'r') as myfile:
    #     data1=myfile.read()
    # obj = json.loads(data1)
    # count-1
    # aid = obj[count]
    # # print(str(aid['Aid']))
    # # if aid['Aid'] == count:
    # #     print("True")

    # print(count+" : "+aid['Aid'])
    # myfile.close()

    # save JSON file
    with open("2021/animeAPI.json", "a") as jsn:
        jsn.write(json.dumps(data, indent=4)) #JSON WRITE/APPEND

    fileHandle = open('2021/animeAPI.json', 'r')
    fileHandle.close()
    
#////////////////////////////////////////////////////////////////////    
def main(): 
    count = 1
    limit = 63
    
    for x in range(limit):
        for i in tqdm (range (100), desc="Loading…", ascii=False, ncols=75):        
            #Change when completed!
            x=x+1
            
            # print('PAGE: '+str(x))
            url = 'https://www26.gogoanimes.tv/anime-list.html?page='+str(x) 
            reqs = requests.get(url)
            soup = BeautifulSoup(reqs.text, 'lxml')

            for ultag in soup.find_all("ul", {"class": 'listing'}):
                for litag in ultag.find_all('li'):
                    for atag in litag.find_all('a'):
                        name = atag.text
                        name = name.split('\n')
                        ANIME_NAME=name[0] #Variable for JSON
                        # print(str(count)+": "+name[0]) # Prints the Anime Name (Title)
                        # print(atag.get('href')) prints the extention link of website
                        

                        aniLink = atag.get('href')
                        aurl = 'https://www26.gogoanimes.tv'+aniLink
                        reqest1 = requests.get(aurl)
                        soup1 = BeautifulSoup(reqest1.text, 'lxml')
                        for divtag in soup1.find_all("div", {"class": 'anime_info_body_bg'}):
                            for ptag in divtag.find_all('p'):
                                #print(ptag.text) #Print all P Tags Data
                                psect = ptag.text
                                psect_split = psect.split('\n')
                                pdata=psect_split[0]

                                plot1 = pdata.split(': ')
                                if plot1[0] == "Plot Summary":
                                    ANIME_PLOT=plot1[1] #Variable for JSON
                                    # print("Plot Summary: "+plot1[1]) #Prints Plot Summary

                                ON1 = pdata.split(': ')
                                if ON1[0] == "Other name":
                                    ANIME_OTHER_NAMES=ON1[1] #Variable for JSON
                                    # print("Other Names: "+ON1[1]) #Prints Other Name
                                
                                rel1 = pdata.split(': ')
                                if rel1[0] == "Released":
                                    ANIME_RELEASED=rel1[1] #Variable for JSON
                                    # print("Released: "+rel1[1]) #Prints Released Year

                                stat1 = pdata.split(': ')
                                if stat1[0] == "Status":
                                    ANIME_STATUS=stat1[1] #Variable for JSON
                                    # print("Status: "+stat1[1]) #Prints Anime Status
                            
                            #FOR TYPE AND GENRE
                            genre=[] 
                            for pptag in divtag.find_all('p', {'class':'type'}):
                                #print("Type: "+pptag.text) #Print all Data with class:type in P Tage
                                for aatag in pptag.find_all("a"):
                                    for spantag in pptag.find_all('span'):
                                        #print(spantag.text)
                                        if spantag.text == "Type: ":
                                            aniType = aatag.text
                                            ANIME_TYPE=aniType #Variable for JSON
                                            # print("Type: "+aniType) #Prints Anime Type
                                        
                                        if spantag.text == "Genre: ":
                                            temp1 = aatag.text
                                            genre.append(temp1) #Adds to Array
                                            ANIME_GENRE=genre #Variable for JSON
                            # print(genre) #Prints Anime Genre Array
                                    

                            for imgtag in divtag.find_all('img'):
                                img=imgtag.get('src')
                                ANIME_IMAGE=img #Variable for JSON

                                # print(imgtag.get('src')) # Prints the IMG url
                                # print("\n\n")
                            
                            # print(ANIME_NAME)
                            # print(ANIME_PLOT)
                            # print(ANIME_GENRE)
                            # print(ANIME_IMAGE)
                            # print(ANIME_RELEASED)
                            # print(ANIME_TYPE)
                            # print(ANIME_STATUS)
                            # print(ANIME_OTHER_NAMES)
                            # print('\n\n')

                            
                            # # Opening JSON file 
                            # f = open('animeAPI.json') 
                            # data = json.load(f) 
                            # # for i in data['emp_details']:
                            # temp= data[0] 
                            # print(temp['Aid'])

                            

                            # CALL JSONADD()
                            jsonADD(ANIME_NAME,
                                    ANIME_PLOT,
                                    ANIME_OTHER_NAMES,
                                    ANIME_RELEASED,
                                    ANIME_STATUS,
                                    ANIME_TYPE,
                                    ANIME_GENRE,
                                    ANIME_IMAGE,
                                    count)
                                    
                            count=count+1

        

        print("Complete.")
        with open("animeAPI.json", "a") as txt:
            txt.write(" ".join(']'))

if __name__ == "__main__":
    main()