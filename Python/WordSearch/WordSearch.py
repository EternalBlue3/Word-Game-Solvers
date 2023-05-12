import sys, time

END = '\033[0m'
RED = '\033[31m'

def read_gameboard():
    try:
        with open('game.txt', 'r') as f:
            gameboard = [row.strip().lower() for row in f.readlines()]
        return gameboard
    except FileNotFoundError:
        print("Could not find the game file. Please create a file called \"game.txt\" in the same directory as this solver.")
        sys.exit(1)

def check_dir(gameboard, word, direction, lengthx, lengthy):
    dx, dy = direction
    for y in range(lengthy):
        for x in range(lengthx):
            match = True
            for i in range(len(word)):
                xi, yi = x + i * dx, y + i * dy
                if not (0 <= xi < lengthx and 0 <= yi < lengthy) or gameboard[yi][xi] != word[i]:
                    match = False
                    break
            if match:
                return [(x + i * dx, y + i * dy) for i in range(len(word))]
    return None
    
def find_word(gameboard, word):
    dirs = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]
    lengthx, lengthy = len(gameboard[0]), len(gameboard)
    for direction in dirs:
        coords = check_dir(gameboard, word, direction, lengthx, lengthy)
        if coords is not None:
            return True, coords
    return False, None

def main():
    gameboard = read_gameboard()

    print('Enter words to find or type "exit" to quit.')
    while True:
        word = input('Enter word: ').strip().lower()
        if word == 'exit':
            break

        start = time.time()
        found, coords = find_word(gameboard, word)
        end = time.time()
        
        if coords is None:
            print(f'"{word}" not found.\n')
            continue

        coord_set = set(coords)
        print(f'\n"{word}" found at coords: {coords}\n')
        print('   ' + ' '.join(str(i % 10) for i in range(len(gameboard[0]))))
        for i, row in enumerate(gameboard):
            line = f'{i:>2} '
            for j, letter in enumerate(row):
                if (j, i) in coord_set:
                    line += f'{RED}{letter}{END} '
                else:
                    line += f'{letter} '
            print(line)
        print(f"\nSearch took {end-start}s to complete.\n")

if __name__ == '__main__':
    main()
