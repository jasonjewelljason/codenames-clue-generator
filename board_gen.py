# Adapted from https://github.com/hbiede/Codenames-Board-Generator. I don't fully understand how this 
# code works. ChatGPT translated it from Ruby to Python, I added the color functionality.

import csv
import random
from colorama import Fore, Style, Back

def read_csv(file_name):
    try:
        with open(file_name, 'r') as file:
            reader = csv.reader(file)
            words = [row[0].lower() for row in reader if row]
        return words
    except FileNotFoundError:
        print(f"Sorry, the file '{file_name}' does not exist")
        exit(1)

def gen_word_board(words):
    word_board = [['' for _ in range(5)] for _ in range(5)]
    random.shuffle(words)
    first_color = random.choice(['R', 'B'])
    colors = [first_color] * 9 + ['B' if first_color == 'R' else 'R'] * 8 + ['N'] * 7 + ['X']
    random.shuffle(colors)
    #print(f"{first_color} goes first")
    for i in range(5):
        for j in range(5):
            word_board[i][j] = (words.pop(0), colors.pop(0))
    return word_board

def assign_board_tiles(board, letter, times):
    empty_indices = [(i, j) for i in range(5) for j in range(5) if not board[i][j]]
    if len(empty_indices) < times:
        print(f"Cannot fill the board with {times} empty spaces")
        exit(1)

    chosen_indices = random.sample(empty_indices, times)
    for i, j in chosen_indices:
        board[i][j] = letter

def gen_spy_board():
    spy_board = [['N' for _ in range(5)] for _ in range(5)]
    colors = ['R'] * 9 + ['B'] * 8 + ['N'] * 7 + ['X']
    random.shuffle(colors)
    for i in range(5):
        for j in range(5):
            spy_board[i][j] = colors.pop(0)
    return spy_board

def print_board(board, spy_board):
    for row, spy_row in zip(board, spy_board):
        print('|', end=' ')
        for (word, color), spy_color in zip(row, spy_row):
            if color == 'R':
                print('%-24s' % (Fore.RED + word + ' (' + str(color) + ')' + Style.RESET_ALL), end=' | ')
            if color == 'B':
                print('%-24s' % (Fore.BLUE + word + ' (' + str(color) + ')' + Style.RESET_ALL), end=' | ')
            if color == 'N':
                print('%-15s' % (word + ' (' + str(color) + ')'), end=' | ')
            if color == 'X':
                print('%-24s' % (Fore.YELLOW + word + ' (' + str(color) + ')' + Style.RESET_ALL), end=' | ')
        print()

def longest_word(board):
    longest_word_length = -1
    for line in board:
        for word in line:
            longest_word_length = max(len(word), longest_word_length)
    return longest_word_length


def combine_board(board, spy_board):
    combined_board = []
    for row_board, row_spy in zip(board, spy_board):
        combined_row = []
        for (word, _), color in zip(row_board, row_spy):
            combined_row.append((word, color))
        combined_board.append(combined_row)
    return combined_board

def get_word_color_tuples(board, spy_board):
    word_color_tuples = []
    for i in range(5):
        for j in range(5):
            word, _ = board[i][j]
            color = spy_board[i][j]
            word_color_tuples.append((word, color))
    return word_color_tuples


def output(board):
    #print('Key:')
    spy_board = gen_spy_board()
    combined_board = combine_board(board, spy_board)
    print_board(combined_board, spy_board)
    word_color_tuples = get_word_color_tuples(board, spy_board)
    #print(word_color_tuples)
    return word_color_tuples

def main():
    words = read_csv('words.csv')
    board = gen_word_board(words)
    return output(board)

if __name__ == '__main__':
    main()
