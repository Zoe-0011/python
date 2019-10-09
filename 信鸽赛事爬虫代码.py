import requests
from bs4 import BeautifulSoup
import bs4
import re
import traceback
session=requests.session()
headers={"User-Agent":"Mozilla/5.0(WindowsNT6.1;rv:2.0.1)Gecko/20100101Firefox/4.0.1",
        }
login_url='http://s.crpa.net.cn/mlogin.aspx'
response=session.get(login_url,headers=headers)
#print(response.text)

captchar_url='http://s.crpa.net.cn/mlogin_img.aspx'
captchar_response=session.get(captchar_url)
with open('captchar.jpg','wb')as f:
    f.write(captchar_response.content)
check_url='http://s.crpa.net.cn/mlogin.aspx'
code=input('请打开左侧jpg图片查看验证码并输入>>>>:')
data={
    '__VIEWSTATE':'/wEPDwULLTEwMjY5MTUwNjVkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYBBQdCdXR0b24xEJ3+btx8o7jW/CSxb/td1tIkmwhXlM8kZMHsvV6nM4U=',
    '__VIEWSTATEGENERATOR':'B0A1EB3C',
    '__EVENTVALIDATION':'/wEdAAOLUZ+aU8smFG3otwTqz4zA9XU/Y71901ANuAMxuQ5LR834O/GfAV4V4n0wgFZHr3eOc6MeBcTZ09DEcUiFPb3HnEU5ij712WvDk26fOylj+A==',
    'txtCheckCode':code,
    'Button1.x':'0',
    'Button1.y':'0',
}
check_response=session.post(check_url,data=data)
needurl='http://s.crpa.net.cn/default.aspx?month=201805'                      #链接去掉'month=101805'或将其改成'month=时间'，如：'month=201804',关键是要与所查询直播平台主页面链接一致。
def gethtmltext(url):
    try:
        r=session.get(url,timeout=30)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        return r.text
    except:
        return ""

def getmainurl(mainhtml,maindic,fpath):
     listh=[]
     listl=[]
     soup=BeautifulSoup(mainhtml,'html.parser')
     table=soup.find('table',attrs={'cellspacing':'0','rules':'all'})
     for tr in table.children:
         if isinstance(tr,bs4.element.Tag):
             try:
                 a = tr.find_all('a')
                 headline = a[0].attrs['href']
                 lastline=a[1].attrs['href']
                 tds = tr.find_all('td')
                 ths = table.find_all('th')
                 for i in range(len(tds)):
                     key=ths[i].text
                     val=tds[i].text
                     maindic[key]=val
                     maindic.update({'头链接': headline, '尾链接': lastline})
                 listh.append(headline)
                 listl.append(lastline)

                 with open(fpath,'a',encoding='utf-8') as f:
                        f.write(str(maindic)+'\n')

             except:
                 continue

     return  listh,listl

def getheadurl(headurl,headdic,fpathhead):
    html=gethtmltext(headurl)
    try:
        soup=BeautifulSoup(html,'html.parser')
        table = soup.find('table', attrs={'cellspacing': '0', 'rules': 'all','bordercolor':'#003366','border':'1','id':'GridView1','bgcolor':'#E3F4D7','width':'970'})
        for tr in table.children:
            if isinstance(tr,bs4.element.Tag):
                try:
                    tds = tr.find_all('td')
                    ths = table.find_all('th')
                    for i in range(len(tds)):
                        key = ths[i].text
                        val = tds[i].text
                        headdic[key] = val
                        headdic.update({'头链接': headurl})
                    with open(fpathhead, 'a', encoding='utf-8') as f:
                            f.write(str(headdic)+'\n')

                except:
                    continue

    except:
        traceback.print_exc()

def getlasturl(lasturl, lastdic, fpathlast,a):
    html = gethtmltext(lasturl)
    try:
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table', attrs={'cellspacing': '0','rules': 'all'})
        for tr in table.children:
            if isinstance(tr, bs4.element.Tag):
                try:
                    tds = tr.find_all('td')
                    ths = table.find_all('th')
                    for i in range(len(tds)):
                        key = ths[i].text
                        val = tds[i].text
                        lastdic[key] = val
                        lastdic.update({'尾链接': lasturl})
                    with open(fpathlast, 'a', encoding='utf-8') as f:
                        f.write(str(lastdic) + '\n')
                except:
                    continue
    except:
        traceback.print_exc()

maindic={}
headdic={}
lastdic={}
fpath='E://main.txt'                     #main、head、last文件的保存路径（首先要在自己电脑任意路径新建空白main.txt文件）
fpathhead='E://head.txt'                 #main、head、last文件的保存路径（同上）
fpathlast='E://last.txt'                 #main、head、last文件的保存路径（同上）
needhtml=gethtmltext(needurl)
a=getmainurl(needhtml,maindic,fpath)
for ll in a[0]:
    headurl='http://s.crpa.net.cn/'+ll
    getheadurl(headurl, headdic, fpathhead)
for ll in a[1]:
    print(ll)
    lasturl = 'http://s.crpa.net.cn/' + ll
    getlasturl(lasturl, lastdic, fpathlast,a)














