from io import StringIO
import pymysql
import railway
import privateInfo
import json

endingIntent = ["Roomnumconfirmed","CallingConfirmed","Getrestaurantinfo","TrainConfirmed"]

class StringBuilder:

     _file_str = None

     def __init__(self):
         self._file_str = StringIO()

     def Append(self, str):
         self._file_str.write(str)

     def __str__(self):
         return self._file_str.getvalue()


def getResponseText(Intent,session):

    
    conn = pymysql.connect(
    host = privateInfo.mysqlaccount.ip,
    user = privateInfo.mysqlaccount.user,
    password = privateInfo.mysqlaccount.password,
    database = privateInfo.mysqlaccount.dbname,
    charset = 'utf8',
    cursorclass = pymysql.cursors.DictCursor)

    cursor = conn.cursor()    

    intent = Intent

    if len(session['location']) >= 2 :
        loc1 = session['location'][0]
        loc2 = session['location'][1]
    else:
        loc1 = ""
        loc2 = ""

    responseDict = {
        
    "Welcome" : ["您好!!","哈囉!!"],

    "Bookinghotel" : ["請問您要預訂哪間"+session['hotel']+"呢?"],

    "Confirmhotel" : ["您要預訂的是\""+session['hotelname']+"\"嗎?"],

    "truehotel" : ["將幫您預定\""+session['hotelname']+"\"。"+"@@@"+"接下來，請告訴我預訂的詳細資訊"+"@@@"+"請問預計的入住日期是?"] ,

    "Dateconfirmed" : ["請問您要預訂幾間房間?"],

    "Roomnumconfirmed": ["已完成房間的預訂"+"@@@"+"您預訂的是"+session['hotelname']+
                        "。   入住日期為: "+session["date"]+"。   房間數量為: "+session["number"]+"。"],

    "CallingCar" :['好的，請告訴我您的"起點"(或所在位置) 與 預計到達的"終點"(目的地)。'] ,

    "Confirmpassenger" :["請問共有幾位乘客呢?"] ,

    "Confirmdate" : ["接著請告訴我乘坐日期。"] ,

    "Confirmtrain" : [""],

    "TrainConfirmed" : ["已完成 "+session['number']+"車次 的預定。"] ,

    "CallingConfirmed" : ['已完成叫車，您將從\"'+loc1+'\" 到達\"'+loc2+'\"，請於十分鐘後至'+loc1+'搭乘。'],

    "EatingService" : [''],

    "Getrestaurantinfo" : ['好的以下是'+session["restaurantname"]+"的詳細聯絡資訊。@@@"] ,

    "Getrestaurantlist" : ['restaurantlist'],

    "Bookingtrain" : ['好的，請問您要從哪裡到哪裡呢? 請告訴我"起點車站"和"到達車站"。'] ,

    "NotDefined" : ['']

    }
 

    reponsetext = StringBuilder()

    reponsetext.Append(responseDict[intent][0])


############################################需要資料庫或其他資料的部分###############################################

    if intent == 'EatingService':

        result = session['queryResult']

        reponsetext.Append("為您推薦幾家網路評分較高的餐廳<p><p>")

        for i in range(2) :

            # print("店名: "+result[i]['name'])
            reponsetext.Append("店名: "+result[i]['name']+"(網路評分: "+result[i]['rating']+") <p><p>")

        reponsetext.Append("@@@請問需要為您提供哪間店的聯絡資訊嗎?&nbsp;或是您有其他想去的店嗎? 請告訴我店名。")


    elif intent == 'Getrestaurantinfo':

        reponsetext.Append("店名: "+session['restaurantname']+"<p><p>地址: "+session['restaurantinfo']['address']+"<p>電話: "+session['restaurantinfo']['phone'])

    elif intent == "Confirmtrain" :

        timetable = session['queryResult']

        reponsetext.Append("車次&nbsp;&nbsp;&nbsp;出發時間&nbsp;&nbsp;&nbsp;到達時間<p><p>")

        # print(timetable)
        for row in timetable:

            reponsetext.Append(row['Train_Code']+"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+row['From_Departure_Time']+"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+row['To_Arrival_Time']+"<p><p>")

        reponsetext.Append("@@@請告訴我您所要預訂的車次。")

##########################################################################################################

    if intent == "Bookingtrain" and session['context'] == 'Confirmdate':

        reponsetext = StringBuilder()
        reponsetext.Append("無指定的班次，請重新輸入條件@@@")
        reponsetext.Append('請問您要從哪裡到哪裡呢? 請告訴我"起點車站"和"到達車站"。')

    elif intent == "NotDefined":

        if session['context'] == 'None':

            reponsetext.Append("不好意思，我不瞭解您的意思，或本系統未提供此服務，你重新說明您的需求。")
            reponsetext.Append("@@@")
            reponsetext.Append("本系統目前提供 叫車 、訂車票 、訂飯店和預定(查詢)餐廳 的服務。")
            reponsetext.Append("@@@")
            reponsetext.Append("請問需要什麼服務呢??")
        

        elif session['context'] == "Bookinghotel":
            reponsetext.Append("不好意思，我不瞭解您的意思，或查詢不到您所要的"+session['hotel'])
            reponsetext.Append("@@@")
            reponsetext.Append("再次跟您確認，您所要預訂的"+session['hotel']+"名稱是?")

        elif session['context'] == "Confirmhotel":

            reponsetext.Append("不好意思，我不瞭解您的意思")
            reponsetext.Append("@@@")
            reponsetext.Append("您要預訂的是\""+session['hotelname']+"\"嗎?")

        elif session['context'] == "truehotel":

            reponsetext.Append("不好意思，我不瞭解您的意思")
            reponsetext.Append("@@@")
            reponsetext.Append("請問預計的入住日期是?")

        elif session['context'] == "Dateconfirmed":

            reponsetext.Append("不好意思，我不瞭解您的意思，請輸入正確的數字")
            reponsetext.Append("@@@")
            reponsetext.Append("請問您要預訂幾間房間?")

        elif session['context'] == "CallingCar":

            reponsetext.Append("不好意思，我不瞭解您的意思，或無法判斷您所輸入的起點或目的地")
            reponsetext.Append("@@@")
            reponsetext.Append('請告訴我您的"起點"(或所在位置) 與 預計到達的"終點"(目的地)。')    

        elif session['context'] == "Confirmpassenger":

            reponsetext.Append("不好意思，我不瞭解您的意思，請輸入正確的數字")
            reponsetext.Append("@@@")
            reponsetext.Append("請問共有幾位乘客呢?")

        elif session['context'] == "EatingService":

            reponsetext.Append("不好意思，我不瞭解您的意思，請輸入正確的店名。")

        elif session['context'] == "Bookingtrain":

            reponsetext.Append("不好意思，我不瞭解您的意思，或無法判斷您所輸入的站名。")    
            reponsetext.Append("@@@")
            reponsetext.Append('請告訴我"起點車站"和"到達車站"。')    

        elif session['context'] == "Confirmdate":

            reponsetext.Append("不好意思，我不瞭解您的意思，請您輸入正確的日期。")    

        elif session['context'] == "Confirmtrain":

            reponsetext.Append("不好意思，我不瞭解您的意思，請您輸入正確的車次。") 

    elif intent in endingIntent:
        
        reponsetext.Append("@@@")
        reponsetext.Append("請問您還需要什麼服務呢??")
        reponsetext.Append("@@@")
        reponsetext.Append("本系統目前提供 叫車 、訂車票 、訂飯店和預定(查詢)餐廳 的服務。")



    cursor.close()
    conn.close()
    
    return reponsetext.__str__()

