# -*- coding: utf-8 -*-
import time
import sys
import threading

playing_area = r"""
       ____________________________________________________________________________       
      / __________________________________________________________________________ \      
     / /                                                                          \ \     
    / /                                                                            \ \    
   / /                                                                              \ \   
  | |                                                                                | |  
  | |                                                                                | |  
  | |                                                                                | |  
   \ \                                                                              / /   
    \ \                                                                            / /    
     \ \__________________________________________🚩🏁____________________________/ /     
      \___________________________________________🚩________🏁_____________________/      
"""

# 内赛道坐标
segment11 = [(i,11) for i in range(53,81)]
segment12 = [(i,2) for i in range(82,8,-1)]
segment13 = [(i,11) for i in range(9,50)]
track1 = segment11 + \
    [(81,11), (84,10), (85,9), (86,8), (86,7), (86,6), (85,5), (84,4), (83,3)] + \
    segment12 + \
    [(8,3), (7,4), (6,5), (5,6), (5,7), (5,8), (6,9), (7,10), (8,11)] + \
    segment13

# 外赛道坐标
segment21 = [(i,12) for i in range(61,82)]
segment22 = [(i,1) for i in range(83,7,-1)]
segment23 = [(i,12) for i in range(8,50)]
track2 = segment21 + \
    [(82,12), (83,11), (86,10), (87,9), (88,8), (88,7), (88,6), (87,5), (86,4), (85,3), (84,2)] + \
    segment22 + \
    [(7,2), (6,3), (5,4), (4,5), (3,6), (3,7), (3,8), (4,9), (5,10), (6,11), (7,12)] + \
    segment23 

area = [playing_area, track1, track2]

class RunningLap:
    
    def __init__(self, competitor1, competitor2, area=area):
        """
        snapshots : 比赛快照(长度必须160)
        competitor : 参赛动物
        width : 进度条宽度
        desc : 参赛方
        track : 1.内赛道, 2.外赛道
        """
        self.playing_area = area[0]
        self.track1 = area[1]
        self.track2 = area[2]
        
        self.task1 = competitor1.snapshots
        self.symbol1 = competitor1.symbol
        self.task2 = competitor2.snapshots
        self.symbol2 = competitor2.symbol
        self.index1 = self.index2 = 0
    
    def get_snapshot(self, index1, index2):
        area_list = self.playing_area.split('\n')
        for index, track, symbol in zip([index1, index2], [self.track1, self.track2], [self.symbol1, self.symbol2]):
            x, y = track[index]
            area_list[y] = area_list[y][:x] + symbol + area_list[y][x+1:]
        new_area = '\n'.join(area_list)
        return f"\r{new_area}"
    
    def update(self, index1, index2):
        if index1 + index2 == 0:
            sys.stdout.write(self.playing_area)
        sys.stdout.write("\033[13A")
        sys.stdout.write(self.get_snapshot(index1+1, index2+1))
