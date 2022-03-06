# dominoes

Implementation of Jetbrains Academy project Dominoes

## Game Rules

As you might know, a domino is a playing piece that is characterized by the two numbers written on it. The numbers are
integers and can range from 0 to 6. A single domino piece has no orientation, so, a full domino set (that includes all
the possible pairs of numbers) will have 28 unique dominoes.

To play domino, you need a full domino set and at least two players. In this project, the game is played by you and the
computer.

At the beginning of the game, each player is handed 7 random domino pieces. The rest are used as stock (the extra
pieces).

To start the game, players determine the starting piece. The player with the highest domino or the highest
double (`[6,6]` or `[5,5]` for example) will donate that domino as a starting piece for the game. After doing so, their
opponent will start the game by going first. If no one has a double domino, the pieces are reshuffled and redistributed.

Below is an example of the game field:

```
======================================================================
Stock size: 14
Computer pieces: 6

[6, 6]

Your pieces:
1:[0, 6]
2:[5, 5]
3:[4, 4]
4:[4, 6]
5:[0, 1]
6:[0, 5]
7:[1, 6]

Status: It's your turn to make a move. Enter your command.
```

In dominoes, you can make a move by taking one of the following actions:

Select a domino and place it on the right side of the snake. Select a domino and place it on the left side of the snake.
Take an extra piece from the stock (if it's not empty) and skip a turn. To make a move, the player has to specify the
action they want to take. In this project, the actions are represented by integer numbers in the following manner:
`{side_of_the_snake (+/-), domino_number (integer)}` or `{0}`.

For example:\
`-6` : Take the sixth domino and place it on the left side of the snake. \
`6 `  : Take the sixth domino and place it on the right side of the snake. \
`0 `  : Take an extra piece from the stock (if it's not empty) and skip a turn or simply skip a turn if the stock is
already empty by this point.

*According to the rules*, the numbers on the ends of the two neighboring dominoes must match each other. This rule can
also be described as a set of two requirements:

    1. A player cannot add a domino to the end of the snake if it doesn't 
    contain the matching number. 
    2. The orientation of the newly added domino ensures that the matching 
    numbers are neighbors.

For example, consider the following situation:

We have a `[3,4],[4,4],[4,2]` snake and a `[1,2]` domino. The domino cannot be added to the left side of the snake
because there is no 3 in `[1,2]`. However, the domino can be added to the right side of the snake because `[1,2]`
contains a 2. If we were to place the domino on the right side of the snake, we would have to reorient
it: `[3,4],[4,4],[4,2]
,[2,1]`.

### AI

The primary objective of the AI is to determine which domino is the least favorable and then get rid of it. To reduce
your chances of skipping a turn, one must increase the diversity of their pieces. For example, it's unwise to play the
only domino that has a 3, unless there's nothing else that can be done. Using this logic, the AI evaluates each domino
in possession, based on the rarity. Dominoes with rare numbers will get lower scores, while dominoes with common numbers
will get higher scores.

The AI uses the following algorithm to calculate the score:

    1- Count the number of 0's, 1's, 2's, etc., in the computer hand, 
    and in the snake. Each domino in the hand receives a score equal 
    to the sum of appearances of each of its numbers. 

    2- The AI will attempt to play the domino with the largest score, 
    trying both the left and the right sides of the snake. If the rules 
    prohibit this move, the AI will move down the score list and try 
    another domino. The AI will skip the turn if it runs out of options.

### Examples

The greater-than symbol followed by a space (> ) represents the user input. Note that it's not part of the input.

#### Example 1

*Invalid move*

```
====================================================================== 
Stock size: 14 Computer pieces: 6

[6, 6]

Your pieces:
1:[0, 5]
2:[1, 5]
3:[2, 4]
4:[2, 6]
5:[0, 1]
6:[1, 6]
7:[5, 6]

Status: It's your turn to make a move. Enter your command.
> 5 Illegal move. Please try again.
>
```

#### Example 2

_Valid move (with corrected domino orientation)_

```
====================================================================== 
Stock size: 14 Computer pieces: 6

[6, 6]

Your pieces:
1:[0, 6]
2:[5, 5]
3:[4, 4]
4:[4, 6]
5:[0, 1]
6:[0, 5]
7:[1, 6]

Status: It's your turn to make a move. Enter your command.
> 7 
> 
====================================================================== 
Stock size: 14 Computer pieces: 6

[6, 6][6, 1]

Your pieces:
1:[0, 6]
2:[5, 5]
3:[4, 4]
4:[4, 6]
5:[0, 1]
6:[0, 5]

Status: Computer is about to make a move. Press Enter to continue...
>
```