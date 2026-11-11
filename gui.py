import tkinter as tk
from word_list import get_random_word, words

# COLOR CODES
BG_COLOR = "#172033"
TITLE_COLOR = "#F8FAFC"
SUBTITLE_COLOR = "#94A3B8"
GAME_FRAME_COLOR = "#243047"
PLAY_BUTTON_COLOR = "#22C55E"
QUIT_BUTTON_COLOR = "#EF4444"

# OTHER CONSTANTS
MAX_LIVES = 6

# VARIOUS FUNCTIONS FOR THE GAME
def quit_game(event):
    window.destroy()


def play_game(event):
    global lives, hangman_index, hint, hidden_word, word_display

    lives = MAX_LIVES
    hangman_index = 0

    menu_frame.pack_forget()
    result_frame.pack_forget()
    game_over_label.pack_forget()
    victory_label.pack_forget()

    lives_label.config(text=f"♡ LIVES: {lives}")

    hint, hidden_word = get_random_word(words)
    word_display = len(hidden_word) * ["_"]

    hint_label.config(text=f"HINT: {hint}")
    word_label.config(text=" ".join(word_display))

    for letter_button in keyboard_buttons:
        letter_button.config(bg=GAME_FRAME_COLOR, fg=TITLE_COLOR)
        letter_button.bind("<Button-1>", handle_letter_guess)

    for body_part in result_hangman:
        result_canvas.itemconfigure(body_part, state="hidden")

    for gf_body_part in gf_hangman:
        gf_canvas.itemconfigure(gf_body_part, state="hidden")

    game_frame.pack(fill="both", expand=True)
    window.update_idletasks()


def draw_gallows(canvas):

    return [
        canvas.create_line(40, 220, 260, 220, width=6, fill=SUBTITLE_COLOR),
        canvas.create_line(100, 30, 100, 220, width=6, fill=SUBTITLE_COLOR),
        canvas.create_line(97, 30, 190, 30, width=6, fill=SUBTITLE_COLOR),
        canvas.create_line(170, 30, 170, 50, width=2, fill=SUBTITLE_COLOR)
    ]


def draw_hangman(canvas):

    return [
        canvas.create_oval(150, 50, 190, 90, width=4, outline=SUBTITLE_COLOR),
        canvas.create_line(170, 90, 170, 150, width=4, fill=SUBTITLE_COLOR),
        canvas.create_line(170, 100, 140, 130, width=4, fill=SUBTITLE_COLOR),
        canvas.create_line(170, 100, 200, 130, width=4, fill=SUBTITLE_COLOR),
        canvas.create_line(170, 150, 140, 180, width=4, fill=SUBTITLE_COLOR),
        canvas.create_line(170, 150, 200, 180, width=4, fill=SUBTITLE_COLOR)
    ]


def handle_letter_guess(event):
    global lives, hangman_index

    selected_letter = event.widget["text"]

    event.widget.unbind("<Button-1>")

    selected_letter_lowercase = selected_letter.lower()
    letter_found = any(char == selected_letter_lowercase for char in hidden_word)
    
    for index, char in enumerate(hidden_word):
        if char == selected_letter_lowercase:
            word_display[index] = selected_letter

    if letter_found:
        event.widget.config(bg=PLAY_BUTTON_COLOR)
    else:
        event.widget.config(bg=QUIT_BUTTON_COLOR)
        lives -= 1
        lives_label.config(text=f"♡ LIVES: {lives}")
        gf_canvas.itemconfigure(gf_hangman[hangman_index], state="normal")
        hangman_index += 1

    word_label.config(text=" ".join(word_display))

    if lives == 0 or hidden_word == "".join(word_display).lower():
        show_result()

    window.update_idletasks()


