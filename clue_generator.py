print('Importing...')
from embeddings import Embeddings
import board_gen
from nltk.stem import WordNetLemmatizer
from colorama import Fore, Back, Style
print('Imports complete!')

# Making list of functor words (bad for clues)
with open("functors.txt") as f:
    functors = f.readlines()
functors = [x.strip() for x in functors]

def top_n(my_list, n, reverse=True):
    # Given a list of tuples (word, score), sorts by score and returns the top n tuples
    # Returns:
    #   list: a list of the top n tuples
    my_list.sort(key=lambda a: a[1], reverse=reverse)
    return my_list[:n]

def generate_random_board():
    # Updates the board variable to be a random board generated by board_gen.py
    global board
    board = board_gen.main()
    return

def find_midpoint(embeddings, word1, word2, n=1):
    # Unused in the final program, this finds the word closest to the midpoint of two other words
    midpoint_vector = (embeddings.__getitem__(word1) + embeddings.__getitem__(word2)) / 2
    similarity_to_midpoint = []
    counter = 1
    for word in embeddings.embeddings.keys():
        similarity_to_midpoint.append((word, embeddings.cosine_similarity(word, midpoint_vector)))
        print(counter, end='\r')
        counter += 1
    return top_n(similarity_to_midpoint, n)

def is_board_valid(embeddings, board):
    # Checks to see if input board is in a valid format, and that every word has an embedding
    # Returns bool
    if type(board) != list:
        print('Wrong format... (not a list)')
        return False
    for square in board:
        if type(square) != tuple:
            print("Wrong format... board must be made of tuples")
            return False
        if square[1] != 'R' and square[1] != 'B' and square[1] != 'X' and square[1] != 'N':
            print('Invalid colors- must be R, B, N, or X')
            return False
        if len(square) != 2:
            print('Tuple length must be 2')
            return False
        if square[0] not in embeddings.embeddings.keys():
            print(square[0], 'has no vector')
            return False
    
    return True

def is_clue_valid(clue, board):
    # Checks to see if a clue is valid
    # Returns bool
    lemmatizer = WordNetLemmatizer()
    clue_lemma = lemmatizer.lemmatize(clue)

    for square in board:                        # does the clue share a lemma with a word on the board
        tile_lemma = lemmatizer.lemmatize(square[0])
        if tile_lemma == clue_lemma:
            return False
        if tile_lemma.startswith(clue_lemma) or clue_lemma.startswith(tile_lemma):
            return False
    
    if clue in functors:                        # is the clue a functor word
        return False
    
    return True


def score_clue(embeddings, board, clue, team, method=1):
    # This is the main function of the program- given a board, clue, and team, it scores the clue
    # for that team. There are two methods, but method 1 was just used in testing; method 2 is the
    # one that I use.
    if method == 1:
        # This is a simple method: it calculates similarity to every word on the board,
        # and adds up scores for all red and all blue. Does not consider assassin.
        bluescore = 0.0
        redscore = 0.0
        redcount, bluecount = 0,0
        for square in board:
            if square[1] == 'R':
                redscore += embeddings.cosine_similarity(square[0], clue)
                redcount += 1
            if square[1] == 'B':
                bluescore += embeddings.cosine_similarity(square[0], clue)
                bluecount += 1
        if team == 'B':
            return (bluescore/bluecount) - (redscore/redcount)
        if team == 'R':
            return (redscore/redcount) - (bluescore/bluecount)

    if method == 2:
        # Score is basically how many of the same color are closer than any of the other color (or assassin)
        # My method of scoring could certainly be better, but it's what I landed on after a hefty 
        # amount of trial and error
        score = 0
        list_of_closest = []
        # Make a list of the most similar board words to the clue word
        for square in board:
            list_of_closest.append((square[0], embeddings.cosine_similarity(square[0], clue), square[1]))
        for word in top_n(list_of_closest, n=len(board)):       # go through the closest words one by one
            if word[2] == team and word[1] > 0.47:      # if the color matches and the word is close 'enough'; .47 is what I landed on
                score += 1                              # add 1 and also add a tiny amount proportional to the similarity, to give an edge to the more similar of otherwise identically scored clues
                score += word[1] / 10
            elif (word[2] == 'N'):                      # if it's no color or the same color but dissimilar, keep looking
                score -= 0.5                            # but penalize, b/c we don't want neutral words to be close
            elif (word[2] == team):                     # same color but doesn't meet threshold
                score += word[1] / 10                   # don't add a whole point, but still favor more similar words
            elif (word[2] == 'X'):                      # if it's the assassin
                score -= 1                              # penalize; we really don't want the assassin close to the clue
                break
            else:                                       # if it's the opposite color
                score -= word[1] / 10                   # subtract a little based on how close it is; we want to favor clues that are farther from the opposite team
                break
        
        return score

def generate_clue(embeddings, board, team, method=1, n=1):
    # For a board and team, scores all possible clues and returns the top clue
    clues = []
    counter = 1
    print('Words checked (out of 108947):')
    for word in embeddings.embeddings.keys():
        score = score_clue(embeddings, board, word, team, method)
        clues.append((word, score))
        print(counter, end='\r')
        counter += 1
    print('Done!     ')
    return top_n([x for x in clues if is_clue_valid(x[0], board)], n)

