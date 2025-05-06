#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  1 12:55:54 2025

Created by: Dhananjoy Bhuyan
"""
import sys
import tty
import termios
import os
from random import randint, choice
from time import time, sleep
import requests
import json
from shutil import get_terminal_size
from string import ascii_letters, digits, punctuation

def text2art(char: str) -> str:
    if char == 'CORRECT':
        return '  ____   ___   ____   ____   _____   ____  _____ \n / ___| / _ \\ |  _ \\ |  _ \\ | ____| / ___||_   _|\n| |    | | | || |_) || |_) ||  _|  | |      | |  \n| |___ | |_| ||  _ < |  _ < | |___ | |___   | |  \n \\____| \\___/ |_| \\_\\|_| \\_\\|_____| \\____|  |_|  \n                                                 \n'
    elif char == 'WRONG':
        return '__        __ ____    ___   _   _   ____ \n\\ \\      / /|  _ \\  / _ \\ | \\ | | / ___|\n \\ \\ /\\ / / | |_) || | | ||  \\| || |  _ \n  \\ V  V /  |  _ < | |_| || |\\  || |_| |\n   \\_/\\_/   |_| \\_\\ \\___/ |_| \\_| \\____|\n                                        \n'
    elif char == '5':
        return ' ____  \n| ___| \n|___ \\ \n ___) |\n|____/ \n       \n'
    elif char == '4':
        return ' _  _   \n| || |  \n| || |_ \n|__   _|\n   |_|  \n        \n'
    elif char == '3':
        return ' _____ \n|___ / \n  |_ \\ \n ___) |\n|____/ \n       \n'
    elif char == '2':
        return ' ____  \n|___ \\ \n  __) |\n / __/ \n|_____|\n       \n'
    elif char == '1':
        return ' _ \n/ |\n| |\n| |\n|_|\n   \n'

    
SCORE = 0
CORRECT = 0
TIMES = []
BADGE = None
FORGIVEN = None
Multiplier = 1
Bonus = 0
Badges_scores = {'No Badge Yet': 0,
                 'Newbie': 100,
                 'Rising Star': 500,
                 'Quick Thinker': 1000,
                 'Math Warrior': 2500,
                 'Speed Demon': 5000,
                 'Mastermind': 10000,
                 'Unstoppable': 20000,
                 'Score Machine': 50000,
                 'Legend': 100000,
                 'Immortal Solver': 250000,
                 'Ultimate Pro Solver': 1000000,
                 'MAX LEVEL SOLVER': 1200000,
                 'No more badges, you already reached MAX LEVEL. More badges will be added later on in updates.': None}


def generate_questions(level: int = 1):
    operations = ["+", "-", "*", "/"]
    chosen_op = choice(operations)
    level_ranges = {
        1: (1, 9),
        2: (10, 99),
        3: (100, 999),
        4: (1000, 9999),
        5: (10000, 100000)
    }

    if chosen_op == '/':
        min_a, max_b = level_ranges[level]
        num2 = randint(min_a, max_b)
        num1 = num2*randint(min_a, max_b)
    else:
        num1 = ""
        num2 = ""
        for i in range(level):
            num1 += str(randint(1, 9))
            num2 += str(randint(1, 9))
    expression = f"{num1} {chosen_op} {num2}"
    return expression


def badges(name: str):
    try:
        score = float(get(name, "quick_solver_scores"))
    except (KeyError, FileNotFoundError):
        score = SCORE

    if score >= 1200000:
        return "MAX LEVEL SOLVER"
    elif score >= 1000000:
        return "Ultimate Pro Solver"
    elif score >= 250000:
        return "Immortal Solver"
    elif score >= 100000:
        return "Legend"
    elif score >= 50000:
        return "Score Machine"
    elif score >= 20000:
        return "Unstoppable"
    elif score >= 10000:
        return "Mastermind"
    elif score >= 5000:
        return "Speed Demon"
    elif score >= 2500:
        return "Math Warrior"
    elif score >= 1000:
        return "Quick Thinker"
    elif score >= 500:
        return "Rising Star"
    elif score >= 100:
        return "Newbie"
    else:
        return "No Badge Yet"


def badge_bonus(badge: str):
    global FORGIVEN
    global Multiplier
    global SCORE
    global Bonus
    daily_login = {
        "Newbie": 0,
        "Rising Star": 0,
        "Quick Thinker": 0,
        "Math Warrior": 5,
        "Speed Demon": 8,
        "Mastermind": 10,
        "Unstoppable": 15,
        "Score Machine": 18,
        "Legend": 20,
        "Immortal Solver": 25,
        "Ultimate Pro Solver": 30,
        "MAX LEVEL SOLVER": 100
    }
    Bonus = daily_login[badge]
    SCORE += daily_login[badge]

    multipliers = {
        "Newbie": 1.0,
        "Rising Star": 1.0,
        "Quick Thinker": 1.2,
        "Math Warrior": 1.25,
        "Speed Demon": 1.35,
        "Mastermind": 1.45,
        "Unstoppable": 1.5,
        "Score Machine": 1.88,
        "Legend": 2.0,
        "Immortal Solver": 2.55,
        "Ultimate Pro Solver": 3.0,
        "MAX LEVEL SOLVER": 8.99
    }

    Multiplier = multipliers[badge]
    if randint(1, 10) > 5:
        immunity = {
            "Newbie": 0,
            "Rising Star": 0,
            "Quick Thinker": 1,
            "Math Warrior": 2,
            "Speed Demon": 2,
            "Mastermind": 3,
            "Unstoppable": 4,
            "Score Machine": 5,
            "Legend": 10,
            "Immortal Solver": 15,
            "Ultimate Pro Solver": 20,
            "MAX LEVEL SOLVER": 28,
        }

        FORGIVEN = immunity[badge]


def _add2json(file_name: str,
              key: str,
              value):
    if os.path.exists(file_name):
        with open(file_name) as f:
            db = json.load(f)
    else:
        db = {}

    db[key] = value

    with open(file_name, "w") as f:
        json.dump(db, f, indent=4)


def store(data,
          key: str,
          database_name: str):
    database_name += '.json'

    _add2json(
        f"{os.path.expanduser('~')}/.qsi/{database_name}", key, data)


def get(key: str,
        database_name: str):

    database_name += '.json'
    if os.path.exists(f"{os.path.expanduser('~')}/.qsi/{database_name}"):
        with open(f"{os.path.expanduser('~')}/.qsi/{database_name}") as f:
            full_data = json.load(f)
        if not full_data:
            raise KeyError("Database is empty.")
        if key in full_data:
            return full_data[key]
        else:
            raise KeyError(f"Key {key} not found in database.")
    else:
        raise FileNotFoundError("Database not found.")


def get_key() -> str:
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setraw(fd)             # Turn off buffering
        key = sys.stdin.read(1)    # Read 1 character
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return key


def print_screen(screen: list[list[str]]) -> None:
    for row in screen:
        print(''.join(row))


def make_border(frame: list[list[str]]) -> None:
    frame[0] = ['-']*len(frame[0])
    frame[-1] = ['-']*len(frame[0])

    for row in range(len(frame)):

        frame[row][0], frame[row][-1] = '|', '|'
    for row, col in [(0, 0), (-1, 0), (0, -1), (-1, -1)]:
        frame[row][col] = '+'


def make_box(screen: list[list[str]], row: int, col: int, width: int, height: int) -> None:
    box = [[' ' for _ in range(width)] for _ in range(height)]
    make_border(box)
    for i in range(height):
        for j in range(width):
            screen[row + i][col + j] = box[i][j]
    del box


def insert_text(frame: list[list[str]], text: str, row: int, col: int) -> None:
    sw = len(frame[0]) - 1
    sh = len(frame) - 1
    r = row
    c = col
    for ch in text:
        if r >= sh:
            break
        frame[r][c] = ch
        c += 1
        if c >= sw:
            c = 2
            r += 1


def insert_text_in_box(frame: list[list[str]], text: str, box_row: int, box_col: int, box_width: int, box_height: int) -> None:
    box = [[' ' for _ in range(box_width)] for _ in range(box_height)]
    make_border(box)
    insert_text(box, text, 1, 1)
    for i in range(box_height):
        for j in range(box_width):
            frame[box_row + i][box_col + j] = box[i][j]
    del box


def dynamic_text(frame: list[list[str]], text: str, row: int, col: int) -> None:
    r = row
    c = col
    for ch in text:
        os.system('clear')
        if c >= len(frame[0]) - 1:
            r += 1
            c = 2
        if r >= len(frame) - 1:
            break
        frame[r][c] = ch
        print_screen(frame)
        c += 1
        sleep(0.08)
    os.system('clear')


def make_screen(width: int, height: int) -> list[list[str]]:
    scr = [[' ' for _ in range(width)] for _ in range(height - 1)]
    make_border(scr)
    insert_text(scr, "\\:: Quick Solver 3.0.0 ::/",
                2, len(scr[0])//2 - 13)
    return scr


def set_visible(text: str, placeholder: str) -> str:
    visible_length = len(placeholder) + 1
    if not text:
        return '█' + placeholder
    else:
        if len(text) > visible_length:
            return text[-visible_length] + '█'
        else:
            return text[:] + '█'


def username() -> str:
    global BADGE
    name = ""
    visible = None

    os.system('clear')
    while 1:

        scr_width, scr_height = get_terminal_size(fallback=(80, 24))

        screen = make_screen(scr_width, scr_height)
        visible = set_visible(name, 'Enter you username...')
        insert_text_in_box(screen, visible, len(screen) //
                           2 - 1, len(screen[0])//2 - 12, 24, 3)

        insert_text(screen, "Username:", len(
            screen)//2 - 2, len(screen[0])//2 - 4)

        print_screen(screen)
        key = get_key()
        if key == '\x7f':
            os.system('clear')
            if name:
                name = name[:-1]
        elif key == '\r' or key == '\n':
            if name:
                break
        elif key in ascii_letters + digits + ' ' + punctuation:
            os.system('clear')
            name += key
        else:
            os.system('clear')
    try:
        score = get(name, "quick_solver_scores")
        badge = get(name, "quick_badges")
        os.system('clear')
        width, height = get_terminal_size(fallback=(80, 24))
        screen = make_screen(width, height)
        insert_text(screen, "Welcome Back!!", 4, len(screen[0])//2 - 7)
        dynamic_text(
            screen, f"Hi {name}! Your current score is: {score}", 6, 2)
        insert_text(screen, f"Current Badge: {badge}", 7, 2)
        BADGE = badge
        if BADGE != 'No Badge Yet':
            badge_bonus(BADGE)
            insert_text(screen, 'Badge Bonus:', 9, len(screen[0])//2 - 6)
            dynamic_text(screen, f'Login Bonus: score + {Bonus}', 11, 2)
            dynamic_text(screen,
                         f'Score Multiplier: {Multiplier}', 12, 2)
            dynamic_text(
                screen, 'This means each time you answer a question, ', 13, 2)
            dynamic_text(screen,
                         f'the score you get will be multiplied by {Multiplier}', 14, 2)

            if FORGIVEN not in [None, 0]:
                insert_text(screen,
                            'In this session, ', 16, 2)
                dynamic_text(
                    screen, f'{FORGIVEN} wrong answers will be forgiven because you have a "{BADGE}" badge.', 17, 2)

    except (KeyError, FileNotFoundError):
        width, height = get_terminal_size(fallback=(80, 24))
        screen = make_screen(width, height)
        dynamic_text(screen, 'New user detected...', 4, len(screen[0])//2 - 10)
        dynamic_text(screen, f'Hello {name}!!', 6, 2)
        store('0', name, "quick_solver_scores")
        store("No Badge Yet", name, "quick_badges")

    insert_text(screen, 'Press any key to proceed.', len(screen) - 3, 2)

    print_screen(screen)
    get_key()

    return name


def draw_button(screen: list[list[str]], text: str, row: int, col: int, focused: bool) -> None:
    button = [[' ' for _ in range(len(text) + 4)] for _ in range(3)]
    insert_text(button, f"[{text}]", 1, 1)
    if focused:
        make_border(button)

    for i in range(len(button)):
        for j in range(len(button[0])):
            screen[row + i][col + j] = button[i][j]
    del button


def level() -> int:
    focus = 0
    buttons = {0: 'lvl 1: Beginner',
               1: 'lvl 2: Intermediate',
               2: 'lvl 3: Pro',
               3: 'lvl 4: Master',
               4: 'lvl 5: Legend'
               }

    os.system('clear')
    width, height = get_terminal_size(fallback=(80, 24))

    screen = make_screen(width, height)
    insert_text(
        screen, 'Now you are going to choose a level to play.', 4, 2)
    insert_text(
        screen, 'Remember that Higher level means Harder Questions.', 5, 2)
    insert_text(
        screen, 'For choosing, use arrow keys to navigate to a button. And Press "enter" to click on the button.', 7, 2)
    insert_text(
        screen, 'When a button is selected, a box will be drawn around it...if it is not selected it will be just like: [button text] (Wrapped in []) The OK button below is selected. Now press Enter!!', 9, 2)
    insert_text_in_box(screen, '[OK]', 12, len(screen[0])//2 - 3, 6, 3)
    print_screen(screen)
    get_key()

    while 1:
        os.system('clear')

        screen = make_screen(get_terminal_size(fallback=(80, 24)).columns, 22)

        insert_text(screen, 'Choose Level', 4, len(screen[0])//2 - 6)

        brow = 5

        for idx, b in enumerate(buttons.keys()):

            draw_button(screen, buttons[b], brow, 2, focused=(idx == focus))
            brow += 3
        print_screen(screen)
        key = get_key()
        if key == '\x1b':
            get_key()
            key = get_key()
            if key == 'A':
                if focus > 0:
                    focus -= 1
                    continue
            elif key == 'B':
                if focus < len(buttons) - 1:
                    focus += 1
                    continue
        elif key == '\r' or key == '\n':
            return focus + 1
        else:
            continue


def questions() -> int:
    noq = ""

    while 1:
        os.system('clear')
        width, height = get_terminal_size(fallback=(80, 24))

        screen = make_screen(width, height)

        insert_text(
            screen, 'How many questions will you answer in this session?', 4, 2)
        insert_text(
            screen, '**Please note that you only have to enter an integer.**', 6, 2)
        insert_text(screen, 'Number of Questions:', 7, len(screen[0])//2 - 10)
        insert_text_in_box(screen, set_visible(noq, 'Enter number of questions....'), 8,
                           len(screen[0])//2 - 16, 32, 3)
        print_screen(screen)
        key = get_key()
        if key in digits:
            noq += key
        elif key == '\r' or key == '\n':
            if noq:
                return int(noq)
        elif key == '\x7f':
            if noq:
                noq = noq[:-1]
        else:
            pass


def ask_and_calculate(level: int, qn: int, ques: int) -> None:
    global SCORE, FORGIVEN, TIMES, Multiplier, CORRECT

    question = generate_questions(level)
    answer = int(eval(question))
    user_answer = ""
    start = time()
    while 1:
        os.system('clear')
        size = get_terminal_size(fallback=(80, 24))
        screen = make_screen(*size)
        insert_text(screen, f'Question: {qn}/{ques}', 3, 2)
        insert_text(screen, question, 4, len(
            screen[0])//2 - (len(question)//2))
        insert_text(screen, 'Your answer:', 6, len(screen[0])//2 - 6)
        visible = set_visible(user_answer, "Enter your answer....")
        insert_text_in_box(screen, visible, 8, len(screen[0])//2 - 12, 24, 3)
        print_screen(screen)

        key = get_key()
        if key in digits + '-':
            user_answer += key
        elif key == '\x7f':
            if user_answer:
                user_answer = user_answer[:-1]
        elif key == '\r' or key == '\n':
            if not user_answer:
                continue
            end = time()
            user_answer = int(user_answer)
            break
        else:
            pass

    if user_answer == answer:
        os.system('clear')
        size = get_terminal_size(fallback=(80, 24))
        screen = make_screen(*size)
        time_taken = end - start
        TIMES.append(float(f'{time_taken:.3f}'))
        CORRECT += 1
        x = text2art("CORRECT").splitlines()
        yay = [[j for j in i] for i in x]
        for i in range(len(yay)):
            for j in range(len(yay[0])):
                screen[4 + i][2 + j] = yay[i][j]
        dynamic_text(screen, f'You took {time_taken:.3f} seconds!', 10, 5)
        os.system('clear')
        if time_taken < 1:
            insert_text(
                screen, 'Whoa!! You just did it under 1 second! Score + 100', 12, 2)
            SCORE += (100*Multiplier)
        elif time_taken < 2:
            insert_text(
                screen, 'Awesome! You just did it under 2 seconds. Score + 50', 12, 2)
            SCORE += (50*Multiplier)
        elif time_taken < 3:
            insert_text(
                screen, 'time taken less than 3 seconds. Score + 10', 12, 2)
            SCORE += (10*Multiplier)
        elif time_taken < 5:
            insert_text(
                screen, "Score + 8, time taken less than 5 seconds...", 12, 2)
            SCORE += (8*Multiplier)
        elif time_taken < 10:
            insert_text(
                screen, "Score + 5, time taken less than 10 seconds...", 12, 2)
            SCORE += (5*Multiplier)
        else:
            insert_text(
                screen, "Score + 1, VERY SLOW!! But it's okay practice will make you perfect.", 12, 2)
            SCORE += (1*Multiplier)

        print_screen(screen)
    else:
        os.system('clear')
        width, height = get_terminal_size(fallback=(80, 24))
        screen = make_screen(width, height)
        x = text2art("WRONG").splitlines()
        boo = [[j for j in i] for i in x]
        for i in range(len(boo)):
            for j in range(len(boo[0])):
                screen[4 + i][2 + j] = boo[i][j]
        dynamic_text(screen,
                     f'Wrong answer! The correct answer was {answer}', 10, 5)

        if FORGIVEN not in [0, None]:
            FORGIVEN -= 1
            dynamic_text(
                screen, "It's alright, wrong answer forgiven because of your '{BADGE}' badge. Score + 5", 12, 2)
            SCORE += (5*Multiplier)
        print_screen(screen)
    sleep(1.5)


def stats(name: str, ques: int) -> None:
    width, height = get_terminal_size(fallback=(80, 24))
    screen = make_screen(width, height)
    score_in_this_session = SCORE
    total = get(name, "quick_solver_scores")
    dynamic_text(screen, f'Player: {name}', 4, 2)
    dynamic_text(screen,
                 f'Scored in this session: {score_in_this_session}', 5, 2)
    dynamic_text(screen, f'Total Score: {total}', 6, 2)
    if BADGE != badges(name):
        dynamic_text(screen, 'NEW BADGE UNLOCKED!', 7, 2)
        store(badges(name), name, "quick_badges")
    dynamic_text(screen, f'Player Badge: {badges(name)}', 8, 2)
    badge_list = list(Badges_scores.keys())
    nt_badge = badge_list[badge_list.index(badges(name)) + 1]
    score_needed = Badges_scores[nt_badge]
    dynamic_text(screen,
                 f'next badge coming: "{nt_badge}"(minimum score needed: {score_needed})', 9, 2)
    dynamic_text(screen, f'Answered correct: {CORRECT}/{ques}', 11, 2)
    dynamic_text(screen, f'Answered wrong: {ques - CORRECT}/{ques}', 12, 2)
    insert_text(screen, f'Total questions answered: {ques}', 13, 2)
    print_screen(screen)
    sleep(2.5)
    os.system('clear')
    width, height = get_terminal_size(fallback=(80, 24))
    screen = make_screen(width, height)
    insert_text(screen, 'TIMES', 4, len(screen[0])//2 - 2)
    dynamic_text(screen, f'Best time in this session: {min(TIMES)}', 6, 2)
    dynamic_text(screen, f'Average: {sum(TIMES)/len(TIMES)}', 8, 2)
    dynamic_text(screen, f'Slowest: {max(TIMES)}', 10, 2)
    print_screen(screen)


def leaderboard(name: str):
    os.system('clear')
    print("\n\n\t\\:: Quick Solver ::/\n\n")
    with open(f"{os.path.expanduser('~')}/.qsi/quick_solver_scores.json") as f:
        data = json.load(f)
    data = {k: float(v) for k, v in data.items()}
    data = dict(sorted(data.items(), key=lambda x: x[1], reverse=True))
    if len(data.keys()) == 1:
        print("\n\nNOTE: More than one player can play on this device with different usernames, so the leader board doesn't have only one player to show!\n")
        print("Even you can compete with yourself with different usernames!!\n")
    print("_"*66 + "\nLeaderboard:-" + (" "*53) + "|")
    print("_"*66 + "|")
    sleep(1)

    for idx, curname in enumerate(data, 1):
        umcn = curname
        score = data[curname]
        if len(curname) >= 16:
            curname = curname[:13] + "..."

        else:
            spaces_to_add = 16 - len(curname)
            curname += (" "*spaces_to_add)

        spaces_to_add2 = 66 - (2 + len(str(idx)) + 3 +
                               len(curname) + 18 + len(str(score)))

        if umcn == name:
            print(f"| {idx} | {curname}(You)    | score: {score}", end="")
            print(" "*spaces_to_add2 + "|")
        else:
            print(f'| {idx} | {curname}         | score: {score}', end="")
            print(" "*spaces_to_add2 + "|")
        sleep(1)
    print("_"*66 + "|\n\n")

    print("PLAYER BADGES: ")
    sleep(1)
    with open(os.path.expanduser("~/.qsi/quick_badges.json")) as f:
        pbadges = json.load(f)
    print("_"*66)
    print("Badges:-" + " "*58 + "|")
    print("_"*66 + "|")
    sleep(1)
    for idx, player in enumerate(pbadges, 1):
        umpn = player
        if len(player) >= 16:
            player = player[:13] + "..."
        else:
            spaces_to_add = 16 - len(player)
            player += (" "*spaces_to_add)

        spaces_to_add2 = 66 - (2 + len(str(idx)) + 3 +
                               len(player) + 13 + len(str(pbadges[umpn])) + 1)

        print(f"| {idx} | {player}    | badge: {pbadges[umpn]} ", end="")
        print(" "*spaces_to_add2 + "|")
        sleep(1)
    print("_"*66 + "|\n\n")


def play():
    global CORRECT
    global SCORE
    global NAME
    global FORGIVEN
    global BADGE
    global Multiplier
    global Bonus
    global TIMES
    global Badges_scores

    CORRECT = 0
    SCORE = 0
    TIMES = []
    NAME = None
    BADGE = None
    FORGIVEN = None
    Multiplier = 1
    Bonus = 0

    if not os.path.exists(os.path.expanduser("~/.Quick_Solver/first.txt")):
        with open(os.path.expanduser("~/.Quick_Solver/first.txt"), "w") as f:
            f.write(
                "This file was created when the game was first launched on this device.")

    name = username()
    lvl = level()
    ques = questions()
    for i in range(5, 0, -1):
        os.system('clear')
        width, height = get_terminal_size(fallback=(80, 24))
        screen = make_screen(width, height)
        insert_text(screen, 'We are starting in....',
                    4, len(screen[0])//2 - 11)
        num = text2art(str(i)).splitlines()
        num = [[j for j in i] for i in num]
        for i in range(len(num)):
            for j in range(len(num[0])):
                screen[6 + i][(len(screen[0])//2 -
                               (len(num[0])//2)) + j] = num[i][j]
        print_screen(screen)
        sleep(1)
    for i in range(1, ques + 1):
        ask_and_calculate(lvl, i, ques)
    store(str(float(get(name, "quick_solver_scores")) + SCORE),
          name, "quick_solver_scores")
    stats(name, ques)
    sleep(1.5)
    leaderboard(name)


def want_desktop() -> None:

    buttons = {
        0: "Yes",
        1: "No"
    }
    focus = 0
    while 1:
        os.system('clear')
        size = get_terminal_size(fallback=(80, 24))
        screen = make_screen(*size)
        insert_text(
            screen, 'Do you want the game icon in your desktop screen??', 4, 2)
        insert_text(
            screen, 'Use arrow keys to choose from buttons and press enter to click.', 6, 2)
        bcol = 3
        for i, b in enumerate(buttons):
            draw_button(screen, buttons[b], 7, bcol, focused=(i == focus))
            bcol += 8
        print_screen(screen)
        key = get_key()
        if key == '\x1b':
            get_key()
            key = get_key()
            if key == 'D':
                if focus > 0:
                    focus -= 1
                    continue
            elif key == 'C':
                if focus < len(buttons) - 1:
                    focus += 1
                    continue
        elif key == '\r' or key == '\n':
            chosen = buttons[focus]
            break
        else:
            continue
    if chosen == 'Yes':
        os.system(os.path.expanduser("bash ~/.qsi/qsi4dsktp.sh"))


def check_updates() -> None:

    with open(f"{os.path.expanduser('~')}/.Quick_Solver/version.txt", "r") as f:
        current_version = f.read().strip()
    url = "https://raw.githubusercontent.com/DhananjoyBhuyan/Quick_Solver/main/latest_version.txt"

    response = requests.get(url)

    if response.status_code == 200:
        latest_version = response.text.strip()

        if latest_version != current_version:
            url2 = "https://raw.githubusercontent.com/DhananjoyBhuyan/Quick_Solver/main/whats_new.txt"
            new = requests.get(url2)
            if new.status_code == 200:
                new = new.text.strip()
            else:
                new = "\n\nError: failed to fetch 'what's new' section, kindly check your internet connection, if your connection is good, continue by ignoring...\n\n"
            print()
            print("="*67)
            print()
            print("\\:: IMPORTANT NOTE ::/")
            print()
            print("Update Available!!")
            print(f"\nVersion {latest_version} is available.")
            print()
            print("Your currently installed version: ", current_version)
            print()
            print(new)
            screen = [[' ' for _ in range(get_terminal_size(
                fallback=(80, 24)).columns)] for _ in range(8)]
            focus = 0
            buttons = {
                0: "Yes",
                1: 'No'
            }
            sleep(2)
            while 1:
                
                insert_text(screen, 'Do you want to update?',
                            0, len(screen[0])//2 - 11)
                insert_text(
                    screen, 'Use arrow keys to choose from buttons and press enter to click.', 2, 2)
                bcol = 4
                for b in buttons:
                    draw_button(screen, buttons[b],
                                4, bcol, focused=(b == focus))
                    bcol += 8
                print_screen(screen)
                key = get_key()
                if key == '\x1b':
                    get_key()
                    key = get_key()
                    if key == 'D':
                        if focus > 0:
                            focus -= 1
                    elif key == 'C':
                        if focus < 1:
                            focus += 1
                elif key == '\r' or key == '\n':
                    chosen = buttons[focus]
                    break
                os.system('clear')
            if chosen == 'Yes':
                os.system(os.path.expanduser('bash ~/.qsi/qsi4update.sh'))

    else:
        print("\n\nError: Couldn't check for updates, make sure your internet connection is good. If it is, then the server might be down or some other problem to check for updates.\n\n")


def main() -> None:
    while 1:
        play()
        focus = 0
        buttons = {
            0: "Yes",
            1: 'No'
        }
        while 1:
            os.system('clear')
            width, height = get_terminal_size(fallback=(80, 24))
            screen = make_screen(width, height)
            insert_text(screen, 'Do you want to play again?',
                        4, len(screen[0])//2 - 11)
            insert_text(
                screen, 'Use arrow keys to choose from buttons and press enter to click.', 6, 2)
            bcol = 4
            for b in buttons:
                draw_button(screen, buttons[b],
                            8, bcol, focused=(b == focus))
                bcol += 8
            print_screen(screen)
            key = get_key()
            if key == '\x1b':
                get_key()
                key = get_key()
                if key == 'D':
                    if focus > 0:
                        focus -= 1
                elif key == 'C':
                    if focus < 1:
                        focus += 1
            elif key == '\r' or key == '\n':
                chosen = buttons[focus]
                break
        if chosen == 'No':
            break


if not os.path.exists(os.path.expanduser('~/.Quick_Solver/first.txt')):
    want_desktop()
check_updates()
main()