def show_result():
    game_frame.pack_forget()

    for part in result_hangman[:hangman_index]:
        result_canvas.itemconfigure(part, state="normal")

    result_word_label.config(text=hidden_word.upper())

    result_canvas.pack(pady=20)

    if lives == 0:
        game_over_label.pack(before=result_canvas, pady=(30, 10))
    else:
        victory_label.pack(before=result_canvas, pady=(30, 10))

    result_text_label.pack()
    result_word_label.pack(pady=10)

    result_buttons_frame.pack(pady=15)

    play_again_button.pack(side="left", padx=10)
    play_again_button.bind("<Button-1>", play_game)

    rf_quit_button.pack(side="left", padx=10)
    rf_quit_button.bind("<Button-1>", quit_game)

    result_frame.pack(fill="both", expand=True)


# Creating WINDOW for Hangman Game
window = tk.Tk()
window.title("HANGMAN")
window.geometry("800x600")
window.resizable(False, False)
window.configure(bg=BG_COLOR)

# INITIAL MENU
menu_frame = tk.Frame(
    window,
    bg=BG_COLOR
)
menu_frame.pack(fill="both", expand=True)

# Label for TITLE
menu_title = tk.Label(
    menu_frame,
    text="HANGMAN",
    bg=BG_COLOR,
    fg=TITLE_COLOR,
    font=("Arial", 40, "bold")
)
menu_title.pack(pady=(10, 20))

# Creating canvas fot HANGMAN
menu_canvas = tk.Canvas(
    menu_frame,
    bg=BG_COLOR,
    width=300,
    height=250,
    highlightthickness=0
)
menu_canvas.pack()

# Draw the GALLOWS
menu_gallows = draw_gallows(menu_canvas)

# Draw the HANGMAN
menu_hangman = draw_hangman(menu_canvas)

# Creating PLAY BUTTON
play_button = tk.Label(
    menu_frame,
    text="PLAY",
    bg=PLAY_BUTTON_COLOR,
    fg="white",
    font=("Arial", 20, "bold"),
    width=16,
    padx=10,
    pady=10,
    cursor="hand2"
)
play_button.pack(pady=(30, 15))
play_button.bind("<Button-1>", play_game)

# Creating QUIT BUTTON
quit_button = tk.Label(
    menu_frame,
    text="QUIT",
    bg=QUIT_BUTTON_COLOR,
    fg="white",
    font=("Arial", 20, "bold"),
    width=16,
    padx=10,
    pady=10,
    cursor="hand2"
)
quit_button.pack(padx=10, pady=15)
quit_button.bind("<Button-1>", quit_game)

# GAME FRAME
hint, hidden_word = get_random_word(words)

word_display = len(hidden_word) * ["_"]

lives = MAX_LIVES
hangman_index = 0

game_frame = tk.Frame(
    window,
    bg=BG_COLOR
)

# Label for TITLE
gf_title = tk.Label(
    game_frame,
    text="HANGMAN",
    bg=BG_COLOR,
    fg=TITLE_COLOR,
    font=("Arial", 40, "bold")
)
gf_title.pack(pady=10)

# Label for SUBTITLE
gf_subtitle = tk.Label(
    game_frame,
    text="Guess the hidden word!",
    bg=BG_COLOR,
    fg=SUBTITLE_COLOR,
    font=("Arial", 20, "normal")
)
gf_subtitle.pack(pady=10)

# Label for LIVES count
lives_label = tk.Label(
    game_frame,
    text=f"♡ LIVES: {lives}",
    bg=BG_COLOR,
    fg=TITLE_COLOR,
    font=("Arial", 18, "normal")
)
lives_label.pack(pady=10)

# Area for HANGMAN and KEYBOARD
main_area = tk.Frame(
    game_frame,
    bg=BG_COLOR
)
main_area.pack(fill="x", pady=10)

# Building AREA for HANGMAN
gf_canvas = tk.Canvas(
    main_area,
    bg=GAME_FRAME_COLOR,
    width=300,
    height=250,
    highlightthickness=0
)
gf_canvas.pack(side="left", padx= 30)

