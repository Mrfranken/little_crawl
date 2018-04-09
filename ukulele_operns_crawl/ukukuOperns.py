# -*- coding:utf8 -*-
# import re
# import requests
# import sys
# import threading
# reload(sys)
# import time
# import Queue
# import os
# import random
# from multiprocessing import Pool
# from requests import exceptions
# import multiprocessing
# sys.setdefaultencoding( "utf-8" )
#
# link_list = []
# name_list = []
# error_link = []
# queue = Queue.Queue()
# # 定义一个类，同时初始化一些参数；定义一个方法用来获取谱子的link和对应的name
# class GetOpernsFromNet(object):
#     def __init__(self):
#         self.hosturl = "http://www.yinyuezj.com/ukulele/pu/1000.html"
#         self.url_prefix = "http://www.yinyuezj.com"
#
#     #获取主页面中曲子对应的link
#     def getLinkAndNameFromHostUrl(self,hostrul):
#         host_htmll = requests.get(hostrul).content
#         host_html = host_htmll.decode("gbk")  # 这个位置很关键
#
#         pattern = re.compile('<li>.*?<a href="(.*?)".*?">(.*?)</a></li>')
#         list = re.findall(pattern, host_html)
#
#         current_path = os.getcwd()
#         print current_path
#         file_path = current_path + '\\' + 'songsinfo.txt'
#
#         with open(file_path, 'w') as f:
#             for i in list:
#                 link_list.append(i[0])  # 存储歌曲的link
#                 name_list.append(i[1])  # 存储歌曲的name
#                 f.write(i[1] + ' ' + i[0] + '\n')
#
#     def getOpernsFromLink(self,url_prefix):
#         completeLink = [] #谱子链接的完整列表
#         for numberOfOperns in range(len(link_list)): #这里是所有谱子的链接
#             completeLink1 = url_prefix + link_list[numberOfOperns] #得到谱子所在页面的url,其中link_list为url的一段
#             completeLink.append(completeLink1)
#             queue.put(completeLink1)
#         print len(completeLink)
#         return completeLink
#
#
# def save_to_local_disk(link_content):
#     try:
#         prefix_link_html = requests.get(link_content)
#         status_code = prefix_link_html.status_code
#         link_htmll = prefix_link_html.content
#         if status_code == 200:
#             link_html = link_htmll.decode("gbk")  # 注意要观察网页使用的编码格式
#             pattern = re.compile('<img border.*?src="(.*?)".*?"(.*?)" id="bigimg">')  # 拿到正则表达式
#             pics_list = re.findall(pattern, link_html)  # 第一个元素为pic的link，第二个为pic的名字
#             getPicsAndWriteToLocaldisk(pics_list)
#         elif status_code == 404:
#             print 'status_code == 404'
#     except exceptions.HTTPError as e:
#         # print '这里出现错误: ' + str(e.code)
#         print '=========' + link_content + '============' + 'status_code' + str(status_code)
#
# def getPicsAndWriteToLocaldisk(pics_list):
#     for i in range(len(pics_list)):
#         link = pics_list[i][0] #谱子图片的链接
#         pic_name = pics_list[i][1] #谱子图片的名字
#         pic_name = pic_name.encode('utf-8')
#
#         if '/' in pic_name:
#             pic_name = re.sub('/', ' ', pic_name)
#         elif '\\' in pic_name:
#             pic_name = re.sub(r'\\', ' ', pic_name)
#
#         tody = time.strftime('%Y%m%d')  # 一个路径
#         tody_time = time.strftime('%H%M%S')  # 一个字符串，用作文件名
#
#         if not os.path.exists('D:\ukulele1'):
#             os.mkdir('D:\ukulele1')
#
#         filename = r'D:\ukulele1\\' + pic_name + tody + tody_time+ r'.jpg'
#         try:
#             r = requests.get(link)
#             status_code = r.status_code
#             if status_code == 404:
#                 print 'status_code == 404'
#                 return
#             print link
#             pic_content = r.content
#             with open(unicode(filename, 'utf-8'), 'wb') as f:
#                 f.write(pic_content)
#
#         except exceptions.ConnectionError as e:
#             print 'error happend1' + str(e.code)
#         except exceptions.HTTPError as e:
#             print 'error happend2' + str(e.code)
#         # 将内容写入文件
#
#
# if __name__ == '__main__':
#     print time.strftime('%H%M%S')
#     newObject = GetOpernsFromNet()
#     newObject.getLinkAndNameFromHostUrl(newObject.hosturl)
#     completeLink = newObject.getOpernsFromLink(newObject.url_prefix)
#     pool = multiprocessing.Pool(processes=6) #设定进程池中的运行进程数为6个,每次有进程运行完再进行补充
#     # for link_content in completeLink:
#     #     if completeLink.index(link_content) != 17:
#     #         pool.apply_async(save_to_local_disk,(link_content,)) #非阻塞进程池
#     i = 0
#     while True:
#         i += 1
#         if not queue.empty():
#             link_content = queue.get()
#             pool.apply_async(save_to_local_disk, (link_content,))
#         else:
#             break
#
#     pool.close()
#     pool.join() #进程池中进程执行完毕后再关闭，如果注释，那么程序直接关闭
#     print time.strftime('%H%M%S')




