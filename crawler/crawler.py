import requests
import re
import time
from bs4 import BeautifulSoup
requests.packages.urllib3.disable_warnings()
import csv
start_time = time.time()
for page in range(3334,3336):                                               #網址的頁數
    article_href = []
    url = 'https://www.ptt.cc/bbs/Beauty/index'+str(page)+'.html'           #要爬的正妹版網址
    payload = {
                'form':'/bbs/stock/Beauty.html',
                'yes':'yes'
              }                                           #派出爬蟲的時間
    rs=requests.session()
    res=rs.post('https://www.ptt.cc/ask/over18',verify=False,data=payload)  #通過滿18歲認證
    res=rs.get(url,verify=False)                                            #取得HTML頁面
    soup = BeautifulSoup(res.text,"html.parser")                            #將抓回的HTML頁面傳入BeautifulSoup，使用html.parser解析
    result = soup.select("div.title")                                       #找到網頁中全部的 <div class="title">

    for item in result:                                                     #取得所有連結 存在article_href裡
        try:
            item_href = item.select_one("a").get("href")
            article_href.append(item_href)
           # print(article_href)                                         
        except:
            continue;

    for pcontent in range(len(article_href)):           
        payload = {
                    'form':article_href[pcontent],
                    'yes':'yes'
                  }
        rs=requests.session()
        res=rs.post('https://www.ptt.cc/ask/over18',verify=False,data=payload)
        res = rs.get('https://www.ptt.cc'+article_href[pcontent],verify=False,data=payload)
        soup = BeautifulSoup(res.text, "html.parser")
        result1=soup.select('span.f2')                                      #IP在<span class="f2"裡
        results = soup.select('span.article-meta-value')                    #作者, 標題, 時間都在<span class="article-meta-value"裡
    
        
        if "Mon Jun 22"  in results[3].text:
            if "正妹" in results[2].text.split(" ")[0]:
                print("---------------------------------------------------------")
                print("標題:",results[2].text)
                print("作者:",results[0].text)
                print("時間:",results[3].text) 
                print("IP:",result1[0].text.split("來自:")[1])
                imgLinks = soup.findAll('a',{'href':re.compile('https:\/\/(imgur|i\.imgur)\.com\/.*.jpg$')}) #爬出所有的照片網址
                if len(imgLinks)>0:
                   try:
                        for imgLink in imgLinks:
                            print ("第一張圖片網址:",imgLink['href'])
                            print()
                            break                                            #print出第一張就結束迴圈
                   except Exception as e:
                       print(e)       
                g=0                                                         #推數
                b=0                                                         #噓數
                n=0                                                         #→ 數
                for tag in soup.select('div.push'):                         #推,噓,→ 都在<div class"push"裡
                    push_tag = tag.find("span", {'class': 'push-tag'}).text
                    #print ("push_tag:",push_tag)
                    if push_tag == u'推 ':
                        g += 1
                    elif push_tag == u'噓 ':
                        b += 1
                    else:
                        n += 1
                print("推文總數:",g)
                print("噓文總數:",b)
                print ('execution time:' + str(time.time() - start_time)+'s') #執行爬蟲的時間 
                #匯出 csv檔 
                with open('正妹.csv', mode='a',encoding="utf-8") as csv_file:
                    fieldnames = ['作者','標題','時間','第一張圖片網址','推文總數','噓文總數','爬蟲爬取之時間','po文IP']
                    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                    writer.writerow({'作者':results[0].text,'標題':results[2].text,'時間':results[3].text,'第一張圖片網址':imgLink['href'],'推文總數':g,'噓文總數':b,'爬蟲爬取之時間':str(time.time() - start_time)+'s','po文IP':result1[0].text.split("來自:")[1]})
                    
                print("---------------------------------------------------------") 
        
                
            elif "帥哥" in results[2].text.split(" ")[0]:
                print("---------------------------------------------------------")
                print("標題:",results[2].text)
                print("作者:",results[0].text)
                print("時間:",results[3].text) 
                print("IP:",result1[0].text.split("來自:")[1]) 
                imgLinks = soup.findAll('a',{'href':re.compile('https:\/\/(imgur|i\.imgur)\.com\/.*.jpg$')})
                if len(imgLinks)>0:
                   try:
                        for imgLink in imgLinks:
                            print ("第一張圖片網址:",imgLink['href'])
                            print()
                            break
                   except Exception as e:
                       print(e)       
                g=0
                b=0
                n=0
                for tag in soup.select('div.push'):
                # push_tag  推文標籤  推  噓
                    push_tag = tag.find("span", {'class': 'push-tag'}).text
                    #print ("push_tag:",push_tag)
                    if push_tag == u'推 ':
                        g += 1
                    elif push_tag == u'噓 ':
                        b += 1
                    else:
                        n += 1
                print("推文總數:",g)
                print("噓文總數:",b)
                print ('execution time:' + str(time.time() - start_time)+'s')
                print("---------------------------------------------------------")
                #匯出 csv檔 
                with open('帥哥.csv', mode='a',encoding="utf-8") as csv_file:
                    fieldnames = ['作者','標題','時間','第一張圖片網址','推文總數','噓文總數','爬蟲爬取之時間','po文IP']
                    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                    writer.writerow({'作者':results[0].text,'標題':results[2].text,'時間':results[3].text,'第一張圖片網址':imgLink['href'],'推文總數':g,'噓文總數':b,'爬蟲爬取之時間':str(time.time() - start_time)+'s','po文IP':result1[0].text.split("來自:")[1]})

           # else:
                #continue;