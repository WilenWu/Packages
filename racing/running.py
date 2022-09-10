# -*- coding: utf-8 -*-
import time
import sys
import threading
from progressbar import ProgressBar, MultiProgressBar
from .competitor import metal_symbol

class Running(ProgressBar):
    
    def __init__(self, competitor, space='_', width=80, desc="起跑线"):
        """
        competitor : 参赛选手
        width : 进度条宽度
        desc : 参赛方
        """
        ProgressBar.__init__(self,
            task = competitor.snapshots,
            symbol = competitor.symbol,
            space = space,
            width = width,
            desc = desc,
            circle = False
            )
        self._get_bar = self.get_snapshot
        self.rank = '🚩'
    
    def get_snapshot(self, index, time_start, time_end):
        """当前快照"""
        percent = index / self._len 
        left = int(self.width * percent)
        right = self.width - left
        
        tags = self.space * left  + self.symbol
        spaces = self.space * right
        
        t = time_end - time_start 
        
        current_bar = f'{tags}{spaces}'
        return f"\r{self.desc}: 🏁 {current_bar} {self.rank} {percent:.1%} | Time: {t:.1f}s"

class MultiRunning(MultiProgressBar):
    
    def __init__(self, end='\n'):
        MultiProgressBar.__init__(self, end=end)
        self.competitor_dict = {}
    
    def add_competitor(self, competitor_id, running):
        """
        competitor_id : 参赛选手id
        running: 进度条实例
        """
        self.competitor_dict[competitor_id] = running
        self._task_dict[competitor_id] = {
            'bar':running, 
            'func':time.sleep, 
            'args':(), 
            'kwargs':{}
            }
    
    def update(self, tasks):
        sorted_bars = self.set_rank(tasks)
        for task_id in tasks:
            bar = self._task_dict[task_id]['bar']
            bar.update(bar._index)
            sys.stdout.write('\n')
    
    def set_rank(self, tasks, metal_symbol=metal_symbol):
        """终点处添加排名"""
        bars = {task_id: self._task_dict[task_id]['bar']._index for task_id in tasks}
        sorted_bars = sorted(bars.items(), key=lambda item: item[1], reverse=True)
        for rank, (task_id, index) in enumerate(sorted_bars):
            if rank == 0:
                self._task_dict[task_id]['bar'].rank = metal_symbol['gold']
            elif rank == 1:
                self._task_dict[task_id]['bar'].rank = metal_symbol['silver']
            elif rank == 2:
                self._task_dict[task_id]['bar'].rank = metal_symbol['bronze']
            else:
                self._task_dict[task_id]['bar'].rank = ' ' + str(rank + 1) 
        return sorted_bars
