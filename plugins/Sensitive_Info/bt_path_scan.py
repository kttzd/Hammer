#!/usr/bin/python
#coding:utf-8
import re
from dummy import *
import httplib2  #test
import futures
info = {
        'NAME':'bt scan',
        'AUTHOR':'kttzd',
        'TIME':'20141011',
        'WEB':''
}
DIR=[]
ADMIN_DIR=['-admin','2013','_2013','adminer','_admin','2012','_2012','2008','_2008','_system','_sys_admin','admin','2014','system','test','_test','-system','_adminer','-test','info','data','conn','backup','-data','_data','-conn','_conn','_backup','-backup']
def getname(url):
    target=url
    target_url=re.match(r'\w+:\/\/\w+\.(.*?)\.\w+',target).group(1)   #来源于乌云社区
    return target_url
def normal(str):
    for i in range(len(str)):
        newstr=str[0:(i+1)]
        for a in ADMIN_DIR:
            DIR.append(newstr+a)

def bt(target_url):
    newstr=target_url.split('-')
    for item in newstr:
        normal(item)
def test(target_url):
    match=re.search(r'-',target_url)
    if match:
        bt(target_url)
    else:
        normal(target_url)
class btscan():
    def __init__(self,url):
        self.url=url        
    def dirscan(self,dir):
        host=self.url+dir+'/'
        #print host
        h=httplib2.Http(timeout=2)
        try:
            #respone=urllib2.urlopen(host)
            resp,content=h.request(host,"HEAD")
            if resp["status"]=!404:
                secutity_info(host+resp["status"])   #扫到的有趣路径加到里面
        except Exception,e:
            #print e
            pass

def Audit(services):
    if services.has_key('url'):
        url = services['url']
        #print "!!!!!"
        target_url=getname(url)
        test(target_url)    # 这里执行  得到  DIR
        if url[-1]!="/":
            url += "/"
        print url
        bttest=btscan(url)
        
        with futures.ThreadPoolExecutor(max_workers=10) as executor:      #默认10线程
            tasks=dict((executor.submit(bttest.dirscan,dir),dir) for dir in DIR)
            futures.as_completed(tasks)
if __name__=='__main__':
    services = {'url':'http://www.27zg.com'}
    pprint(Audit(services))
