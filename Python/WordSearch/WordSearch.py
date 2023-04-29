END = '\033[0m'
BOLD = '\033[1m'

with open('game.txt','r') as fh:
    gameboard = [row.strip().lower() for row in fh.readlines()]

def check_horizontal_vertical(positions, vertical, word):
    for index, x in enumerate(positions):
        reversed_ = x[::-1]
        if word in x:
            index_y = x.index(word)
            if vertical:
                return True, (word,index,index_y,index,index_y+len(word)-1)
            else:
                return True, (word,index_y,index,index_y+len(word)-1,index)
        elif word in reversed_:
            index_y = reversed_.index(word)
            if vertical:
                return True, (word,index,index_y,index,index_y+len(word)-1)
            else:
                return True, (word,index_y,index,index_y,index_y+len(word)-1)
    return [False]

def solve(gameboard,word):
    horizontal = check_horizontal_vertical(gameboard,False,word)
    if horizontal[0] is True:
        return horizontal[1]
    else:
        vertical_board = [''.join(col) for col in zip(*gameboard)]
        vertical = check_horizontal_vertical(vertical_board,True,word)
        if vertical[0] is True:
            return vertical[1]
    return None

def main():
    
    while True:
        word = input("Enter word to find: ")
        coordinates = solve(gameboard,word)
        
        if coordinates == None:
            print("Couldn't find word. Enter another.\n")
        else:
            word,x1,y1,x2,y2 = coordinates
            print(f"\n\"{word}\" found at: ({x1},{y1}) to ({x2},{y2})")
            print("\n"," "*4,' '.join([str(x) for x in range(len(gameboard))]))

            # Print board with solved words
            for indexX, x in enumerate(gameboard):
                modded = []
                for indexY, y in enumerate(x):
                    if coordinates[1] <= indexY <= coordinates[3] and coordinates[2] <= indexX <= coordinates[4]:
                        modded.append(f"{BOLD}{y}{END}")
                    else:
                        modded.append(y)
                print(f"{indexX:<5}{' '.join(modded)}")
            print()
        
if __name__ == '__main__':
    main()
