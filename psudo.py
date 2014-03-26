# -*- coding: utf-8 -*-

import utils.parser as parser
import module.commodule as commodule
import structure
import glb

import threading
import time

class psudo(threading.Thread):
    def __init__(self, contents, lock):
        threading.Thread.__init__(self)
        self.lock = lock
        self.status = False
        self.contents = contents
        self.globalModule = None

    def getStatus(self):
        return self.status

    def getParamList(self):
        if self.globalModule is None:
            raise Exception('Psuedo code compiler haven\' started yet!')
        else:
            return self.globalModule.varList

    def run(self):
        self.status = True
        try:
            self.contents = parser.preprocess(self.contents)
            self.globalModule = commodule.commodule(glb.globalVarList,
                                                    glb.globalFuncList,
                                                    contents)
            self.globalModule.run()

            for func in glb.globalFuncList:
                if func == 'Main':
                    glb.globalFuncList[func].run()
        # except Exception as e:
            # print('Run compiler fail: {}'.format(e))
        finally:
            self.status = False

class monitor(threading.Thread):
    def __init__(self, contents, lock):
        threading.Thread.__init__(self)
        self.lock = lock
        self.pseudoCompiler = psudo(contents, self.lock)
        self.task = [] # task queue

    def add_task(self, task):
        self.task.append(task) # task enqueue

    def run(self):
        while True:
            with self.lock:
                print('monitor thread running!')
                self.add_task('get_status')
                while self.task:
                    task = self.task.pop(0)
                    if task == 'start':
                        self.pseudoCompiler.start()
                    elif task == 'get_status':
                        print('current status : {}'.format(self.pseudoCompiler.getStatus()))
                    elif task == 'get_params':
                        print(self.pseudoCompiler.getParamList())
                # self.lock.notify()
            time.sleep(0.5)

if __name__ == '__main__':
    lock = threading.Lock()
    with open('bubble.txt', 'r') as f:
        contents = f.readlines()
    monitor = monitor(''.join(contents), lock)
    monitor.add_task('start')
    monitor.start()
