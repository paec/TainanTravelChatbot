import Entity
import json
from response import getResponseText
import RE
import session_init
import acessmysql
import pymysql
from fuzzywuzzy import fuzz
import privateInfo
from CN2Num import _trans
import railway

nothasfollowupIntent = ["Welcome","NotDefined"]
endingIntent = ["Roomnumconfirmed","CallingConfirmed","Getrestaurantinfo","TrainConfirmed"]

Session = dict()
originString = ""

def getIntent(inputlist):

    global Session

    matchingEntity = dict()
    Intent = ""
    print("\ncontext before: "+Session['context'])

# ---------------------------判斷user input包含哪些entity----------------------------
    print("斷詞結果: "+str(inputlist))

    conn = pymysql.connect(
    host = privateInfo.mysqlaccount.ip ,
    user = privateInfo.mysqlaccount.user,
    password = privateInfo.mysqlaccount.password,
    database = privateInfo.mysqlaccount.dbname,
    charset = 'utf8',
    cursorclass = pymysql.cursors.DictCursor)

    cursor = conn.cursor()

    for word in inputlist:

        data = acessmysql.querydb("SELECT * FROM `BookingChatbot_Entity` WHERE name LIKE '"+word.lower()+"'",conn,cursor)

        entity = data[0]['entity'] if len(data)>0 else None

        if entity:

            if entity == "location":  # 有些參數可能需要match兩次以上，須把參數存成list

                if entity not in matchingEntity:
                    matchingEntity[entity] = [word]
                    print(1)

                else:
                    matchingEntity[entity].append(word)
                    print(2)

            else:
                matchingEntity[entity] = data[0]['name']



# ---------------------------------沒有任何context----------------------------------------
  	
    if Session['context'] == 'None' :
        
        if "welcome" in matchingEntity:                                                 #Welcome

            Intent= "Welcome"  #沒參數也帶一個空字串，避免tuple變str


        if any(entity in matchingEntity for entity in ["hotel"]):             #Bookinghotel

            Intent = "Bookinghotel"
            Session["hotel"] = matchingEntity["hotel"]

        if "callcar" in matchingEntity:

            Intent = "CallingCar"

        if "eating" in matchingEntity or "restaurant" in matchingEntity:

            Session["queryTimes"] = 1 #用於計算抓餐廳的迴圈開始index

            if 'queryResult' not in Session:

                cursor.execute("SELECT * FROM BookingChatbot_Restaurant ORDER BY rating desc LIMIT 200")

                result = cursor.fetchall()

                Session["queryResult"] = result    

            Intent = "EatingService"

        if any(entity in matchingEntity for entity in["train"]):

            Intent = "Bookingtrain"

        elif Intent=="":                                                                #NotDefined 沒匹配到任何intent

            Intent = "NotDefined" 


# -----------------------------------訂飯店--------------------------------------------

    elif Session['context'] == "Bookinghotel":  #飯店名稱，使用字串匹配

        with open("jieba\\"+"hotelname.txt","r",encoding="utf8") as r:

            hotelname = ""
            maxscore = 0 

            hotellist = r.read().splitlines()

            for name in hotellist:

                score = fuzz.ratio(originString, name)

                if score > maxscore :
                    maxscore = score
                    hotelname = name

            print("maxscore: ",maxscore)

            if maxscore > 25:
                Intent = "Confirmhotel"
                Session["hotelname"] = hotelname
           
            else:

                Intent = "NotDefined"


    elif Session['context'] == "Confirmhotel":

        if "true" in matchingEntity:

            Intent = "truehotel"

        elif "false" in matchingEntity:
            Session["hotelname"] = ""
            Intent = "Bookinghotel"

        else:

            Intent = "NotDefined"


    elif Session['context'] == "truehotel":

        match = RE.date_pattern.search(originString)

        if match:

            result = "2019-"+match.group(1)+"-"+match.group(2)

            Session["date"] = result
            
            Intent = "Dateconfirmed"
     

        else:

            Intent = "NotDefined"


    elif Session['context'] == "Dateconfirmed":

        result = RE.num_pattern.findall(originString)

        if len(result) > 0:

            Intent = "Roomnumconfirmed"
            Session["number"] = _trans(result[0])

        else:

            Intent = "NotDefined"


