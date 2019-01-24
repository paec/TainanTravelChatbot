import os 
from fuzzywuzzy import fuzz
import privateInfo

# with open("jieba\\"+"restaurantname.txt","r",encoding="utf8") as r:

#             restaurantname = ""
#             maxscore = 0 

#             restaurantlist = r.read().splitlines()
            
#             for r in restaurantlist:

#                 score = fuzz.ratio("牛肉湯", r)

#                 if score>0:

#                     print(r)        
#                     print(score)

    

result = "123".find("13")

print(result)

# with open("jieba\\"+"wrtie.txt","r+") as w:

#     list = w.readlines()

#     with open("jieba\\"+"taiwanrailway.txt","r+") as r :

#         for l in list:
#             r.write(l)


# print(privateInfo.mysqlaccount.ip)