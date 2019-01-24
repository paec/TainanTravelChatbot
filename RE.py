import re
 
date_pattern = re.compile(r'(?:[12]\d{3}(?:-|/|年))*((?<!\d)0{0,1}[1-9]|(?<!\d)1[0-2])(?:-|/|月)(0{0,1}[1-9]|[12]\d|3[01])(?!\d)(?:日|號)*') 
num_pattern = re.compile(r'(\d+|[一二三三四五六七八九十]+)')
# date_pattern =re.compile(r'([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))')

if __name__ == '__main__':

    result1 = date_pattern.findall('12/12')
    
    match = date_pattern.search('120/12')

    print(match)

    if match:
        
        result = "2019-"+match.group(1)+"-"+match.group(2)

        print(result)


