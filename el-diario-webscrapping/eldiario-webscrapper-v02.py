import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
import time
import subprocess
from datetime import timedelta, date 

article_name = []
article_date = []
article_words = []
article_len = []
article_URL = []
article_category = []

categories =['i_politica.php', 'i_sociedad.php', 'i_nacional.php']

# Use a sequence of args

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

start_date = date(2019, 1, 1)
end_date = date(2020, 1, 30)
for single_date in daterange(start_date, end_date):
    news_date = single_date.strftime("%Y-%m-%d")
    
    for category in categories:       
        #this defines the changing name of each article
        name = category
        if single_date.month > 9:
            if single_date.day > 9:
                URL = f'https://www.eldiario.net/noticias/{str(single_date.year)}/{str(single_date.year)}_{str(single_date.month)}/nt{str(single_date.year)[2:4]}{str(single_date.month)}{str(single_date.day)}/{name}'
                print(URL)
            else:
                URL = f'https://www.eldiario.net/noticias/{str(single_date.year)}/{str(single_date.year)}_{str(single_date.month)}/nt{str(single_date.year)[2:4]}{str(single_date.month)}0{str(single_date.day)}/{name}'
                print(URL)                     
        else:
            if single_date.day > 9:
                URL = f'https://www.eldiario.net/noticias/{str(single_date.year)}/{str(single_date.year)}_0{str(single_date.month)}/nt{str(single_date.year)[2:4]}0{str(single_date.month)}{str(single_date.day)}/{name}'
                print(URL)
            else:
                URL = f'https://www.eldiario.net/noticias/{str(single_date.year)}/{str(single_date.year)}_0{str(single_date.month)}/nt{str(single_date.year)[2:4]}0{str(single_date.month)}0{str(single_date.day)}/{name}'
                print(URL)  

        #------------------------------------------------
        #--------------- FIRST PART ---------------------
        #------------------------------------------------

        #This part of the code retrieves the links of the news (1 for now).

        #The first request
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        
        

        #The part where the desired info is:
        main_body = soup.find(id='col_a')

        #print(main_body.prettify())

        #once we have the main body, this is the way to get the link.
        links_with_text=[]
        try:
            for a in main_body.find_all('a', href=True): 
                if a.text:
                    links_with_text.append(a['href'])
        except Exception:
            continue       

        #Now, the 'name' will change and will be the link of the new we want to analyze.
        name = str(links_with_text[0])

        #------------------------------------------------
        #--------------- SECOND PART --------------------
        #------------------------------------------------

        #This part analyze the given new
        if single_date.month > 9:
            if single_date.day > 9:
                URL = f'https://www.eldiario.net/noticias/{str(single_date.year)}/{str(single_date.year)}_{str(single_date.month)}/nt{str(single_date.year)[2:4]}{str(single_date.month)}{str(single_date.day)}/{name}'
                #print(URL)
            else:
                URL = f'https://www.eldiario.net/noticias/{str(single_date.year)}/{str(single_date.year)}_{str(single_date.month)}/nt{str(single_date.year)[2:4]}{str(single_date.month)}0{str(single_date.day)}/{name}'
                #print(URL)                     
        else:
            if single_date.day > 9:
                URL = f'https://www.eldiario.net/noticias/{str(single_date.year)}/{str(single_date.year)}_0{str(single_date.month)}/nt{str(single_date.year)[2:4]}0{str(single_date.month)}{str(single_date.day)}/{name}'
                #print(URL)
            else:
                URL = f'https://www.eldiario.net/noticias/{str(single_date.year)}/{str(single_date.year)}_0{str(single_date.month)}/nt{str(single_date.year)[2:4]}0{str(single_date.month)}0{str(single_date.day)}/{name}'
                #print(URL)      

        #This part analyze the given new
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')

        # The part where the desired info is:
        main_body = soup.find(id='col_a')

        #print(results.prettify())

        #Accesing the main body of the article
        main_body_parts = []
        for part in main_body.select('div'): 
            #print('---------------------')
            #print(elem)
            main_body_parts.append(part)

        #print(divs[0])

        # Here is my beloved text
        main_text = main_body_parts[0].find('div', class_ ="nota_txt")

        try:
            texto_completo = main_text.find_all('p')
        except Exception:
            continue 
        

        #Lets get rid of everything but the text itsef.
        #It will be store in 'phrases'.
        phrases = []
        for fragmento in texto_completo:
            phrases.append(fragmento.getText())    

        #--------------------    

        # In this part of the code, the phrases are split and store
        # along with more info, such as date or number of words.
        list_words = []

        for phrase in phrases:
            list_words.append(phrase.split())

        #super fast way to flatten a nested list
        flatten_words = [x for y in list_words for x in y]

        #super fast way to remove empty lists
        only_words = [word for word in flatten_words if word != []]
        
        #writting nice the category
        if category == 'i_politica.php':
            article_category.append('politica')
        elif category == 'i_sociedad.php':
            article_category.append('sociedad')
        else:
            article_category.append('nacional')

        #time to add the info to different lists
        article_name.append(str(name))      
        article_date.append(news_date)
        article_words.append(only_words)
        article_len.append(len(only_words))
        article_URL.append(URL)

        time.sleep(0.5)
        
#------------------------------------------------
#--------------- PANDAS PART --------------------
#------------------------------------------------
                            
df = pd.DataFrame(list(zip(article_name, article_date,article_category,article_words,article_len,article_URL)), 
               columns =['article_name', 'article_date','article_category', 'article_words','article_len','article_URL'])
                            
df.to_csv(f'eldiario{start_date}_{end_date}.csv')