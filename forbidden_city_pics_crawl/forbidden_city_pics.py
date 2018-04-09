import time
import requests
from fake_useragent import UserAgent
import re
from threading import Thread
try:
    from Queue import Queue
except:
    from queue import Queue
'''
这个脚本的运行环境是python2.7，下载了大约7000张图片，但是由于当时下载的时候都是打开
文件直接写入的，这样导致很多的图片都没有内容（然后还有很多图片在下载是报错了的，需要重新
下载，这里我是手动记录下来了，然后在test.py中进行了重新下载），所以在JudgeFileValid.py
这个脚本中多所有的文件都做了可用性的判断，去除了所有无用的图片
'''

class GetNextPageContent(Thread):
    def __init__(self, page_num, queue, ua):
        Thread.__init__(self)
        self._init_page = 1
        self._sum_page_num = page_num + 1
        self._ua = ua
        self.queue = queue
        self._next_page_url = "http://www.dpm.org.cn/searchs/royal/category_id/173/p/{}.html"

    def run(self):
        regex = '<a target.*href="/light/(\d+).html".*?title="(.*?)".*?</a>'
        pattern = re.compile(regex)
        for page_num in range(self._init_page, self._sum_page_num):
            headers = {'User-Agent': self._ua.random}
            html = requests.get(self._next_page_url.format(page_num), headers=headers, timeout=5).content
            groups = re.findall(pattern=pattern, string=html)
            for pic in groups:
                pic_info = (pic[0], pic[1])
                self.queue.put(pic_info)
            time.sleep(3)


class DownLoadPics(Thread):
    def __init__(self, queue, ua):
        global num1
        Thread.__init__(self)
        self.queue = queue
        self._ua = ua
        self.pic_download_url = 'http://www.dpm.org.cn/download/lights_image/id/{}/img_size/{}.html'
        self.download_path = 'D:\\forbidden_city1\\{}{}.jpg'
        self.pic_resolution = {1: 1024.768,
                               2: 1280.800,
                               3: 1680.1050,
                               4: 1920.1080,
                               5: 640.960,
                               6: 640.1136,
                               7: 720.1280,
                               8: 1024.1024,
                               9: 2048.2048}

    def run(self):
        while True:
            pic_info = self.queue.get()
            pic_num = pic_info[0]
            pic_name = pic_info[1]
            self.save_pic_to_local(pic_num, pic_name)

    def save_pic_to_local(self, pic_num, pic_name):
        headers = {'User-Agent': self._ua.random}
        for num in range(1, 10):
            if num % 3 == 0:
                headers = {'User-Agent': self._ua.random}
            try:
                with open(unicode(self.download_path.format(pic_name, self.pic_resolution[num]), 'utf-8'), 'wb') as f:
                    pic_content = requests.get(self.pic_download_url.format(pic_num, num), timeout=2, headers=headers).content
                    f.write(pic_content)
                time.sleep(5)
            except:
                print('there are some problems when download pic {} in {} at url: {}'.format(pic_name, self.pic_resolution[num], self.pic_download_url.format(pic_num, num)))

if __name__ == '__main__':
    num1 = 0
    threads = []
    queue = Queue(maxsize=27)
    ua = UserAgent()
    get_page_content = GetNextPageContent(104, queue, ua)
    threads.append(get_page_content)
    get_page_content.start()

    for i in range(6):
        download_pics = DownLoadPics(queue, ua)
        download_pics.start()
        threads.append(download_pics)

    for thread in threads:
        thread.join()

