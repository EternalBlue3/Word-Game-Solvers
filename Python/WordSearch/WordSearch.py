import sys

END = '\033[0m'
BOLD = '\033[31m'

def read_gameboard():
    try:
        with open('game.txt', 'r') as f:
            gameboard = [row.strip().lower() for row in f.readlines()]
        return gameboard
    except FileNotFoundError:
        print("Could not find the game file. Please create a file called \"game.txt\" in the same directory as this solver.")
        sys.exit(1)

def check_horizontal_vertical(gameboard, word):
    for i, row in enumerate(gameboard):
        if word in row:
            j = row.index(word)
            return True, (i, j, i, j + len(word) - 1)
        
    for j in range(len(gameboard[0])):
        column = ''.join(row[j] for row in gameboard)
        if word in column:
            i = column.index(word)
            return True, (i, j, i + len(word) - 1, j)
        
    return False, None

def check_diagonals(gameboard, word):
    diagonals = []
    opposite_diagonals = []
    for i in range(-len(gameboard)+1, len(gameboard)):
        diagonal = ''.join([gameboard[x][y] for x in range(len(gameboard)) for y in range(len(gameboard)) if x - y == i])
        diagonals.append((diagonal, i))
        diagonal = ''.join([gameboard[x][y] for x in range(len(gameboard)) for y in range(len(gameboard)) if (len(gameboard)-1-x) - y == i])
        opposite_diagonals.append((diagonal, i))
    
    for x in diagonals:
        if word in x[0] or word in x[0][::-1]:
            i = x[1]
            index = x[0].index(word) if word in x[0] else x[0].index(word[::-1])
            x,y = (-i+index,index) if i<0 else (index,i+index)

            indices = [(x,y)]
            for i in range(len(word)-1):
                x += 1
                y += 1
                indices.append((x,y))
            
            return True, indices
    
    for x in opposite_diagonals:
        if word in x[0] or word in x[0][::-1]:
            i = x[1]
            gameboard_length = len(gameboard)-1
            index = x[0].index(word) if word in x[0] else x[0].index(word[::-1])
            x,y = (gameboard_length-index,-i+index) if i<0 else (gameboard_length-(i + index),index)

            indices = [(x,y)]
            for i in range(len(word)-1):
                x -= 1
                y += 1
                indices.append((x,y))
            
            return True, indices
    
    return False, None

def main():
    gameboard = read_gameboard()

    print('Enter words to find or type "exit" to quit.')
    while True:
        word = input('Enter word: ').strip().lower()
        if word == 'exit':
            break

        diagonal = False
        found, coords = check_horizontal_vertical(gameboard, word)
        if not found:
            diagonal = True
            found, coords = check_diagonals(gameboard, word)

        if coords is None:
            print(f'"{word}" not found.\n')
            continue

        if diagonal:
            print(f'\n"{word}" found at coords: {coords}\n')
            print('   ' + ' '.join(str(i % 10) for i in range(len(gameboard))))
            
            for i, row in enumerate(gameboard):
                line = f'{i:>2} '
                for j, letter in enumerate(row):
                    if any((j,i) == coord for coord in coords):
                        line += f'{BOLD}{letter}{END} '
                    else:
                        line += f'{letter} '
                print(line)
            print()
            
        else:
            print(f'\n"{word}" found at: ({coords[0]},{coords[1]}) to ({coords[2]},{coords[3]})\n')
            print('   ' + ' '.join(str(i % 10) for i in range(len(gameboard))))

            for i, row in enumerate(gameboard):
                line = f'{i:>2} '
                for j, letter in enumerate(row):
                    if coords[0] <= i <= coords[2] and coords[1] <= j <= coords[3]:
                        line += f'{BOLD}{letter}{END} '
                    else:
                        line += f'{letter} '
                print(line)
            print()

if __name__ == '__main__':
    main()
