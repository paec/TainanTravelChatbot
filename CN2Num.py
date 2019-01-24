import re
digit = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}

def _trans(s):

    num = 0
    if re.search(r"\d+",s):

        return s

    elif s:
        idx_q, idx_b, idx_s = s.find('千'), s.find('百'), s.find('十')

        if idx_q != -1:
            num += digit[s[idx_q - 1:idx_q]] * 1000

        if idx_b != -1:
            num += digit[s[idx_b - 1:idx_b]] * 100

        if idx_s != -1:
            num += digit.get(s[idx_s - 1:idx_s], 1) * 10

        if s[-1] in digit:
            num += digit[s[-1]]

    return str(num)

if __name__ == '__main__':
    
    cn  = _trans("五十")
    print(cn)