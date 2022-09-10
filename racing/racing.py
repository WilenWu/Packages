import re 
import time 
import re 
import rich 
import random 
from rich.markdown import Markdown
from rich.console import Console
from rich.table import Table
from .competitor import Competitor, animals, metal_symbol
from .running import Running, MultiRunning

console = Console()


class Game:
    def __init__(self, symbol_level, coef=0.05, animals=animals, coins = None):
        self.symbol_level = symbol_level
        self.coef = coef
        """初始化动物数据"""
        competitor_pool = {}
        animals = animals[symbol_level]
        for serial_num in range(len(animals)): 
            speed = random.uniform(18,22) if serial_num < 12 else random.uniform(15,25)
            competitor = Competitor(symbol=animals[serial_num], speed=speed, coef=coef)
            competitor.set_snapshots(length=200, num=160)
            # 参赛选手在12生肖中的序列号
            competitor_pool[serial_num] = competitor
        self.competitor_pool = competitor_pool
        self.foreigner_pool = list(competitor_pool.keys())[12:]
        self.coins = coins 
        self.set_race()
    
    def print_competitors(self, pool, tian, king, output=True):
        sorted_pool = sorted(pool.items(), key=lambda item: item[1], reverse=True)
        sorted_tian = [item[0] for item in sorted_pool if item[0] in tian]
        sorted_king = [item[0] for item in sorted_pool if item[0] in king]
        """输出动物战力表格"""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("五局三胜")
        table.add_column("田忌", justify="right")
        table.add_column("齐王", justify="left")
        for i, (tian_id, king_id) in enumerate(zip(sorted_tian, sorted_king)):
            table.add_row(
                f"{i+1}", 
                f"{tian_id}: {pool[tian_id].symbol} {pool[tian_id].speed:.1f}",
                f"{pool[king_id].speed:.1f} {pool[king_id].symbol} :{king_id}"
                )
        console.print(table)
        if output:
            return sorted_tian, sorted_king
    
    def set_race(self):
        # 12生肖随机分配
        serial_num_pool = list(range(12))
        random.shuffle(serial_num_pool)
        tian_pool, king_pool = serial_num_pool[:6], serial_num_pool[6:]
        # 打印田和齐的选手实力
        sorted_tian, sorted_king = self.print_competitors(self.competitor_pool, tian_pool, king_pool)
        # 添加运动员
        race = MultiRunning()
        for serial_num, competitor in self.competitor_pool.items():
            if serial_num in tian_pool:
                name = '田忌'
            elif serial_num in king_pool:
                name = '齐王'
            else:
                name = '外援'
            race.add_competitor(serial_num, Running(competitor, desc=name))
        self.race = race 

        # 游戏难度选择，并确定出场顺序
        game_level = input('请选择游戏难度 [ 1.随机, 2.普通(default) ] : ')
        game_level = game_level if game_level in ['1','2','3'] else '2'
        if game_level == '1':
            self.sorted_tian = tian_pool
            self.sorted_king = king_pool
            rich.print('随机模式: 田忌和齐王随机挑选动物出场')
        elif game_level == '2':
            self.normal_game(sorted_tian, sorted_king)
    
    def normal_game(self, sorted_tian, sorted_king):
        self.sorted_king = sorted_king
        sorted_king_symbol = [self.competitor_pool[king_id].symbol for king_id in sorted_king]
        rich.print(f'普通模式: 齐王将依次出场 {" >> ".join(sorted_king_symbol)}') 
        while True:
            input_str = input('请田忌选择出场顺序[ 0.随机, 1.顺序, 2.逆序, 3.空格分隔自排序 ]: ')
            input_str = '0' if input_str.strip() == '' else input_str.strip()
            if input_str == '0':
                random_tian = sorted_tian.copy()
                random.shuffle(random_tian)
                self.sorted_tian = random_tian
                break 
            elif input_str == '1':
                self.sorted_tian = sorted_tian
                break 
            elif input_str == '2':
                asc_pool = sorted(self.competitor_pool.items(), key=lambda item: item[1])
                self.sorted_tian = [item[0] for item in asc_pool if item[0] in sorted_tian]
                break 
            else:
                input_str = re.split(' +', input_str.strip())
                input_str = [int(k) for k in input_str]
                if set(input_str) != set(sorted_tian):
                    rich.print('出场运动员不符合规则，请重新选择')
                else:
                    self.sorted_tian = [int(k) for k in input_str]
                    break 
    
    def start(self):
        pool = self.competitor_pool
        tian_pool = self.sorted_tian
        king_pool = self.sorted_king
        race = self.race
        # 比赛开始
        n = wins = 0
        medal_pool = []
        extra_coins = 0
        for index in range(len(king_pool)):
            tian_id, king_id = tian_pool[index], king_pool[index]
            n += 1
            rich.print(f'\n第 {n} 局比赛即将开始')
            time.sleep(1)
            tian_power = f'{pool[tian_id].symbol} {pool[tian_id].speed:.1f}'
            king_power = f'{pool[king_id].symbol} {pool[king_id].speed:.1f}'
            rich.print(f'[bold]田忌[/bold]: {tian_power}  v.s.  [bold]齐王[/bold]: {king_power}')
            print('\nReady ?')
            for i in range(3):
                rich.print(f'{3 - i} ',end=' ')
                time.sleep(1)
            print('\nGo !\n')
            race.start([tian_id, king_id])
            if race._task_dict[tian_id]['bar'].rank == metal_symbol['gold']:
                wins += 1
            medal_pool.append(race._task_dict[tian_id]['bar'].rank)
            rich.print(f"[ {''.join(medal_pool)} ] / 5")
            # 赢三局或者输三局则结束本场比赛
            if wins >= 3:
                break 
            elif n - wins >= 3:
                break 
            elif n - wins == 2 and random.random() < 0.3:
                need_foreigner = input("目前已战败两局，是否雇佣外援？[y/N] :")
                if need_foreigner.lower() == 'y' and self.coins >= 300:
                    rich.print('雇佣成功，每局雇佣费 300')
                    rich.print('悄悄告诉你，外援水分很大')
                    extra_coins -= 300 
                    self.coins  -= 300
                    foreigner = random.choice(self.foreigner_pool) # 随机分配外援
                    tian_pool.insert(index + 1, foreigner)
                elif need_foreigner.lower() == 'y':
                    rich.print('穷鬼 ！继续你的比赛吧')
        result = wins >= 3 
        if result:
            print('\n恭喜! 田忌获胜! ')
        else:
            print('\n齐王获胜! ')
        
        return result, extra_coins

