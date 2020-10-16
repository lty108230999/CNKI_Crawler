import requests
from bs4 import BeautifulSoup
import re
import time
import csv
import random
csv_file = open('引文.csv','a',encoding = 'utf-8',newline = '')
writer = csv.writer(csv_file)
writer.writerow(['title','target_reference','target_refered'])
A = 1
url_index = 'https://kns.cnki.net/kns/request/CustomizeOperate.aspx'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
cabbage = open('网页架构.txt','r',encoding = 'utf-8')
url_new = 'https://kns.cnki.net/KCMS/detail/detail.aspx?'
number = 1
raw = cabbage.read()
soup = BeautifulSoup(raw,'html.parser')
bow = soup.find_all('a',class_='fz14')
quest_count = 1
for i in bow:
    print('当前第'+str(quest_count)+'条')
    quest_count += 1
    title = i.text
    leaf = i['href']
    dbcode = re.search('(?i)dbcode=.*?&',leaf).group()
    dbcode = re.sub(r'(?i)dbcode=','',dbcode)
    dbcode = re.sub(r'&','',dbcode)


    filename = re.search('(?i)filename=.*?&',leaf).group()
    filename = re.sub(r'(?i)filename=','',filename)
    filename = re.sub(r'&','',filename)
    
    dbname = re.search('(?i)dbname=.*?&',leaf).group()
    dbname = re.sub(r'(?i)dbname=','',dbname)
    dbname = re.sub(r'&','',dbname)

    '''print(dbcode)
    print(filename)
    print(dbname)'''
    data = {
            'dbcode':dbcode,
            'filename': filename,
            'dbname': dbname,
            'RefType': '1',
            'vl': '',
            'CurDBCode': dbcode,
            'page': '1'
        }
    res = requests.get(url_new,headers = headers,data = data)
    t = random.uniform(0.5,9.0)
    time.sleep(t)
    soup = BeautifulSoup(res.text,'html.parser')
    try:
        number_article = int(soup.find('div',class_='essayBox').find('div',class_='dbTitle').find('span').text)
    except:
        number_article = 10
    if (number_article%10) == 0:
        number = number_article//10
    else:
        number = number_article//10 + 1

    target_reference = ''
    for i in range(1,int(number)+1):
        url_reference = url_new+'dbcode='+dbcode+'&filename='+filename+'&dbname='+dbname+'&Reftype=1&vl='+'&page='+str(i)
        print(url_reference)
        res = requests.get(url_reference,headers = headers,)
        t = random.uniform(1.5,4.0)
        time.sleep(t)
        try:
            soup = BeautifulSoup(res.text,'html.parser')
            target = soup.find_all('li')
            reference = []
        except:
            print('【该文章尚无引用信息】')
        count = 1
        for i in target:
            countnumber = '['+str(count)+']'
            f = open('摘录.txt','w+',encoding = 'utf-8')
            k = i.text
            k = re.sub('  ','',k)
            k = re.sub('    ','',k)
            k = re.sub('  ','',k)
            k = re.sub('         ','',k)
            k = re.sub('\n','',k)
            k = re.sub(' \n','',k)
            k = re.sub(', ',',',k)
            f.write(k)
            f.close()
            ff = open('摘录.txt','r',encoding = 'utf-8')
            kk = ff.read()
            kk = kk.replace('.\n','.')
            kk = kk.replace('\n.','.')
            kk = kk.replace(']\n',']')
            kk = re.sub('[a-z]\n','',kk)
            kk = re.sub('\n\n','\n',kk)
            kk = re.sub(',\n',',',kk)
            kk = re.sub('\n,',',',kk)
            kk = re.sub(r'\[\d\]',countnumber,kk)
            ff.close()
            reference.append(kk)
            count +=1
        for i in reference:
            target_reference =  target_reference + i.strip() + '\n'

    print(title)
    print('【该文章的参考文献：】')
    print(target_reference)
    target_refered='【该文章尚无被引信息】'
    try:
        url_refered = url_new+'filename='+filename+'&dbcode='+dbcode+'&dbname='+dbname+'&reftype=3&catalogId=lcatalog_YzFiles&catalogName='+'&CurDBCode='+dbcode+'&page=1'
        res = requests.get(url = url_refered,headers = headers)
        soup = BeautifulSoup(res.text,'html.parser')
        number_article = int(soup.find('div',class_='essayBox').find('div',class_='dbTitle').find('span').text)
        if (number_article%10) == 0:
            number = number_article//10
        else:
            number = number_article//10 + 1
        print('【引用该文章的文献】：')
        refered = []
        for i in range(1,int(number)+1):
            url_raw = url_new
            url_newnew = url_raw+'filename='+filename+'&dbcode='+dbcode+'&dbname='+dbname+'&reftype=3&catalogId=lcatalog_YzFiles&catalogName='+'&page='+str(i)
            res = requests.get(url = url_newnew,headers = headers)
            soup = BeautifulSoup(res.text,'html.parser')
            try:
                target_raw = soup.find_all('div',class_='essayBox')
                target = target_raw[0].find('ul').find_all('li')
                for n in target:
                    k = n.text
                    k = re.sub(' ','',k)
                    k = re.sub(' ','',k)
                    k = re.sub('\n','',k)
                    refered.append(k)
                    print(k)
            except:
                target = soup.find('div',class_='essayBox')

                for n in target:
                    k = n.text
                    k = re.sub(' ','',k)
                    k = re.sub(' ','',k)
                    k = re.sub('\n','',k)
                    refered.append(k)
                    print(k)
        t = random.uniform(1.0,3.0)
        time.sleep(t)
        try:            
            url_raw = 'https://kns.cnki.net/kcms/detail/frame/list.aspx?'
            url_newnew = url_raw+'filename='+filename+'&dbcode='+dbcode+'&dbname='+dbname+'&reftype=3&catalogId=lcatalog_YzFiles&catalogName='+'&CurDBCode='+dbcode
            res = requests.get(url = url_newnew,headers = headers)
            soup = BeautifulSoup(res.text,'html.parser')
            target_raw = soup.find_all('div',class_='essayBox')
            for i in target_raw[1:len(target_raw)]:
                target = i.find_all('li')
                for n in target:
                    k = n.text
                    k = re.sub(' ','',k)
                    k = re.sub(' ','',k)
                    k = re.sub('\n','',k)
                    refered.append(k)
                    print(k)
        except:
            print('【该文章尚无硕博论文被引信息】')
        refered_count = 1
        refered2 = []
        for m in refered:
            countnumber2 = '['+str(refered_count)+']'
            m = re.sub(r'\[\d\]',countnumber2,m)
            refered2.append(m)
            refered_count += 1
        target_refered=''
        for i in refered2:
            target_refered =  target_refered + i.strip() + '\n'
    except:
        print('【该文章尚无被引信息】')
    print('----------------------')



    try:
        writer.writerow([title,target_reference,target_refered])
        print('已写入1')
    except:
        writer.writerow([title,target_reference,'【该文章尚无被引信息】'])
        print('已写入2')
    '''except:
        writer.writerow([title,'【该文章尚无引用信息】','【该文章尚无被引信息】'])'''
csv_file.close()
cabbage.close()
