import tkinter as tk
from game_logic import *

def start_game():
    global numbers, total_score, bank, current_turn
    current_turn = starter_var.get()
    total_score = 0
    bank = 0
    numbers = generate_number_list(15)
    update_display()
    update_moves()

def update_display():
    numbers_label.config(text="Numbers: " + str(numbers))
    score_label.config(text="Score: " + str(total_score))
    bank_label.config(text="Bank: " + str(bank))
    turn_label.config(text="Turn: " + current_turn)

root = tk.Tk()
root.title("Number Game")
root.configure(bg="#1e1e2e")
root.geometry("500x650")
root.resizable(False, False)

tk.Label(root, text="🎮 Number Game", font=("Arial", 20, "bold"), bg="#1e1e2e", fg="#cdd6f4").pack(pady=10)

# Zone 1 - Configuration
config_frame = tk.Frame(root, bg="#313244", pady=10)
config_frame.pack(fill="x", padx=20, pady=5)

starter_var = tk.StringVar(value="Human")
tk.Label(config_frame, text="Who starts?", bg="#313244", fg="white", font=("Arial", 11, "bold")).pack()
tk.Radiobutton(config_frame, text="Human", variable=starter_var, value="Human", bg="#313244", fg="white", selectcolor="#1e1e2e").pack()
tk.Radiobutton(config_frame, text="AI", variable=starter_var, value="AI", bg="#313244", fg="white", selectcolor="#1e1e2e").pack()

algo_var = tk.StringVar(value="Minimax")
tk.Label(config_frame, text="Algorithm?", bg="#313244", fg="white", font=("Arial", 11, "bold")).pack()
tk.Radiobutton(config_frame, text="Minimax", variable=algo_var, value="Minimax", bg="#313244", fg="white", selectcolor="#1e1e2e").pack()
tk.Radiobutton(config_frame, text="Alpha-Beta", variable=algo_var, value="Alpha-Beta", bg="#313244", fg="white", selectcolor="#1e1e2e").pack()

tk.Button(config_frame, text="Start Game", bg="#a6e3a1", fg="#1e1e2e", font=("Arial", 12, "bold"), command=start_game).pack(pady=8)

# Zone 2 - État du jeu
state_frame = tk.Frame(root, bg="#313244", pady=10)
state_frame.pack(fill="x", padx=20, pady=5)

numbers_label = tk.Label(state_frame, text="Numbers: ", font=("Arial", 11), bg="#313244", fg="#cdd6f4")
numbers_label.pack()
score_label = tk.Label(state_frame, text="Score: ", font=("Arial", 11), bg="#313244", fg="#cdd6f4")
score_label.pack()
bank_label = tk.Label(state_frame, text="Bank: ", font=("Arial", 11), bg="#313244", fg="#cdd6f4")
bank_label.pack()
turn_label = tk.Label(state_frame, text="Turn: ", font=("Arial", 11, "bold"), bg="#313244", fg="#f9e2af")
turn_label.pack()

move_buttons = []

def update_moves():
    for btn in move_buttons:
        btn.destroy()
    move_buttons.clear()
    if current_turn == "Human" and numbers:
        moves = get_legal_moves(numbers)
        for move in moves:
            btn = tk.Button(
                actions_frame,
                text=str(move),
                bg="#89b4fa", fg="#1e1e2e",
                font=("Arial", 10, "bold"),
                command=lambda m=move: human_move(m)
            )
            btn.pack(side="left", padx=5, pady=5)
            move_buttons.append(btn)
    elif current_turn == "AI" and numbers:
        root.after(500, ai_move)

def human_move(move):
    global numbers, total_score, bank, current_turn
    numbers, total_score, bank = simulate_move(numbers, total_score, bank, move)
    current_turn = "AI"
    update_display()
    check_game_over()
    if numbers:
        update_moves()

def ai_move():
    global numbers, total_score, bank, current_turn
    algo = algo_var.get()
    if algo == "Minimax":
        move = ai_choose_move_minimax(numbers, total_score, bank)
    else:
        move = ai_choose_move_alphabeta(numbers, total_score, bank)
    numbers, total_score, bank = simulate_move(numbers, total_score, bank, move)
    current_turn = "Human"
    update_display()
    check_game_over()
    if numbers:
        update_moves()

def check_game_over():
    if not numbers:
        winner = get_winner(total_score, bank)
        if winner == "human":
            result_label.config(text=" Human wins!", fg="#a6e3a1")
        elif winner == "ai":
            result_label.config(text="AI wins!", fg="#f38ba8")
        else:
            result_label.config(text=" Draw!", fg="#f9e2af")
        new_game_btn.pack(pady=5)

# Zone 3 - Actions
actions_frame = tk.Frame(root, bg="#1e1e2e")
actions_frame.pack(pady=10)

# Zone 4 - Résultat
result_frame = tk.Frame(root, bg="#1e1e2e")
result_frame.pack()
result_label = tk.Label(result_frame, text="", font=("Arial", 14, "bold"), bg="#1e1e2e")
result_label.pack()
new_game_btn = tk.Button(result_frame, text="New Game", bg="#a6e3a1", fg="#1e1e2e", font=("Arial", 11, "bold"), command=start_game)

root.mainloop()