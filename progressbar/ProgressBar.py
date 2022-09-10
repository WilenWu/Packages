# -*- coding: utf-8 -*-
import time
import sys
import threading

class ProgressBar:
    def __init__(self, task, symbol='#', space='-', width=50, desc="Processing", circle = False):
        """
        task : 可迭代对象
        symbol : 进度条符号
        width : 进度条展示的长度
        desc : 进度条前面展示的文字
        """
        self._task = task
        self._len = len(task)
        self.symbol = symbol
        self.space = space
        self.width = width
        self.desc = desc
        self._index = 0
        self.__circle = circle
        self.__circle_chars = ['-', '\\', '|', '/']
    
    def __len__(self):
        return self._len 
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._index == 0:
            self.time_start = time.time()
        if self._index < self._len:
            self.time_end = time.time()
        sys.stdout.write(self._get_bar(self._index, self.time_start, self.time_end))
        if self._index == self._len:
            raise StopIteration
        self._index += 1
        return self._task[self._index - 1]
    
    def _get_bar(self, index, time_start, time_end):
        percent = index / self._len 
        left = int(self.width * percent)
        right = self.width - left
        
        tags = self.symbol * left
        spaces = self.space * right
        
        t = time_end - time_start 
        
        current_bar = self.__circle_chars[index % 4] if self.__circle else f'{tags}{spaces}'
        return f"\r{self.desc}:  [ {current_bar} ] {percent:.1%} | Time: {t:.1f}s "
    
    def update(self, index):
        if index == 0:
            self.time_start = time.time()
        if index < self._len:
            self.time_end = time.time()
        if index >= self._len:
            index = self._len - 1
        sys.stdout.write(self._get_bar(index + 1, self.time_start, self.time_end))

class MultiProgressBar:
    
    def __init__(self, end='\ncomplete\n'):
        self._task_dict = {}
        self.task_result = {}
        # 锁定进程，避免输出混乱
        self._lock = threading.Lock()
        self.end = end
    
    def add_task(self, task_id, progress, func, *args, **kwargs):
        """
        progress: 进度条实例
        func: 处理可迭代任务中每个元素的函数
        *args, **kwargs: progress 实例提供可迭代任务中每个元素，*args, **kwargs 为剩余参数 
        """
        self._task_dict[task_id] = {'bar':progress, 'func':func, 'args':args, 'kwargs':kwargs}
    
    def update(self, tasks):
        for task_id in tasks:
            bar = self._task_dict[task_id]['bar']
            bar.update(bar._index)
            sys.stdout.write('\n')
    
    def _update_thread(self, task_id):
        # 调取进程参数
        bar  = self._task_dict[task_id]['bar']
        task = self._task_dict[task_id]['bar']._task
        func = self._task_dict[task_id]['func']
        args = self._task_dict[task_id]['args']
        kwargs = self._task_dict[task_id]['kwargs']
        
        for value in task:
            with self._lock: 
                sys.stdout.write(f'\033[{self._thread_num}A')
                self.update(self._ordered_tasks)
                bar._index += 1
            result = func(value, *args, **kwargs)
        
        with self._lock:
            self.task_result[task_id] = result 
    
    def start(self, tasks):
        self._thread_num = len(tasks)
        self._ordered_tasks = tasks
        # 初始化零进度条
        for task_id in tasks:
            self._task_dict[task_id]['bar']._index = 0
        sys.stdout.write('\n'*self._thread_num)
        # 启动进程
        thread_pool = []
        for task_id in tasks:
            thread = threading.Thread(target=self._update_thread, args=(task_id,))
            thread_pool.append(thread)
        for thread in thread_pool:
            thread.start()
        # 检测多进程是否结束
        for p in thread_pool:
            p.join()
        sys.stdout.write(self.end)
