# -*- coding: utf-8 -*-

import utils.parser as parser
import module.commodule as commodule

from structure.config import *

import json

import glb

# import threading
import time
import sys

def pseudo(filepath):
    with open(filepath, 'r') as inf:
        contents = ''.join(inf.readlines()).split('\n')

    # init global settings
    glb.step = 1
    glb.var_dict.clear()
    glb.error_msg = ""
    glb.global_var_list.update(globals())

    init_module = commodule.commodule(glb.global_var_list,
                                      glb.global_func_list,
                                      contents,
                                      line = 1)
    init_module.run()

    if 'Main' in glb.global_func_list:
        glb.global_func_list['Main'].__call__()

    with open(r'visualize/varList.json', 'w') as f:
        json.dump(glb.var_dict, f, sort_keys=True, indent=4)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python3 psudo [filename]')
        exit()
    pseudo(sys.argv[1])

# class psudo(threading.Thread):
#     def __init__(self, contents, lock):
#         threading.Thread.__init__(self)
#         self.lock = lock
#         self.status = False
#         self.contents = contents
#         self.global_module = None
#
#     def getStatus(self):
#         return self.status
#
#     def getParamList(self):
#         if self.global_module is None:
#             raise Exception('Psuedo code compiler haven\' started yet!')
#         else:
#             ret = {}
#             for module in glb.module_stack:
#                 for key in module.local_var_list:
#                     ret[key] = module.var_list[key]
#             return ret
#
#     def run(self):
#         self.status = True
#         # set force stop label to false
#         glb.forceStop = False
#
#         glb.step = 1
#         glb.var_dict.clear()
#         glb.error_msg = ""
#
#         # run compiler
#         contents = parser.preprocess(self.contents)
#         glb.global_var_list.update(globals())
#         self.global_module = commodule.commodule(glb.global_var_list,
#                                                  glb.global_func_list,
#                                                  contents,
#                                                  line = 1)
#         self.global_module.run()
#         for func in glb.global_func_list:
#             if func == 'Main':
#                 glb.global_func_list[func].__call__()
#         print(self.contents)
#
#         self.status = False
#
# class monitor(threading.Thread):
#     def __init__(self, contents, lock):
#         threading.Thread.__init__(self)
#         self.lock = lock
#         self.pseudoCompiler = psudo(contents, self.lock)
#         # task queue in glb.py
#
#     # def add_task(self, task):
#     #     self.task.append(task) # task enqueue
#
#     def run(self):
#         while True:
#             with self.lock:
#                 """
#                 import os
#                 if os.path.exists(r'tasks.txt'):
#                     with open(r'tasks.txt', 'r') as f:
#                         glb.task_queue = (''.join(f.readlines())).split('\n')
#                 with open(r'tasks.txt', 'w') as f:
#                     f.write('')
#                 """
#                 while glb.task_queue:
#                     task = glb.task_queue.pop(0)
#                     if task == 'start':
#                         self.pseudoCompiler.start()
#                         # try:
#                         #     self.pseudoCompiler.start()
#                         # except Error:
#                         #     print('{}: {}'.format(glb.current_line, glb.current_content))
#                     elif task == 'get_status':
#                         print('current status : {}'.format(self.pseudoCompiler.getStatus()))
#                     elif task == 'get_params':
#                         print(self.pseudoCompiler.getParamList())
#                 # self.lock.notify()
#             time.sleep(0.1)

# if __name__ == '__main__':
#     lock = threading.Lock()
#     glb.task_queue.append('start')
#     with open('demo/graph.txt', 'r') as f:
#         contents = f.readlines()
#     monitor = monitor(''.join(contents), lock)
#     monitor.start()
