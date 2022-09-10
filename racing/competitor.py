import numpy as np 

animals = {
  '1': ['鼠','牛','虎','兔','龍','蛇','馬','羊','猴','鷄','狗','猪'],
  '2': ['🐭','🐮','🐯','🐰','🐲','🐍','🐴','🐐','🐵','🐔','🐶','🐷'], 
  '3': ['🐁','🐄','🐅','🐇','🐉','🐍','🐎','🐐','🐒','🐓','🐕','🐖']
  }
foreigners = ['🐌','🐢','🦀','🐸']
animals = {k: animals[k] + foreigners for k in animals.keys()}

metal_symbol = {'trophy':'🏆', 'gold':'🥇', 'silver':'🥈', 'bronze':'🥉'}

class Competitor:
    """运动员"""
    def __init__(self, symbol='🐌', speed=20, coef=0.05):
        """
        speed : 经验速度
        coef : 稳定性
        """
        self.symbol = symbol
        self.speed = speed
        self._coef = coef 
        
    def set_snapshots(self, length=200, num=160):
        """  
        length : 赛道长度(m)
        num : 快照数量
        """
        delta_t = length / self.speed / num
        dt = np.random.normal(0, delta_t * self._coef, num)
        t = dt.cumsum() + delta_t
        t[t<=0] = 0
        
        self.length = length
        self.snapshots = t 
        self.average_velocity = length/t.sum()
        self.record = t.sum()
    
    def __lt__(self,other):
        return self.speed < other.speed
    
    def __gt__(self,other):
        return self.speed > other.speed
