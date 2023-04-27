import time, random, sys, string, itertools

words = input("Enter current known letters (ex. H_LL_; Unknown letters = _): ").lower().split(' ')
unused = set(input("Enter letters that are not used: ").lower())

for word in words:
    if any(char in unused or char in string.punctuation or char.isnumeric() for char in word.replace('_','').replace(' ','')):
        print("Unused letters, numbers, and symbols cannot be used as an input word. Try reentering with correct values.")
        sys.exit()

with open("wordlist.txt") as file:
    wordlist = {x.strip().lower() for x in file}

def get_valid_words(word,wordlist):
    word_length = len(word)
    valid_words = [x for x in wordlist if not any(char in unused for char in x) and len(x) == word_length]
    second_valid_words = [x for x in valid_words if not any(word[y] == '_' and x[y] in word for y in range(word_length))]
    return [x for x in second_valid_words if all(a == b or a == '_' for a, b in zip(word, x))]

def get_probable_guesses(words,valid_words):
    letters = []
    for x in itertools.product(*valid_words):
        appended = set()
        for y in ''.join(x):
            if not any(y in word for word in words) and y not in appended:
                letters.append(y)
                appended.add(y)

    letter_counts = {}
    for letter in letters:
        if letter in letter_counts:
            letter_counts[letter] += 1
        else:
            letter_counts[letter] = 1

    sorted_letter_counts = sorted(letter_counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_letter_counts

potential_words_list = []
total_combinations = 1
for x in words:
    valid_words = get_valid_words(x,wordlist)
    total_combinations *= len(valid_words)
    potential_words_list.append(valid_words)
        
probable_guesses = get_probable_guesses(words,potential_words_list)
    
print("\nLetters to guess:\n----------------------------------------")
num = 1
for letter, count in probable_guesses:
    print(f"  {str(num)}. '{letter}' with probability {str(count)}/{str(total_combinations)}")
    num += 1

for x in range(len(words)):
    print(f"\nHere are the possible resulting words for input #{str(x+1)}:\n----------------------------------------")
    output_words = potential_words_list[x]
    if len(output_words) > 25:
        for x in range(25):
            print("  ",output_words[x])
        print("...Output truncated to first 25 words...")
    else:
        for x in output_words:
            print("  ",x)
