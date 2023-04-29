END = '\033[0m'
BOLD = '\033[31m'

def read_gameboard():
    with open('game.txt', 'r') as f:
        gameboard = [row.strip().lower() for row in f.readlines()]
    return gameboard

def check_horizontal_vertical(gameboard, word):
    for i, row in enumerate(gameboard):
        if word in row:
            j = row.index(word)
            return True, (word, i, j, i, j + len(word) - 1)
        
    for j in range(len(gameboard[0])):
        column = ''.join(row[j] for row in gameboard)
        if word in column:
            i = column.index(word)
            return True, (word, i, j, i + len(word) - 1, j)
        
    return False, None

def solve(gameboard, word):
    found, coords = check_horizontal_vertical(gameboard, word)
    if found:
        return coords
    return None

def main():
    gameboard = read_gameboard()
    
    print('Enter words to find or type "exit" to quit.')
    while True:
        word = input('Enter word: ').strip().lower()
        if word == 'exit':
            break
        
        coords = solve(gameboard, word)
        if coords is None:
            print(f'"{word}" not found.\n')
            continue
        
        print(f'\n"{word}" found at: ({coords[1]},{coords[2]}) to ({coords[3]},{coords[4]})\n')
        print('   ' + ' '.join(str(i % 10) for i in range(len(gameboard))))
        for i, row in enumerate(gameboard):
            line = f'{i:>2} '
            for j, letter in enumerate(row):
                if coords[1] <= i <= coords[3] and coords[2] <= j <= coords[4]:
                    line += f'{BOLD}{letter}{END} '
                else:
                    line += f'{letter} '
            print(line)
        print()

if __name__ == '__main__':
    main()
