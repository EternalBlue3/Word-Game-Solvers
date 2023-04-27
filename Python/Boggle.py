import time

X, Y = 4, 4

def get_grid(grid):
    return {(index // X, index % Y): str(value) for index, value in enumerate(grid)}

def get_neighbours():
    neighbours = {}
    for position in grid:
        x, y = position
        positions = [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x + 1, y),
                     (x + 1, y + 1), (x, y + 1), (x - 1, y + 1), (x - 1, y)]
        neighbours[position] = [p for p in positions if 0 <= p[0] < X and 0 <= p[1] < Y]
    return neighbours

def path_to_word(path):
    return ''.join([grid[p] for p in path])

def search(path):
    word = path_to_word(path)
    if word not in stems:
        return
    if word in dictionary:
        paths.append(path)
    for next_pos in neighbours[path[-1]]:
        if next_pos not in path:
            search(path + [next_pos])

def get_dictionary():
    stems, dictionary = {}, {}
    with open('wordlist.txt') as f:
        for word in f:
            word = word.strip().upper()
            dictionary[word] = None

            for i in range(len(word)):
                stem = word[:i + 1]
                if stem not in stems:
                    stems[stem] = None

    return dictionary, stems

def get_words():
    for position in grid:
        search([position])
    return [path_to_word(p) for p in paths]

def print_grid(grid):
    print('\n'.join([' '.join(grid[x, y] for y in range(Y)) for x in range(X)]) + '\n')

def word_score(word):
    score = {1: 0, 2: 0, 3: 1, 4: 1, 5: 2, 6: 3, 7: 5}
    return score.get(len(word), 11)

# Get board from user
board = ' '.join(input("Enter the grid values: ").upper().split()).split()

# Start timing
start = time.time()

grid = get_grid(board)
neighbours = get_neighbours()
dictionary, stems = get_dictionary()
paths = []
print_grid(grid)

wordset = set(get_words())
points = sum(word_score(word) for word in wordset)

print("Time taken:",time.time()-start)
print("Found "+str(len(wordset)) + " words:\n")
print("Word   Points")
print("--------------")
for item in sorted(wordset):
    print(item+"\t"+str(word_score(item)))
print("--------------")
print(points, "Points in total")
