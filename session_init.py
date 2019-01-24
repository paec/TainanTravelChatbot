sessionInformation = ['hotel','hotelname','date','time','number','location',"restaurantname"]

def initsession(sessiondict):
    
    sessiondict['context'] = "None"

    for item in sessionInformation:
        sessiondict[item] = ""

    sessiondict['location'] = list()

    return sessiondict