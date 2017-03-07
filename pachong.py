import requests
import urllib
import time
from lxml import etree
from multiprocessing import Pool

header={
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding':'gzip,deflate',
'Accept-Language':'zh-CN',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Cookie':'Hm_lvt_fd93b7fb546adcfbcf80c4fc2b54da2c=1484955754,1485044689,1485130508,1485826401; _ga=GA1.2.1961886334.1477279934; comment_author_01b0531fab6a989460dd1b231010b496=%E6%98%9F%E5%B0%98; comment_author_email_01b0531fab6a989460dd1b231010b496=xc%40xcexe.com; jdna=01b0531fab6a989460dd1b231010b496#1488328794145',
'Host':'jandan.net',
'Referer':'http://jandan.net/',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2146.0 Safari/537.36',
'X-DevTools-Emulate-Network-Conditions-Client-Id':'E61E38FD-4ECB-44C0-8706-33450F2B1BAD'
}

#获取网页内容
def getcontent(url,headers):
        s=requests.session()
        z=s.get(url,headers=header)
        print("获取网页内容成功=="+str(z.status_code))
        return z
#获取图片地址及oo数大于200的图片url
def  getimgurl(content):
        no=etree.HTML(content.content).xpath('//div[@class="text"]/span/a/text()')
        num=len(no)
        imgurls=[]
        #获取ooxx数量及比例
        for num in no:
            idoo="//span[@id='cos_support-"+str(num)+"']/text()"
            idxx="//span[@id='cos_unsupport-"+str(num)+"']/text()"
            id="//li[@id='comment-"+str(num)+"']//a[@class='view_img_link']/@href"
            oo_num=etree.HTML(content.content).xpath(idoo)
            xx_num=etree.HTML(content.content).xpath(idxx)
            if int(oo_num[0])>=200 and int(oo_num[0])>int(xx_num[0]):
                imgurl=etree.HTML(content.content).xpath(id)
                for i in imgurl:
                    imgurls.append(i)
        print("图片地址获取成功,共"+str(len(imgurls))+"张")
        return imgurls
#下载图片
def  saveimg(url,num,page):
        url="http:"+url 
        try:
                filename="img\img"+str(page)+"-"+str(num)+url[len(url)-4:len(url)]
                print('开始下载'+filename)   
                opener=urllib.request.build_opener()
                opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
                urllib.request.install_opener(opener)               
                urllib.request.urlretrieve(url,filename)
                time.sleep(2)
                return 1
        except Exception as e:
                print (str(e)+"下载出错，重新下载！")
                try:
                    urllib.request.urlretrieve(url,filename)
                except Exception as e:
                    print(str(e)+"下载再次出错，终止！")

#批量下载，控制页码
'''
for page in range(2315,2317):
    num=0
    url="http://jandan.net/ooxx/page-"+str(page)
    _z=getcontent(url,header)
    _imgurls=getimgurl(_z)
    for imgurl in _imgurls:
        num=num+1
        saveimg(str(imgurl),num,page)
    print("第",page,"页，已下载")

print("程序结束")'''

if __name__=='__main__':
    try:
        for page in range(2320,2360):
            p=Pool(5)
            num=0
            url="http://jandan.net/ooxx/page-"+str(page)
            _z=getcontent(url,header)
            _imgurls=getimgurl(_z)
            
            for imgurl in _imgurls:
                num=num+1
                p.apply_async(saveimg,args=(str(imgurl),num,page,))
            p.close()
            p.join()
            time.sleep(10)
            print("第",page,"页，已下载")
    except Exception as e:
        print("多进程异常->",e)
print("程序结束")
