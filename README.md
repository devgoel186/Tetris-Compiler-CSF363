# Tetris

This project build a complete Tetris Game language. Our language is based on the syntax of C-type programs, i.e., C, C++, Java. For our compiler, we use "lex" lexical analyzer and "yacc" parser tools for Python from the **PLY** library.

Some of the offered Tetris primitives in our language are:

- Game Levels
- A variable sized board / playing grid
- Tetrominoes (user-defined pieces / blocks for tetris)
- Color of tetrominoes
- Speed and sequence of tetrominoes
- Programmable randomization
- and many more...

To get a detailed idea of our Tetris language, please refer to Stage1 and Stage2 report included in the **Report** folder of the repository.

The compiler was developed in two stages. Listed below are some filenames and the component / functionality they handle in the compiler, grouped by the stages in which they were developed. You can consider the files in Stage 2 group to be enhanced / improved versions of our previous code:

1. PDF Report - A detailed description of the language and implementation of the compiler.
2. `game.ttr`, a sample game in our language. This depicts the functionalities, syntax, etc.
3. `tetris_lexer.py` - Implementation Type-1. Here, we parse arrays and matrices and return them (instead of returning induvidual character tokens)
4. `tetris_lexer_notParsingArrays` - Implementation Type-2. Here, we return induvidual character tokens for Matrices and Arrays.
5. `tetris_compiler.py` - The entire compiler bundled as one with the lexer and parser.
6. `Level.py` - Defines the logic of levels in our game.
7. `game_config.py` - Declares the configurations for the game.
8. `game.py` - The Tetris Game. We run our compiler with the game which parses the user's declared configurations and converts them to moving pieces in the game.
9. `game.ttr` - A sample
10. `game_final.ttr`

To test, open a terminal (or conda prompt):
`python tetris_lexer.py`

It will wait for filename input, provide - `game.ttr`
