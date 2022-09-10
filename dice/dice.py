# dicegame.py
import random
import sys 
from rich import print 

class Dice:
  def __init__(self, color = 'red'):
    self.color = color 
    self.paint(color)
  def paint(self, color):
    top    = '┌───────┐'
    blank  =  '       '
    left   =  ' ●     '
    middle =  '   ●   '
    right  =  '     ● '
    both   =  ' ●   ● '
    bottom = '└───────┘'
    sides = [
      (blank, middle, blank),
      (left,  blank,  right),
      (left,  middle, right),
      (both,  blank,  both ),
      (both,  middle, both ),
      (both,  both,   both )  
    ]
    for i, side in enumerate(sides):
      sides[i] = (f"|[{color}]{e}[/{color}]|" for e in side)
    self.sides = ['\n'.join((top,) + tuple(side) + (bottom,)) for side in sides]
  def play(self):
    rand = random.randint(1, 6)
    return rand


def GameRunner(dice, guess_num):
  rand_num = dice.play() 
  win = rand_num == int(guess_num)
  if win:
    print("Congratulations !")
  else:
    print("Sorry that's wrong")
  print(f"The answer is: ")
  print(dice.sides[rand_num - 1])
  return win

