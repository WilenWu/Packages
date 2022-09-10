import dice 
import racing
import rich 
from rich.markdown import Markdown

games = {'1':dice.play, '2':racing.play}

md = Markdown("""
# 游戏列表
1. 猜骰子
2. 田忌赛马
""")
rich.print(md)

game_no = input('想玩什么游戏? 请选择: ')
if not 1 <= int(game_no) <= 2 :
    game_no = input('输入错误, 请重新选择: ')
    
play = games[game_no]
play()