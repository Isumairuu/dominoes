# Write your code here
import random


def create_set() -> list:
    """ Create domino set"""
    dominos = []
    for i in range(7):
        for j in range(7):
            if [j, i] in dominos:
                continue
            else:
                dominos.append([i, j])
    random.shuffle(dominos)
    return dominos


def distribute_pieces() -> (list, list, list):
    """ Distribute pieces to stock pieces , player pieces , computer pieces"""
    domino_set = create_set()
    stock = domino_set[:14]
    player_set = domino_set[14:21]
    computer_set = domino_set[21:]
    return stock, player_set, computer_set


def place_starting_piece(player_dominos: list, computer_dominos: list) -> list:
    """ Set starting piece and starting player"""
    dominos = player_dominos + computer_dominos
    global stock_pieces, player_pieces, computer_pieces, status
    starting_piece = max(dominos)
    if starting_piece in player_dominos:
        player_dominos.pop(player_dominos.index(starting_piece))
        status = "Computer"
    elif starting_piece in computer_dominos:
        computer_dominos.pop(computer_dominos.index(starting_piece))
        status = "Player"
    else:
        stock_pieces, player_pieces, computer_pieces = distribute_pieces()
        starting_piece = place_starting_piece(player_pieces, computer_pieces)
    return [starting_piece]


def player_move():
    """Get player input and check if the move is legal"""
    while True:
        move = input()
        if move.lstrip("-").isnumeric():
            move = int(move)
            if move in range(-len(player_pieces) - 1, len(player_pieces) + 1):
                if move > 0:
                    piece = player_pieces[move - 1]
                    if piece[0] == domino_snake[-1][1]:
                        domino_snake.append(player_pieces.pop(move - 1))
                        break
                    elif piece[1] == domino_snake[-1][1]:
                        piece = player_pieces.pop(move - 1)
                        piece.reverse()
                        domino_snake.append(piece)
                        break
                    else:
                        print("Illegal move. Please try again.")
                elif move < 0:
                    move = abs(move)
                    piece = player_pieces[move - 1]
                    if piece[1] == domino_snake[0][0]:
                        domino_snake.insert(0, player_pieces.pop(move - 1))
                        break
                    elif piece[0] == domino_snake[0][0]:
                        piece = player_pieces.pop(move - 1)
                        piece.reverse()
                        domino_snake.insert(0, piece)
                        break
                    else:
                        print("Illegal move. Please try again.")
                elif move == 0:
                    if len(stock_pieces) > 0:
                        player_pieces.append(stock_pieces.pop())
                        break
            else:
                print("Invalid input. Please try again.")
        else:
            print("Invalid input. Please try again.")


def computer_move():
    """Compute computer's next best move"""
    global status
    while True:
        move = input()
        if move == "":
            computer_count = computer_ai()
            for _ in range(len(computer_count)):
                move = computer_pieces.index(list(max(computer_count, key=computer_count.get)))
                piece = computer_pieces[move]
                if piece[0] == domino_snake[-1][1]:
                    domino_snake.append(computer_pieces.pop(move))
                    break
                elif piece[1] == domino_snake[-1][1]:
                    piece = computer_pieces.pop(move)
                    piece.reverse()
                    domino_snake.append(piece)
                    break
                elif piece[1] == domino_snake[0][0]:
                    domino_snake.insert(0, computer_pieces.pop(move))
                    break
                elif piece[0] == domino_snake[0][0]:
                    piece = computer_pieces.pop(move)
                    piece.reverse()
                    domino_snake.insert(0, piece)
                    break
                else:
                    computer_count.pop(max(computer_count, key=computer_count.get))
            if len(computer_count) == 0:
                if len(stock_pieces) > 0:
                    computer_pieces.append(stock_pieces.pop())
            break
        else:
            print("Invalid input. Please try again.")


def computer_ai() -> dict:
    """Return a dict for computer moves scored by counting the number
     of occurrences of 0-6 in computer hand and  in the snake"""
    snake_count = {}
    computer_count = {}
    for i in range(7):
        counter = 0
        for piece in domino_snake:
            for j in (0, 1):
                if i == piece[j]:
                    counter += 1
        for piece in computer_pieces:
            for j in (0, 1):
                if i == piece[j]:
                    counter += 1
        snake_count[i] = counter
    for piece in computer_pieces:
        computer_count[tuple(piece)] = snake_count[piece[0]] + snake_count[piece[1]]
    return computer_count


def game_advancement():
    """Updates the game advancement status"""
    global status
    while len(computer_pieces) > 0 and len(player_pieces) > 0:
        output_field()
        if draw_condition():
            status = "Draw"
            break
        elif status == "Player":
            player_move()
            status = "Computer"
        elif status == "Computer":
            computer_move()
            status = "Player"
    if len(computer_pieces) == 0:
        status = "Lose"
    elif len(player_pieces) == 0:
        status = "Win"


def draw_condition() -> bool:
    """Check if draw condition is met"""
    counter = 0
    if domino_snake[0][0] == domino_snake[-1][1]:
        number = domino_snake[0][0]
        for piece in domino_snake:
            for j in (0, 1):
                if number == piece[j]:
                    counter += 1
    if counter == 8:
        return True
    return False


def output_field():
    """ Output game field """
    print("=" * 70)
    print("Stock size:", len(stock_pieces))
    print("Computer pieces:", len(computer_pieces), "\n")
    output_snake()
    print("\nYour pieces:")
    output_player_pieces()
    output_status()


def output_player_pieces():
    """Output player pieces"""
    for i in range(len(player_pieces)):
        print(f"{i + 1}:{player_pieces[i]}")


def output_snake():
    """Snake print formatting"""
    if len(domino_snake) > 6:
        a = domino_snake[:3]
        b = domino_snake[-3:]
        print(*a, "...", *b)
    else:
        print(*domino_snake)


def output_status():
    """Output the correct message depending on the game status"""
    if status == "Player":
        print("Status: It's your turn to make a move. Enter your command.")
    elif status == "Computer":
        print("Status: Computer is about to make a move. Press Enter to continue...")
    elif status == "Win":
        print("Status: The game is over. You won!")
    elif status == "Lose":
        print("Status: The game is over. The computer won!")
    elif status == "Draw":
        print("Status: The game is over. It's a draw!")


status = ""
stock_pieces, player_pieces, computer_pieces = distribute_pieces()
domino_snake = place_starting_piece(player_pieces, computer_pieces)
game_advancement()
output_field()
