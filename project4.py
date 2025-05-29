# project4.py
#
# ICS 33 Spring 2025
# Project 4: Still Looking for Something

from parsing import *

def read_inp():
    inp_file = input()
    sentences = int(input())
    start_var = input()
    return inp_file, sentences, start_var

def generate_sentence(grammar, start_var):
    pieces = list(grammar.generate(start_var))
    return ' '.join(pieces)

def main() -> None:
    try:
        inp_file, sentences, start_var = read_inp()
        res = parse_file(inp_file)

        for x in range(sentences):
            sentence = generate_sentence(res, start_var)
            print(sentence)
    except Exception as e:
        return e


if __name__ == '__main__':
    main()
