import requests
from random import randint
from bs4 import BeautifulSoup


locations = []
locations.append({'intent':'kids','location':'alexakidskills'})
locations.append({'intent':'life hacks','location':'alexalifehacks'})
locations.append({'intent':'hackathon','location':'alexakidskills'})#tbd

def getAllIdeas(location = 'alexakidskills'):
    #location could be alexakidskills or any other devpost
    baseURL = 'http://' + location + '.devpost.com/submissions?page='
    r = requests.get(baseURL+'1')
    soup = BeautifulSoup(r.text,'html.parser')

    #get no. of pages
    ul = soup.find('ul',attrs={'class':'pagination'}).find_all('li')
    totalPages = int(ul[len(ul)-2].text)
    print('Total pages: ', totalPages)

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

    return submissions

def getRandomIdea(location = 'alexakidskills'):
    #location could be alexakidskills or any other devpost
    baseURL = 'http://' + location + '.devpost.com/submissions?page='
    r = requests.get(baseURL+'1')
    soup = BeautifulSoup(r.text,'html.parser')

    #get no. of pages
    ul = soup.find('ul',attrs={'class':'pagination'}).find_all('li')
    totalPages = int(ul[len(ul)-2].text)
    print('Total pages: ', totalPages)
    #get a random page
    page = randint(1,totalPages)
    
    #load random page
    print('Loading page ' + str(page))
    r = requests.get(baseURL + str(page))
    soup = BeautifulSoup(r.text,'html.parser')

    #get submissions on page
    div = soup.find('div',attrs={'id':'submission-gallery'})
    #get all the rows
    rows = div.find_all('div',attrs={'class':'row'})
    #pick a random row
    row = randint(2,len(rows)-1)
    print('Loading row: ', row)
    columns = rows[row].find_all('div',attrs={'class':'software-entry-name entry-body'})
    #pick a random column
    col = randint(0,len(columns)-1)
    print('Loading column: ', col)
    column = columns[col]
    #get the title and tagline
    title = column.find('h5').get_text(strip=True)
    tagLine = column.find('p',attrs={'class':'small tagline'}).get_text(strip=True)
    print('Title: ',title)
    submission = {'title':title,'tagLine':tagLine}
    return submission

def search(intent):
    global locations
    return next((item for item in locations if item["intent"] == intent))

#Alexa, ask 'is meta' for a cool lifehack idea
#Alexa, ask 'is meta' for a kids idea
#here is an idea: Math Maker. The tagline can be: Using this alexa skill you can easily generate multiplication and division problems.

#optimize by loading a random page



#Alexa Code:
#v       v
# v     v
#  v   v
#   v v
#    v


# --------------- entry point -----------------

def lambda_handler(event, context):
    """ App entry point  """
    
    if event['request']['type'] == "LaunchRequest":
        return on_launch()
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'])


# --------------- response handlers -----------------

def on_intent(request, session):
    """ Called on receipt of an Intent  """

    intent = request['intent']
    intent_name = request['intent']['name']

    #print("on_intent " +intent_name)
    get_state(session)

    if 'dialogState' in request:
        #delegate to Alexa until dialog sequence is complete
        if request['dialogState'] == "STARTED" or request['dialogState'] == "IN_PROGRESS":
            return dialog_response("", False)

    # process the intents
    if intent_name == "getIdea":
        return do_main_action(request, intent)
    elif intent_name == "AMAZON.HelpIntent":
        return do_help()
    elif intent_name == "AMAZON.StopIntent":
        return do_stop()
    elif intent_name == "AMAZON.CancelIntent":
        return do_stop()
    else:
        print("invalid intent reply with help")
        return do_help()

def do_main_action(request, intent):
    #check for intent
    if 'ideaType' and intent['slots'] in intent['slots']:
        ideaType = intent['slots']['Item']['Value']
        print(ideaType)
        item = search(ideaType)
        location = item['location']
        idea = getRandomIdea(location)
        name = idea['name']
        tagline = idea['tagline']
        #here is an idea: Math Maker. The tagline can be: Using this alexa skill you can easily generate multiplication and division problems.
        msg = "Here is a ",ideaType, "idea: ", name, ". The tagline could be: ", tagline
    else:
        return get_welcome_message()



def do_stop():
    """  stop the app """
    exitMsg = "Ok"
    attributes = {}
    return response(attributes, response_plain_text(exitMsg, True))

def do_help():
    """ return a help response  """
    helpMsg = "Ask me: 'What is a good kids skill idea?'"
    attributes = {}
    return response(attributes, response_plain_text(helpMsg, False))

def on_launch():
    """ called on Launch reply with a welcome message """
 
    return get_welcome_message()

def on_session_ended(request):
    """ called on session end  """

    if request['reason']:
        end_reason = request['reason']
        print("on_session_ended reason: " + end_reason)
    else:
    print("on_session_ended")


# --------------- response string formatters -----------------

def get_welcome_message():
    """ return a welcome message """
    welcomeMsg = ("Welcome to Is Meta. "
    "I can give you an idea for a hackathon, a life hack skill, or a kids skill "
    "What would you like to do? ")

    attributes = {}
    return response(attributes, response_plain_text(welcomeMsg, False))



# --------------- speech response handlers -----------------

def response_plain_text(output, endsession):
    """ create a simple json plain text response  """

    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'shouldEndSession': endsession
    }


def response(attributes, speech_response):
    """ create a simple json response """

    return {
        'version': '1.0',
        'sessionAttributes': attributes,
        'response': speech_response
    }