# -*- coding:utf8 -*-
import re
import requests
import sys
from threading import Thread,Condition
import time
import os
from multiprocessing import Pool
from queue import Queue
import multiprocessing
sys.setdefaultencoding( "utf-8" )

link_list = []
name_list = []
queue = Queue()
conditon = Condition()

a = 0
# 定义一个类，同时初始化一些参数；定义一个方法用来获取谱子的link和对应的name
class GetOpernsFromNet:
    def __init__(self):
        self.hosturl = "http://www.yinyuezj.com/ukulele/pu/1000.html"
        self.url_prefix = "http://www.yinyuezj.com"

    #获取主页面中曲子对应的link
    def getLinkAndNameFromHostUrl(self,hostrul):
        global a
        host_htmll = requests.get(hostrul).content
        host_html = host_htmll.decode("gbk")  # 这个位置很关键

        pattern = re.compile('<li>.*?<a href="(.*?)".*?">(.*?)</a></li>')
        list = re.findall(pattern, host_html)

        current_path = os.getcwd()
        print(current_path)
        file_path = current_path + '\\' + 'songsinfo.txt'

        with open(file_path, 'w') as f:
            for i in list:
                link_list.append(i[0])  # 存储歌曲的link
                name_list.append(i[1])  # 存储歌曲的name
                f.write(i[1] + ' ' + i[0] + '\n')

    def getOpernsFromLink(self,url_prefix):
        completeLink = [] #谱子链接的完整列表
        for numberOfOperns in range(len(link_list)): #这里是所有谱子的链接
            completeLink1 = url_prefix + link_list[numberOfOperns] #得到谱子所在页面的url,其中link_list为url的一段
            completeLink.append(completeLink1)
            queue.put((completeLink1))
        print(len(completeLink))
        return completeLink



class MutipleThreadsToDownLoadPics(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        global queue
        while not queue.empty():
            link_content = queue.get()
            conditon.acquire()
            print(link_content)
            conditon.release()
            self.save_to_local_disk(link_content)


    def save_to_local_disk(self,link_content):
        # pass
        try:
            link_htmll = requests.get(link_content,timeout=5).content
            link_html = link_htmll.decode("gbk")  # 注意要观察网页使用的编码格式
            pattern = re.compile('<img border.*?src="(.*?)".*?"(.*?)" id="bigimg">')  # 拿到正则表达式
            pics_list = re.findall(pattern, link_html)  # 第一个元素为pic的link，第二个为pic的名字
            self.getPicsAndWriteToLocaldisk(pics_list)
        except:
            # pass
            # print '这里出现错误: ' + link_content
            a =+ 1
            print(a)
            if a<=1000:
                queue.put(link_content)
            else:
                pass

    def getPicsAndWriteToLocaldisk(self,pics_list):
        for i in range(len(pics_list)):
            link = pics_list[i][0] #谱子图片的链接
            pic_name = pics_list[i][1] #谱子图片的名字
            # print link
            pic_name = pic_name.encode('utf-8')

            if '/' in pic_name:
                pic_name = re.sub('/', ' ', pic_name)
            elif '\\' in pic_name:
                pic_name = re.sub(r'\\', ' ', pic_name)

            tody = time.strftime('%Y%m%d')  # 一个路径
            tody_time = time.strftime('%H%M%S')  # 一个字符串，用作文件名

            filename = r'D:\ukulele3\\' + pic_name + tody + tody_time + r'.jpg'
            # filename = filename.encode('utf-8')

            r = requests.get(link, timeout=5).content
            # 将内容写入文件
            with open(filename,'wb') as f:
                f.write(r)

if __name__ == '__main__':
    print(time.strftime('%H%M%S'))
    newObject = GetOpernsFromNet()
    newObject.getLinkAndNameFromHostUrl(newObject.hosturl)
    completeLink = newObject.getOpernsFromLink(newObject.url_prefix)
    thread_list = []

    for nums in range(5):
        childthread = MutipleThreadsToDownLoadPics()
        childthread.start()
        thread_list.append(childthread)

    for thread in thread_list:
        thread.join()


    print(time.strftime('%H%M%S'))