# Draw the GALLOWS
gf_gallows = draw_gallows(gf_canvas)

# Draw the HANGMAN
gf_hangman = draw_hangman(gf_canvas)
for limb in gf_hangman:
    gf_canvas.itemconfigure(limb, state="hidden")

# Building the KEYBOARD
keyboard_frame = tk.Frame(
    main_area,
    bg=BG_COLOR,
    height=250,
    width=420,
    highlightbackground=SUBTITLE_COLOR,
    highlightthickness=4
)
keyboard_frame.pack(side="right", padx=30)
keyboard_frame.pack_propagate(False)

keyboard = tk.Frame(
    keyboard_frame,
    bg=BG_COLOR
)
keyboard.pack()

letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

row_num = 0
column_num = 0
keyboard_buttons = []

for letter in letters:
    letter_key = tk.Label(
        keyboard,
        text=letter,
        fg=TITLE_COLOR,
        bg=GAME_FRAME_COLOR,
        width=3,
        font=("Arial", 22, "normal"),
        cursor="hand2"
    )
    keyboard_buttons.append(letter_key)

    letter_key.grid(row=row_num, column=column_num, padx=4, pady=15)
    column_num += 1
    if column_num == 7:
        row_num += 1
        column_num = 0

    letter_key.bind("<Button-1>", handle_letter_guess)

# Label for HINT
hint_label = tk.Label(
    game_frame,
    text=f"HINT: {hint}",
    bg=BG_COLOR,
    fg=SUBTITLE_COLOR,
    font=("Arial", 18, "normal")
)
hint_label.pack(pady=10)

# Label for HIDDEN WORD
word_label = tk.Label(
    game_frame,
    text=" ".join(word_display),
    bg=BG_COLOR,
    fg=TITLE_COLOR,
    font=("Arial", 40, "normal")
)
word_label.pack(pady=10)

# RESULT SCREEN
result_frame = tk.Frame(
    window,
    bg=BG_COLOR
)

victory_label = tk.Label(
    result_frame,
    text="VICTORY",
    fg=PLAY_BUTTON_COLOR,
    bg=BG_COLOR,
    font=("Arial", 40, "bold")
)

game_over_label = tk.Label(
    result_frame,
    text="GAME OVER",
    bg=BG_COLOR,
    fg=QUIT_BUTTON_COLOR,
    font=("Arial", 40, "bold")
)

result_text_label = tk.Label(
    result_frame,
    text="The hidden word was:",
    bg=BG_COLOR,
    fg=SUBTITLE_COLOR,
    font=("Arial", 16, "normal")
)

result_word_label = tk.Label(
    result_frame,
    bg=BG_COLOR,
    fg=TITLE_COLOR,
    font=("Arial", 25, "normal")
)

result_canvas = tk.Canvas(
    result_frame,
    bg=GAME_FRAME_COLOR,
    width=300,
    height=250,
    highlightthickness=0
)

result_gallows = draw_gallows(result_canvas)
result_hangman = draw_hangman(result_canvas)

for limb in result_hangman:
    result_canvas.itemconfigure(limb, state="hidden")

result_buttons_frame = tk.Frame(
    result_frame,
    bg=BG_COLOR,
    width=800
)

play_again_button = tk.Label(
    result_buttons_frame,
    text="PLAY AGAIN",
    bg=PLAY_BUTTON_COLOR,
    fg="white",
    font=("Arial", 20, "bold"),
    width=16,
    padx=10,
    pady=10,
    cursor="hand2"
)

rf_quit_button = tk.Label(
    result_buttons_frame,
    text="QUIT",
    bg=QUIT_BUTTON_COLOR,
    fg="white",
    font=("Arial", 20, "bold"),
    width=16,
    padx=10,
    pady=10,
    cursor="hand2"
)

# Keeps the Game running
window.mainloop()
