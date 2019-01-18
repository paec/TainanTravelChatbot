sessionInformation = ['hotel','hotelname','date','time','number','location',"restaurantname"]

def initsession(sessiondict):
    
    sessiondict = dict()

    sessiondict['context'] = "None"

    for item in sessionInformation:
        sessiondict[item] = ""

    sessiondict['location'] = list()
    # print(str(sessiondict))

    return sessiondict