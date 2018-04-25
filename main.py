import requests
from bs4 import BeautifulSoup

#using kids skills as lifehacks isn't visible yet
baseURL = 'http://alexakidskills.devpost.com/submissions?page='
r = requests.get(baseURL+'1')
soup = BeautifulSoup(r.text,'html.parser')

#get no. of pages
ul = soup.find('ul',attrs={'class':'pagination'}).find_all('li')
totalPages = int(ul[len(ul)-2].text)
print(totalPages)

submissions = []
#iterate through pages
for i in range(1,totalPages+1):
    #load page
    print('Loading page ' + str(i))
    r = requests.get(baseURL + str(i))
    soup = BeautifulSoup(r.text,'html.parser')

    #get submissions on page
    div = soup.find('div',attrs={'id':'submission-gallery'})
    #get all the rows
    rows = div.find_all('div',attrs={'class':'row'})
    for j in range(2,len(rows)): #iterate through the rows
        columns = rows[j].find_all('div',attrs={'class':'software-entry-name entry-body'})
        for column in columns: #iterate through the columns in the rows
            #get the title and tagline
            title = column.find('h5').get_text(strip=True)
            tagLine = column.find('p',attrs={'class':'small tagline'}).get_text(strip=True)
            print('Title: ',title)
            #add submissions to list
            submissions.append({'title':title,'tagLine':tagLine})


print(submissions)
#Alexa, ask 'is meta' for a cool lifehack idea
#Alexa, ask 'is meta' for a kids idea
#here is an idea: Math Maker. The tagline can be: Using this alexa skill you can easily generate multiplication and division problems.

#optimize by loading a random page