# -----------------------------------叫車-----------------------------------------

    elif Session['context'] == "CallingCar":

        for word in inputlist:

            data = ""

            if len(word) > 1:
                data = acessmysql.querydb("SELECT name FROM `BookingChatbot_TainanLocation` WHERE name LIKE '%"+word.lower()+"%'",conn,cursor)
                print("time")
            if len(data)>0:

                entity = "location"

                if entity not in matchingEntity:
                    matchingEntity[entity] = [data[0]['name']]
                    print(1)

                else:
                    matchingEntity[entity].append(data[0]['name'])
                    print(2)


        if "location" in matchingEntity and len(matchingEntity["location"]) == 2:

            Intent = "Confirmpassenger"
            Session["location"] = matchingEntity["location"]
            

        else:
            Intent = "NotDefined"


    elif Session['context'] == "Confirmpassenger":

        result = RE.num_pattern.findall(originString)

        if len(result) > 0:

            Intent = "CallingConfirmed"
            Session["number"] = _trans(result[0])

        else:

            Intent = "NotDefined"
  

# ---------------------------------餐廳----------------------------------------------

    elif Session['context'] == "EatingService":

        maxscore = 0

        for i in range(Session['queryTimes']*10):

            name = Session['queryResult'][i]['name']

            score = fuzz.ratio(originString, name)

            if score > maxscore :
                maxscore = score
                restaurantname = name

        print("maxscore: ",maxscore)

        if maxscore >= 50:
            
            Intent = "Getrestaurantinfo"
            Session["restaurantname"] = restaurantname

            cursor.execute("SELECT address , phone FROM BookingChatbot_Restaurant WHERE name = '"+restaurantname+"'")

            result = cursor.fetchone()

            Session["restaurantinfo"] = result

        else:

            with open(".//jieba//restaurantname.txt","r",encoding="utf8") as r:

                restaurantlist = r.read().splitlines()

            mathcinglist = []

            for restaurant in restaurantlist:

                if restaurant.find(originString) != -1 :

                    mathcinglist.append(restaurant)


            if len(mathcinglist) > 0 :

                Intent = "Getrestaurantlist"
                print(restaurantlist)

            else:

                Intent = "NotDefined"


#--------------------------------訂車票------------------------------------------------

    elif Session['context'] == "Bookingtrain":

        for word in inputlist:

            data = acessmysql.querydb("SELECT name FROM `BookingChatbot_TWRailwayStation` WHERE name ='"+word.lower()+"'",conn,cursor)

            print(data)

            if len(data)>0:

                entity = "location"

                if entity not in matchingEntity:
                    matchingEntity[entity] = [data[0]['name']]
                    print(1)

                else:
                    matchingEntity[entity].append(data[0]['name'])
                    print(2)


        if "location" in matchingEntity and len(matchingEntity["location"]) == 2:

            Intent = "Confirmdate"
            Session["location"] = matchingEntity["location"]
            

        else:
            Intent = "NotDefined"


    elif Session['context'] == "Confirmdate" :

        match = RE.date_pattern.search(originString)

        if match:

            result = "2019-"+match.group(1)+"-"+match.group(2)

            Session["date"] = result

            timetable = railway.getTimetable(Session['location'][0],Session['location'][1],Session["date"],Session["time"])

            if timetable == "notrain":

                Intent = "Bookingtrain"

            else:
                Session["queryResult"] = timetable
                Intent = "Confirmtrain"

        else:

            Intent = "NotDefined"


    elif Session['context'] == "Confirmtrain":

        result = RE.num_pattern.findall(originString)

        if len(result) > 0:

            Session["number"] = _trans(result[0])

            Intent = "TrainConfirmed"

        else:

            Intent = "NotDefined"


#------------------------------------------------------------------------------------

    cursor.close()
    conn.close()

    print("匹配到的Entity: "+str(matchingEntity))
    print("匹配到的Intent: "+Intent)

    return Intent
    


# ----------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------------#


def getResponse(input,session):

    global Session
    global originString

    Session = session
    originString = input['originData']

    print(Session)

    Intent = getIntent(input['segdata'])
    

    botresponse = getResponseText(Intent,Session)


    if Intent not in nothasfollowupIntent and Intent not in endingIntent:
        Session['context'] = Intent 

    elif Intent in endingIntent:
        
        Session = session_init.initsession(Session)
     


    print("context after: "+str(Session['context'])+"\n")
    # print("Session content: "+str(Session))

    AjaxResponse = {"botresponse": botresponse , "session": Session}

    return AjaxResponse




