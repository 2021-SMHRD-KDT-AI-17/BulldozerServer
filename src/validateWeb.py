from src import wordList as wl


def validate(extractWords):
    print("extractWords")
    single_list = []
    available=0
    for sublist in extractWords:
        single_list.extend(sublist)
        available+=1
    wdict=wl.getWordDict()
    cnt_h=0
    cnt_m=0
    cnt_l=0
    print(single_list)
    for word in single_list:
        if word in wdict:
            if wdict[word] == '상':
                cnt_h += 1
            elif wdict[word] == '중':
                cnt_m += 1
            elif wdict[word] == '하':
                cnt_l += 1
    
    res=False
    if available>0:
        if (available <= cnt_h * 3)or(cnt_m > cnt_h and cnt_m >=available)or(cnt_l>cnt_m and cnt_l>cnt_h and cnt_h>=available):
            res=True
    print(f"이미지 개수 :{available} 상:{cnt_h} 중:{cnt_m} 하:{cnt_l} 유해사이트:{res}")
    return res

def validateAlone(extractWords):
    print("extractWords")
    single_list = []
    available=0
    for sublist in extractWords:
        if len(sublist)!=0:
            single_list.extend(sublist)
            available+=1
    wdict=wl.getWordDict()
    cnt_h=0
    cnt_m=0
    cnt_l=0
    print(single_list)
    for word in single_list:
        if word in wdict:
            if wdict[word] == '상':
                cnt_h += 1
            elif wdict[word] == '중':
                cnt_m += 1
            elif wdict[word] == '하':
                cnt_l += 1
    
    res=False
    if (available <= cnt_h * 3)or(cnt_m > cnt_h and cnt_m >=available)or(cnt_l>cnt_m and cnt_l>cnt_h and cnt_h>=available):
        res=True
    print(f"이미지 개수 :{available} 상:{cnt_h} 중:{cnt_m} 하:{cnt_l} 유해사이트:{res}")
    return res