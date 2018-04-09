import requests
from fake_useragent import UserAgent
import json
import datetime
import time
try:
    from Queue import Queue #python2
except:
    from queue import Queue #python3

from threading import Thread

queue = Queue()
start = '20110219'
end = time.strftime('%Y%m%d')

queue.put(start)

datestart = datetime.datetime.strptime(start, '%Y%m%d')
dateend = datetime.datetime.strptime(end, '%Y%m%d')

while datestart < dateend:
    datestart += datetime.timedelta(days=1)
    ymd = datestart.strftime('%Y%m%d')
    queue.put(ymd)

ua = UserAgent()
user_agent = ua.Chrome


class DownArticle(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        global queue
        while True:
            current_ymd = queue.get()
            self.get_resp(current_ymd)
            queue.task_done()
            if queue.empty():
                break

    def get_resp(self, current_ymd):
        url = 'https://interface.meiriyiwen.com/article/day?dev=1&date={}'.format(current_ymd)

        try:
            time.sleep(2)
            resp = requests.get(url, headers={"User-Agent": user_agent})
            if resp.status_code == 200:
                self.write_to_local(resp.text)
                print(current_ymd + 'has be done.')
            else:
                resp = requests.get(url, headers={"User-Agent": user_agent})
                if resp.status_code != 200:
                    pass
        except:
            with open('network_error_ymd.txt', 'a+') as f:
                f.write(current_ymd + '\n')
                f.close()



    def write_to_local(self, data):
        dict_article = json.loads(data)
        curr = dict_article['data']['date']['curr']
        title = dict_article['data']['title']
        content = dict_article['data']['content']
        try:
            with open('D:\meiriyiwen\{0}{1}.html'.format(curr, title), 'a+') as f:
                f.write(content)
        except:
            print('there are some problems at {}'.format(curr))
            with open('writefile_error.txt', 'a+') as f:
                f.write(curr + '\n')
                f.close()



if __name__ == '__main__':
    threads = []
    for i in range(5):
        downthread = DownArticle()
        threads.append(downthread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
