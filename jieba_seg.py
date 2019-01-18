import jieba
import re

# jieba.load_userdict("jieba\\"+"welldict.txt")
jieba.load_userdict("jieba\\"+"chatbotdict.txt")
jieba.load_userdict("jieba\\"+"taiwanrailway.txt")
jieba.load_userdict("jieba\\"+"restaurantname.txt")
jieba.load_userdict("jieba\\"+"hotelname.txt")
jieba.load_userdict("jieba\\"+"locationname.txt")

def jieba_seg(text):
   
    punctuation = "[？\s+\.\!\/_」「,$%?^*(+\"\']+|[+——！，。、~@#￥%……&*（）()]+"

    text = re.sub(punctuation,"", text)

    seg_list = list(jieba.cut(text,cut_all = False))

    return seg_list

if __name__ == '__main__':
    
    print(jieba_seg("台南香格里拉國際大飯店"))

