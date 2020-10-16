import re
import xlrd

def xlsx_read(f):   
    wb = xlrd.open_workbook(filename = f)
    sheet1 = wb.sheet_by_index(0)
    cols = sheet1.col_values(1)
    cols2 = sheet1.col_values(0)
    refer = cols
    art_title = cols2
    return refer,art_title

def check_contain_chinese(check_str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


def CN_spliter(k):
    info = {}
    try:
        title = re.search(r'\].*?\[',k)[0]
        title = title.replace('[','')
        title = title.replace(']','')
        title = title.replace('.','')
        kind = re.search(r'\[[A-Z]\]',k)[0]
        kind = kind.replace('[','')
        kind = kind.replace(']','')
    except:
        title = re.search(r'\].*?\.',k)[0]
        title = title.replace('[','')
        title = title.replace(']','')
        kind = ' '
    if 'J' in kind:
        au = re.search(r'\..*\.',k)[0]
        kk = [x for x in au.split('.') if len(x)> 0]
        authors = kk[0].strip()
        journal = kk[-1]
        time = k[3:-1].replace(title,'').replace(kind,'').replace(authors,'').replace(journal,'').replace('.','').replace('[','').replace(']','').strip()
    elif 'M' in kind:
        journal = re.search(r'\]\..*?,',k)[0].replace(']','').replace(',','').replace('.','')
        index = k.index(journal)
        au = (k+' ')[index+len(journal):-1]
        author = re.search(r',.*,',au)[0]
        authors = author[1:-1].replace('编','').replace('著','')
        time = au.replace(author,'')
    elif 'D' in kind:
        title = re.search(r'\].*\[',k)[0]
        title = title.replace('[','')
        title = title.replace(']','')
        kind = re.search(r'\[[A-Z]\]',k)[0]
        kind = kind.replace('[','')
        kind = kind.replace(']','')
        au = re.search(r'\]\..*\.',k)[0]
        authors = au.replace(']','').replace('.','').strip()
        jou = k.split('.')[-1].strip()
        journal = jou.split(' ')[0]
        try:
            time = jou.split(' ')[1]
        except:
            time = re.search(r'\d\d\d\d',jou).group()

    else:
        au = re.search(r'\..*\.',k)[0]
        kk = [x for x in au.split('.') if len(x)> 0]
        authors = kk[0].strip()
        journal = kk[-1]
        time = k[3:-1].replace(title,'').replace(kind,'').replace(authors,'').replace(journal,'').replace('.','').replace('[','').replace(']','').strip()
    if len(title) <= 3:
        l = title
        title = authors
        authors = l
    info['title'] = title
    info['kind'] = kind
    info['authors'] = authors
    info['journal'] = journal
    try:
        info['time'] = time.split('(')[0]
        info['period'] = time.split('(')[1]
    except:
        info['time'] = time
        info['period'] =' '
    '''print(title)
    print(kind)
    print(authors)
    print(journal)
    print(time)'''
    return info

def EN_spliter(k):
    info = {}
    cc = k.split('.')
    title = re.sub(r'\[\d*\]','',cc[0])
    authors = cc[1].strip()
    journal = cc[2].strip()
    try:
        kind = re.search(r'\[\w{1}\]',title)[0]
        kind = kind.replace('[','').replace(']','')

    except:
        kind = ' '
    try:
        time = cc[3].strip()
    except:
        time = cc[2].strip()
        authors = ' '
        journal = cc[1].strip()
    title = re.sub(r'\[\w{1}\]','',title)
    info['title'] = title
    info['kind'] = kind
    info['authors'] = authors
    info['journal'] = journal
    try:
        info['time'] = time.split('(')[0]
        info['period'] = time.split('(')[1]
    except:
        info['time'] = time
        info['period'] =' '
    return info
def doc_writer(name,art_title,info):
    f = open(name+'.txt','a',encoding = 'utf-8')
    f.write(art_title+'\t'+info['title']+'\t'+info['kind']+'\t'+info['authors']+'\t'+info['journal']+'\t'+info['time']+'\t'+info['period']+'\n')

def main():
    name = input('输入你的文件名，请新建一个xlsx文件，将第一列放置文献title,第二列放置被引信息')
    fffff = open(name +'排障.txt','a',encoding = 'utf-8')
    refer,art_title = xlsx_read(name+'.xlsx')
    refer.remove(refer[0])
    art_title.remove(art_title[0])
    count = 0
    for a in refer:
        title = art_title[count]
        try:
            a = re.sub(' . \n','.',a)
            b = [x for x in a.split('\n') if len(x)>6]

            for i in b:
                if check_contain_chinese(i) == True :
                    info = CN_spliter(i)
                else:
                    info = EN_spliter(i)
                doc_writer(name,title,info)
        except:
            if i == '【该文章尚无被引信息】':
                pass
            else:
                fffff.write(str(i)+'\n')
        count += 1
main()

