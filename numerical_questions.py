import tetris_lexer
def parse():
    print("Question 1.ii and 1.iii")
    print(f'If we include comment as a token, it is: {len(tetris_lexer.tokens) - 1}, if not it is {len(tetris_lexer.tokens) - 2}\n')

    print("Question 1.vi")
    print(f'{len(tetris_lexer.reserved)} is the number of token types that are the lexemes themselves.')
                  
if __name__ == "__main__":
    parse()
