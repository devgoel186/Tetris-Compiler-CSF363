In our first stage submission we have pushed the following:
1. PDF Report
2. game.ttr, a sample game in our language. This depticts the functionalities, syntax, etc.
3. tetris_lexer.py, in this implementation, we parse arrays and matrices and return them (instead of returning induvidual character tokens)
4. tetris_lexer_notParsingArrays, we return induvidual character tokens for Matrices and Arrays here

For more details on 3. and 4., please see our report.

To test, open a terminal (or conda prompt):
python tetris_lexer.py

It will wait for filename input, provide - game.ttr