import requests
from bs4 import BeautifulSoup
import re
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
A = 1
while A:
    url = input('请完整粘贴网址,要终止请输入666')
    if url != '666':
        number = input('请输入页数')
        f = open('摘录.txt','w+',encoding = 'utf-8')
        url_new = re.match(r'https://.*aspx\?',url).group()
        url_new = re.sub(r'/detail.aspx','/frame/list.aspx',url_new)

        dbcode = re.search('dbcode=.*?&',url).group()
        dbcode = re.sub(r'dbcode=','',dbcode)
        dbcode = re.sub(r'&','',dbcode)


        filename = re.search('filename=.*?&',url).group()
        filename = re.sub(r'filename=','',filename)
        filename = re.sub(r'&','',filename)

        dbname = re.search('dbname=.*?&',url).group()
        dbname = re.sub(r'dbname=','',dbname)
        dbname = re.sub(r'&','',dbname)


        '''data = {
            'dbcode':dbcode,
            'filename': filename,
            'dbname': dbname,
            'RefType': '1',
            'vl': '',
            'CurDBCode': dbcode,
            'page': i
            }'''




        for i in range(1,int(number)+1):
            data = {
            'dbcode':dbcode,
            'filename': filename,
            'dbname': dbname,
            'RefType': '1',
            'vl': '',
            'CurDBCode': dbcode,
            'page': i
            }
            res = requests.get(url_new,headers = headers,data = data)
            soup = BeautifulSoup(res.text,'html.parser')
            target = soup.find_all('li')
            for i in target:
                k = i.text
                k = re.sub(' ','',k)
                k = re.sub(' ','',k)
                k = re.sub('\n','',k)
                f.write(k)
        f.close()     
        ff = open('摘录.txt','r',encoding = 'utf-8')
        kk = ff.read()
        kk = kk.replace('.\n','.')
        kk = kk.replace(']\n',']')
        kk = re.sub('[a-z]\n','',kk)
        kk = re.sub('\n\n','\n',kk)
        kk = re.sub(',\n',',',kk)
        kk = re.sub('\n,','',kk)
        print(kk)
        ff.close()
    else:
        print('程序已接触，要继续请再次运行')
        A=0
        break
