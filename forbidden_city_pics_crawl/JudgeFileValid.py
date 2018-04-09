from PIL import Image
from threading import Thread
import os
try:
    from Queue import Queue
except:
    from queue import Queue

class JudgeFile(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self._queue = queue

    def run(self):
        while not self._queue.empty():
            pathfile = self._queue.get()
            self.isvalidimage(pathfile)


    def isvalidimage(self, pathfile):
        '''
        这个函数接收一个图片路径，用来判断这个图片是否完整
        :param pathfile:
        :return:
        '''
        try:
            Image.open(pathfile).verify()
            pass
        except:
            print('remove {}'.format(pathfile))
            os.remove(pathfile)


if __name__ == '__main__':
    threads = []
    queue = Queue()
    root_path = 'D:\\forbidden_city1'
    list_file = os.listdir('D:\\forbidden_city1')
    for i in range(0, len(list_file)):
        path = os.path.join(root_path, list_file[i])
        queue.put(path)

    for i in range(4):
        judge = JudgeFile(queue)
        judge.start()
        threads.append(judge)

    for i in range(4):
        threads[i].join()



