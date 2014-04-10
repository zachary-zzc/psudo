# -*- coding: utf-8 -*-

import utils.parser as parser
import module.commodule as commodule
from structure.config import *
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
            ret = {}
            for module in glb.moduleStack:
                for key in module.localVarList:
                    ret[key] = module.varList[key]
            return ret

    def run(self):
        self.status = True
        try:
            contents = parser.preprocess(self.contents)
            glb.globalVarList.update(globals())
            self.globalModule = commodule.commodule(glb.globalVarList,
                                                    glb.globalFuncList,
                                                    contents)
            self.globalModule.setGlobal()
            self.globalModule.run()

            for func in glb.globalFuncList:
                if func == 'Main':
                    glb.globalFuncList[func].run()
        # except Exception as e:
        #     print('Run compiler fail: {}'.format(e))
        finally:
            self.status = False

class monitor(threading.Thread):
    def __init__(self, contents, lock):
        threading.Thread.__init__(self)
        self.lock = lock
        self.pseudoCompiler = psudo(contents, self.lock)
        # task queue in glb.py

    # def add_task(self, task):
    #     self.task.append(task) # task enqueue

    def run(self):
        while True:
            with self.lock:
                """
                import os
                if os.path.exists(r'tasks.txt'):
                    with open(r'tasks.txt', 'r') as f:
                        glb.taskQueue = (''.join(f.readlines())).split('\n')
                with open(r'tasks.txt', 'w') as f:
                    f.write('')
                """
                while glb.taskQueue:
                    task = glb.taskQueue.pop(0)
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
    glb.taskQueue.append('start')
    with open('demo/graph.txt', 'r') as f:
        contents = f.readlines()
    monitor = monitor(''.join(contents), lock)
    monitor.start()
