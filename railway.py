from bs4 import BeautifulSoup
import json
import requests
import codecs
import re

# open station code file
with codecs.open(".\\railway_crawler\\station.json", 'r', encoding='utf-8') as reader:
  jf = json.load(reader)


def getTimetable(ssn,asn,date,time):

  # four input : 起點, 終點, 日期, 時間
  startStationName = ssn
  arriveStationName = asn
  date = date
  time = "0000"


  #find station code
  for i in range(len(jf)):
    if jf[i]["name"] == startStationName:
      startStationNum = jf[i]["id"]
    if jf[i]["name"] == arriveStationName:
      arriveStationNum = jf[i]["id"]


  #post data
  form_data = {
    #"FromCity": "9",
    "FromStation": startStationNum,
    "FromStationName": "0",
    #"ToCity": "18",
    "ToStation": arriveStationNum,
    "ToStationName": "0",
    "TrainClass": "2",
    "searchdate": date,
    "FromTimeSelect": time,
    "ToTimeSelect": "2359",
    "Timetype": 1
  }

  res = requests.post("http://twtraffic.tra.gov.tw/twrail/TW_SearchResult.aspx", data= form_data)
  soup = BeautifulSoup(res.text, "lxml")

  try:

    timetable = soup.find_all("script")[11].text.replace(";","").replace("var JSONData=","")

    print(timetable)
    timetable = json.loads(timetable)

    # temp = re.split(":|,", a)

    print("起點:", startStationName, "終點:", arriveStationName, "日期:", date, "時間:", time)
    # print("\n")
    print("車次   出發時間   到達時間")



    for row in timetable:

      print(row['Train_Code'],"   ",row['From_Departure_Time'],"   ",row['To_Arrival_Time']) 
      # print(row)

    #show 出最接近的3個班次
  #   print("起點:", startStationName, "終點:", arriveStationName, "日期:", date, "時間:", time)
  #   print("車次: ", temp[1], "出發時間: ", temp[31], "抵達時間: ", temp[33])
  #   print("車次: ", temp[54], "出發時間: ",  temp[84], "抵達時間: ", temp[86])
  #   print("車次: ", temp[106], "出發時間: ",  temp[136], "抵達時間: ", temp[138])
    return timetable
    

  except Exception as e:

    return "notrain"
    print(e)

  


if __name__ == '__main__':

  a = getTimetable("台南","沙崙","2019-1-22","0000")
  print(a)
  print(a)