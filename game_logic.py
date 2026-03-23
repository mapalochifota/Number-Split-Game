import random
import json
import os


def generate_number_list(length):
    return [random.choice([1, 2, 3, 4]) for _ in range(length)]


def heuristic_score(total_score, bank, maximizing_player=True):
    if total_score % 2 == 0 and bank % 2 == 0:
        return +10 if not maximizing_player else -10 
    elif total_score % 2 == 1 and bank % 2 == 1:
        return -10 if not maximizing_player else +10
    else:
        return 0  # draw


def get_legal_moves(numbers_list):
    moves = []
    for n in set(numbers_list):
        moves.append(("take", n))
    if 2 in numbers_list:
        moves.append(("split2", 2))
    if 4 in numbers_list:
        moves.append(("split4", 4))
    return moves


def simulate_move(numbers_list, total_score, bank, move):
    new_numbers = numbers_list.copy()
    new_total = total_score
    new_bank = bank

    if move[0] == "take":
        new_numbers.remove(move[1])
        new_total += move[1]
    elif move[0] == "split2":
        new_numbers.remove(2)
        new_numbers.extend([1, 1])
        new_bank += 1
    elif move[0] == "split4":
        new_numbers.remove(4)
        new_numbers.extend([2, 2])
        new_total += 2

    return new_numbers, new_total, new_bank


def alpha_beta(numbers_list, total_score, bank, depth, alpha, beta, maximizing):
    if depth == 0 or not numbers_list:
        return heuristic_score(total_score, bank, maximizing)

    legal_moves = get_legal_moves(numbers_list)

    if maximizing:
        max_eval = -float('inf')
        for move in legal_moves:
            new_numbers, new_total, new_bank = simulate_move(numbers_list, total_score, bank, move)
            eval = alpha_beta(new_numbers, new_total, new_bank, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in legal_moves:
            new_numbers, new_total, new_bank = simulate_move(numbers_list, total_score, bank, move)
            eval = alpha_beta(new_numbers, new_total, new_bank, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval
def minimax(numbers_list, total_score, bank, depth, maximizing):
    if depth == 0 or not numbers_list:
        return heuristic_score(total_score, bank, maximizing)

    legal_moves = get_legal_moves(numbers_list)

    if maximizing:
        max_eval = -float('inf')
        for move in legal_moves:
            new_numbers, new_total, new_bank = simulate_move(numbers_list, total_score, bank, move)
            eval = minimax(new_numbers, new_total, new_bank, depth - 1, False)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for move in legal_moves:
            new_numbers, new_total, new_bank = simulate_move(numbers_list, total_score, bank, move)
            eval = minimax(new_numbers, new_total, new_bank, depth - 1, True)
            min_eval = min(min_eval, eval)
        return min_eval

def ai_choose_move_minimax(numbers_list, total_score, bank, max_depth=3):
    best_score = -float('inf')
    best_move = None
    for move in get_legal_moves(numbers_list):
        new_numbers, new_total, new_bank = simulate_move(numbers_list, total_score, bank, move)
        score = minimax(new_numbers, new_total, new_bank, max_depth - 1, False)
        if score > best_score:
            best_score = score
            best_move = move
    return best_move

def ai_choose_move_alphabeta(numbers_list, total_score, bank, max_depth=3):
    best_score = -float('inf')
    best_move = None
    for move in get_legal_moves(numbers_list):
        new_numbers, new_total, new_bank = simulate_move(numbers_list, total_score, bank, move)
        score = alpha_beta(new_numbers, new_total, new_bank, max_depth - 1, -float('inf'), float('inf'), False)
        if score > best_score:
            best_score = score
            best_move = move
    return best_move

def get_winner(total_score, bank):
    if total_score % 2 == 0 and bank % 2 == 0:
        return "human"
    elif total_score % 2 == 1 and bank % 2 == 1:
        return "ai"
    else:
        return "draw"


def load_win_data():
    if os.path.exists("win_data.json"):
        with open("win_data.json", "r") as file:
            return json.load(file)
    return {"even_even": 0, "odd_odd": 0, "draw": 0}


def save_win_data(data):
    with open("win_data.json", "w") as file:
        json.dump(data, file, indent=4)
def main():
    print("Welcome to the Number Game!")

    # 1. Ask for length
    while True:
        try:
            length = int(input("Enter length (15-20): "))
            if 15 <= length <= 20:
                break
            else:
                print("Please enter a number between 15 and 20.")
        except:
            print("Invalid input.")

    # 2. Generate numbers
    numbers = generate_number_list(length)

    total_score = 0
    bank = 0

    print("\nInitial list:", numbers)

    # 3. Game loop
    turn = "human"  # human starts

    while numbers:
        print("\n----------------------")
        print("Numbers:", numbers)
        print("Total score:", total_score)
        print("Bank:", bank)

        if turn == "human":
            print("\nYour turn!")

            moves = get_legal_moves(numbers)
            for i, m in enumerate(moves):
                print(f"{i}: {m}")

            while True:
                try:
                    choice = int(input("Choose move index: "))
                    if 0 <= choice < len(moves):
                        move = moves[choice]
                        break
                    else:
                        print("Invalid choice.")
                except:
                    print("Invalid input.")

            print("You played:", move)

        else:
            print("\nAI turn...")
            move = ai_choose_move_alphabeta(numbers, total_score, bank)
            print("AI played:", move)

        # Apply move
        numbers, total_score, bank = simulate_move(numbers, total_score, bank, move)

        # Switch turn
        turn = "ai" if turn == "human" else "human"

    # 4. End of game
    print("\n===== GAME OVER =====")
    print("Final total score:", total_score)
    print("Final bank:", bank)

    winner = get_winner(total_score, bank)

    if winner == "human":
        print("Winner: HUMAN (starting player)")
    elif winner == "ai":
        print("Winner: AI (second player)")
    else:
        print("Result: DRAW")


if __name__ == "__main__":
    main()