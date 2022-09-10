from .running import Running, MultiRunning
from .competitor import Competitor, animals, metal_symbol
from .racing import Game
import rich 
from rich.markdown import Markdown
import time 

def play():
    pause_dict = {',': 0.5, '，': 0.5, '.': 1.0, '。': 1.0, '\n': 1.0}
    history = "\t孙武既死，后百余岁有孙膑。膑生阿、鄄之间，膑亦孙武之后世子孙也。孙膑尝与庞涓俱学兵法。庞涓既事魏，得为惠王将军，而自以为能不及孙膑，乃阴使召孙膑。膑至，庞涓恐其贤于己，疾之，则以法刑断其两足而黥之，欲隐勿见。\n\t齐使者如梁，孙膑以刑徒阴见，说齐使。齐使以为奇，窃载与之齐。齐将田忌善而客待之。忌数与齐诸公子驰逐重射。孙子见其马足不甚相远，马有上、中、下、辈。于是孙子谓田忌曰：君弟重射，臣能令君胜。田忌信然之，与王及诸公子逐射千金。及临质，孙子曰：今以君之下驷与彼上驷，取君上驷与彼中驷，取君中驷与彼下驷。既驰三辈毕，而田忌一不胜而再胜，卒得王千金。"
    # 游戏标题
    rich.print(Markdown("# 田忌赛马"))
    # 游戏简介
    for char in history:
        rich.print(char, end='')
        if char in pause_dict.keys():
            time.sleep(pause_dict[char])
        else:
            time.sleep(0.1)
    # 开始游戏
    rich.print('\n\n[red bold]田忌要破产了，快来帮他比赛吧！[/red bold]')
    time.sleep(1)
    rich.print("\n游戏规则：\n\n 1.五局三胜制\n 2.每场赌金 500，逐场递增 200\n 3.初始金币 5000")
    coins = 5000
    n = 0
    while True:
        n += 1
        rich.print(Markdown(f"## 第 {n} 回合比赛"))
        delta_coins = 300 + 200 * n
        rich.print(f'田忌还有金币 {coins}，本回合赌金 {delta_coins}')
        # 直播画面选择
        symbol_level = input('请选择画面分辨率 [ 1.普通, 2.高清(default), 3.超清 ] : ')
        symbol_level = symbol_level if symbol_level in ['1','2','3'] else '2'
        game = Game(symbol_level, coef=0.05, animals=animals, coins=coins)
        win, extra_coins = game.start()
        coins = coins + delta_coins * (win * 2 - 1) + extra_coins
        if coins <= 0:
            rich.print('\n田忌输光了他的所有...\n\n[red]Game Over![/red]')
            break 
        again = input(f"目前还有金币 {coins} ，是否想再玩一局?[Y/n]: ")
        if again.lower() == 'n':
            break 
