from .dice import Dice, GameRunner

def play():
    print("Welcome\nAdd the values of the dice\n"
          "It's really that easy" )
    n = wins = 0
    
    color = input("What color do you like?: ")
    color = color if color else 'red'
    dice = Dice(color)

    while True:
      n += 1
      print(f"Round {n}")
      guess_num = input("What is your guess?: ")
      win = GameRunner(dice, guess_num)
      wins += win 
      print(f"Wins: {wins} of {n}")
      if n%5==0:
        play = input("Would you like to play again?[Y/n]: ")
      else:
        play = 'Y'
      if play.lower() == 'n':
        break 