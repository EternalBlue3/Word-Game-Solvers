import time
start = time.time()

END = '\033[0m'
BOLD = '\033[1m'

with open('game.txt','r') as fh:
    gameboard = [row.strip().lower() for row in fh.readlines()]
    
with open('words.txt','r') as fh:
    words = [word.strip().lower() for word in fh.readlines()]

def check_horizontal_vertical(positions, vertical):
    found = []
    for index, x in enumerate(positions):
        for y in words:
            reversed_ = x[::-1]
            if y in x:
                index_y = x.index(y)
                if vertical:
                    found.extend([(y,index,index_y,index,index_y+len(y)-1)])
                else:
                    found.extend([(y,index_y,index,index_y+len(y)-1,index)])
            elif y in reversed_:
                index_y = reversed_.index(y)
                if vertical:
                    found.extend([(y,index,index_y,index,index_y+len(y)-1)])
                else:
                    found.extend([(y,index_y,index,index_y,index_y+len(y)-1)])
    return found

def solve(gameboard,words):
    found = []
    vertical = [''.join(col) for col in zip(*gameboard)]
    found.extend(check_horizontal_vertical(gameboard,False))
    found.extend(check_horizontal_vertical(vertical,True))
    return found

def main():
    coordinates = solve(gameboard,words)

    # Print board with solved words
    for indexX, x in enumerate(gameboard):
        modded = []
        for indexY, y in enumerate(x):
            incoords = False
            for coords in coordinates:
                if coords[1] <= indexY <= coords[3] and coords[2] <= indexX <= coords[4]:
                    incoords = True
            if incoords:
                modded.append(f"{BOLD}{y}{END}")
            else:
                modded.append(y)
        print(''.join(modded))
        
if __name__ == '__main__':
    main()