def get_clue_number(embeddings, board, clue, team):
    # This calculates the number that should be given alongside a clue.
    # This just looks at the most similar board words to the clue word, and counts every
    # same team word that is more similar than any opposite team word / assassin.
    number = 0
    sims = []
    for square in board:
        sims.append((square[0], embeddings.cosine_similarity(clue, square[0]), square[1]))
    for x in top_n(sims, n=len(board)):
        if x[2] == team:
            number += 1
        elif x[2] == 'N':
            pass
        else:
            break
    return number
    
def remove_squares(board):
    # This is for the user interface; after a turn happens in a game the user can remove words from the board
    wordlist = [x[0] for x in board]
    inword = ''
    while inword != 'done':
        inword = input("Which word would you like to remove from the board? Enter 'done' when done. ")
        if inword in wordlist:
            for square in board:
                if square[0] == inword:
                    board.remove(square)
        else:
            if inword != 'done':
                print(inword, "isn't on the board.")

    # prints remaining words
    print('Remaining words: ', end='')
    for square in board:
        if square[1] == 'R':
            print(Fore.RED + square[0] + Style.RESET_ALL, end=' ')
        elif square[1] == 'B':
            print(Fore.BLUE + square[0] + Style.RESET_ALL, end=' ')
        elif square[1] == 'X':
            print(Fore.YELLOW + square[0] + Style.RESET_ALL, end=' ')
        else:
            print(square[0], end=' ')
    print('')
    return board

def get_input_board(embeddings):
    # Gives the user a way to input their own board
    global board
    board = []
    inword,incolor = '',''
    print("Type 'done' when done")
    while len(board) < 25 and inword != 'done':     # stops when 25 words have been added or user inputs 'done'
        inword = input('Add word: ').lower()
        if inword != 'done':
            incolor = input('What color is that word? (R, B, N, or X) ').upper()
            board.append((inword, incolor))
    if not is_board_valid(embeddings, board):       # makes sure you don't enter an invalid board
        board = []
        if input('Try again? (y/n) ') == 'y':
            get_input_board(embeddings)

    # prints board
    print('Board: ', end='')
    for square in board:
        if square[1] == 'R':
            print(Fore.RED + square[0] + Style.RESET_ALL, end=' ')
        elif square[1] == 'B':
            print(Fore.BLUE + square[0] + Style.RESET_ALL, end=' ')
        elif square[1] == 'X':
            print(Fore.YELLOW + square[0] + Style.RESET_ALL, end=' ')
        else:
            print(square[0], end=' ')
    print('')

def initiate_board():
    # Asks the user whether to make random board or input one, then does that
    board_method = input('Generate random board, or input one? (random / input) ').lower()
    if board_method == 'random':
        generate_random_board()
    elif board_method == 'input':
        get_input_board(embeddings)
    else:
        print('Invalid input')
        initiate_board()

def request_action():
    # This runs after an action in the main loop
    # Prompts the user for what to do next
    # Four options:
    #   Remove: calls remove_squares
    #   Check:  lets the user check a clue word to see what the most similar board words are
    #   Clue:   generates a clue
    #   Quit:   quits the whole program
    global quit
    global board
    quit = False
    nextaction = ''
    while nextaction == '':
        nextaction = input('(remove / check / clue / quit) ')
        if nextaction == 'remove':
            board = remove_squares(board)
            nextaction = ''
        elif nextaction == 'check':
            checkword = ''
            while checkword != 'x':
                checkword = input('What word would you like to check? (x to exit check mode) ')
                if checkword != 'x' and checkword in embeddings.embeddings.keys():
                    mylist = top_n([(square[0], embeddings.cosine_similarity(square[0], checkword), square[1]) for square in board], n=25)
                    for word in mylist:
                        if word[2] == 'R':
                            print(Fore.RED + word[0] + Style.RESET_ALL, word[1])
                        elif word[2] == 'B':
                            print(Fore.BLUE + word[0] + Style.RESET_ALL, word[1])
                        elif word[2] == 'X':
                            print(Fore.YELLOW + word[0] + Style.RESET_ALL, word[1])
                        else:
                            print(word[0], word[1])
            nextaction = ''
        elif nextaction == 'quit':
            quit = True
        elif nextaction == 'clue':
            # The code for this is in the main loop, I probably should reorganize this when I get the chance
            pass
        else:
            print('Invalid input- try again')
            nextaction = ''

embeddings = Embeddings()
initiate_board()

# Main loop: this runs request_action until the board is empty or the user quits
while len(board) > 0:

    request_action()
    if quit:
        break
    
    # Generate a clue
    team = None
    while team != 'R' and team != 'B':          # Input which team to generate for
        team = input('Generate a clue for which team? (R,B): ').upper()
    clue = (generate_clue(embeddings, board, team, n=1, method=1))[0][0]
    if team  == 'R':
        print(Fore.RED + clue + ' ' + str(get_clue_number(embeddings, board, clue, team)) + Style.RESET_ALL)
    if team  == 'B':
        print(Fore.BLUE + clue + ' ' + str(get_clue_number(embeddings, board, clue, team)) + Style.RESET_ALL)