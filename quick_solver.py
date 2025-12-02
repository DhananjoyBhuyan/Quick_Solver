
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
from string import (
    ascii_letters,
    digits,
    punctuation
)
from datetime import date
from os.path import expanduser as expuser


LATEST_VERSION_URL = "https://raw.githubusercontent.com/DhananjoyBhuyan/Quick_Solver/main/latest_version.txt"
RELEASE_NOTES_URL = "https://raw.githubusercontent.com/DhananjoyBhuyan/Quick_Solver/main/whats_new.txt"


def gts():

    return get_terminal_size(
        fallback=(80, 24)
    )


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
NAME = None
Badges_scores = {
    'No Badge Yet': 0,
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
    'No more badges, you already reached MAX LEVEL. More badges will be added later on in updates.': None
}


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
        f"{expuser('~')}/.qsi/{database_name}",
        key,
        data
    )


def get(key: str,
        database_name: str):

    database_name += '.json'
    if os.path.exists(f"{expuser('~')}/.qsi/{database_name}"):
        with open(f"{expuser('~')}/.qsi/{database_name}") as f:
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
        termios.tcsetattr(fd,
                          termios.TCSADRAIN,
                          old_settings)

    return key


def print_screen(screen: list[list[str]]) -> None:
    for row in screen:
        print(''.join(row))


def make_border(frame: list[list[str]]) -> None:
    frame[0] = ['-']*len(frame[0])
    frame[-1] = ['-']*len(frame[0])

    for row in range(len(frame)):

        frame[row][0], frame[row][-1] = '|', '|'
    for row, col in [
            (0, 0),
            (-1, 0),
            (0, -1),
            (-1, -1)
    ]:
        frame[row][col] = '+'


def make_box(screen: list[list[str]],
             row: int,
             col: int,
             width: int,
             height: int) -> None:
    box = [
        [
            ' '
            for _ in range(width)
        ] for _ in range(height)
    ]
    make_border(box)
    for i in range(height):
        for j in range(width):
            screen[row + i][col + j] = box[i][j]
    del box


def insert_text(frame: list[list[str]],
                text: str,
                row: int,
                col: int) -> None:
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


def insert_text_in_box(frame: list[list[str]],
                       text: str,
                       box_row: int,
                       box_col: int,
                       box_width: int,
                       box_height: int) -> None:
    box = [
        [
            ' '
            for _ in range(box_width)
        ] for _ in range(box_height)
    ]
    make_border(box)
    insert_text(box, text, 1, 1)
    for i in range(box_height):
        for j in range(box_width):
            frame[
                box_row + i
            ][
                box_col + j
            ] = box[i][j]
    del box


def dynamic_text(frame: list[list[str]],
                 text: str,
                 row: int,
                 col: int) -> None:
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
        sleep(0.035)
    os.system('clear')


def make_screen(width: int,
                height: int) -> list[list[str]]:
    scr = [
        [
            ' '
            for _ in range(width)
        ] for _ in range(height - 1)
    ]
    make_border(scr)
    insert_text(scr,
                "\\:: Quick Solver 3.6.0 ::/",
                2,
                len(scr[0])//2 - 13)
    return scr


def set_visible(text: str,
                placeholder: str,

                cursor_pos: int = 0) -> str:

    visible_length = len(placeholder)
    if not text:

        return '█' + placeholder
    else:
        cursor_index = len(text) + cursor_pos

        if len(text[cursor_index:]) >= visible_length:

            return '█' + text[cursor_index + 1:cursor_index + visible_length]

        return text[-visible_length:cursor_index] + '█' + text[cursor_index + 1:]


def username(changing: bool = False) -> str:
    global BADGE
    name = ""
    visible = None
    if not os.path.exists(
            expuser(
                "~/.Quick_Solver/first.txt"
            )
    ):
        with open(
                expuser(
                    "~/.Quick_Solver/first.txt"
                ), "w") as f:
            f.write(
                "This file was created when the game was first launched on this device."
            )

    os.system('clear')
    cursor_pos = 0
    while 1:

        scr_width, scr_height = gts()

        screen = make_screen(
            scr_width,
            scr_height
        )
        visible = set_visible(
            name,
            'Enter your username...',
            cursor_pos
        )
        insert_text_in_box(
            screen,
            visible,
            len(screen) //
            2 - 1,
            len(screen[0])//2 - 12,
            24,
            3
        )

        insert_text(
            screen,
            "Username:",
            len(screen)//2 - 2,
            len(screen[0])//2 - 4
        )

        print_screen(screen)
        key = get_key()
        # one of the allowed characters.
        if key in digits + punctuation + ascii_letters + ' ':
            os.system('clear')
            cursor_index = len(name) + cursor_pos
            name = name[:cursor_index] + key + name[cursor_index:]
        elif key == '\x7f':  # Backspace.

            # remove the char right before the cursor.
            cursor_index = len(name) + cursor_pos
            name = name[:cursor_index - 1] + name[cursor_index:]
            # memory.
            del cursor_index
        elif key == '\x1b':  # escape sequence.
            os.system('clear')
            get_key()  # throw away part.
            key = get_key()  # the real key.
            if key == 'D':  # left arrow.
                if cursor_pos > (0-len(name)):
                    cursor_pos -= 1  # move cursor left.
            elif key == 'C':  # right arrow.
                if cursor_pos < 0:
                    cursor_pos += 1  # move it right.
            elif key == '3':  # delete key.
                get_key()  # throw away part.

                # delete the char right after the cursor.
                if cursor_pos < 0:
                    cursor_index = len(name) + cursor_pos
                    name = name[:cursor_index + 1] + \
                        name[cursor_index + 2:]
                    cursor_pos += 1
        elif (key == '\r' or
              key == '\n'):
            if name:
                break
    if not changing:
        try:
            get(name, 'quick_solver_scores')
            BADGE = get(name, 'quick_badges')
            os.system('clear')
            screen = make_screen(
                *gts()
            )
            insert_text(
                screen,
                'Welcome Back!',
                4,
                len(screen)//2 - 6
            )
            print_screen(screen)

            dynamic_text(screen,
                         'Hey ' +
                         name +
                         '!!',
                         6,
                         2)

            dynamic_text(
                screen,
                "Back to rock?? Let's goo!!!",
                8,
                2
            )
            print_screen(screen)
            sleep(1)
        except (KeyError, FileNotFoundError):
            BADGE = 'No Badge Yet'
            store('0',
                  name,
                  'quick_solver_scores')
            store('No Badge Yet',
                  name,
                  'quick_badges')
            os.system('clear')
            screen = make_screen(
                *gts()
            )
            dynamic_text(
                screen,
                'New user detected....',
                4,
                len(screen)//2 - 6
            )
            print_screen(screen)

            dynamic_text(screen,
                         'Hello ' +
                         name +
                         '!!',
                         6,
                         2)

            dynamic_text(
                screen,
                'First time?? Crush it like nothing!! Let\'s Gooo!!',
                8,
                2
            )
            print_screen(screen)
            sleep(1)
    return name


def draw_button(screen: list[list[str]],
                text: str,
                row: int,
                col: int,
                focused: bool) -> None:
    button = [
        [
            ' '
            for _ in range(len(text) + 4)
        ] for _ in range(3)
    ]
    insert_text(button,
                f"[{text}]",
                1,
                1)
    if focused:
        make_border(button)

    for i in range(len(button)):
        for j in range(len(button[0])):
            screen[
                row + i
            ][
                col + j
            ] = button[i][j]
    del button


def level() -> int:
    focus = 0
    buttons = {
        0: 'lvl 1: Beginner',
        1: 'lvl 2: Intermediate',
        2: 'lvl 3: Pro',
        3: 'lvl 4: Master',
        4: 'lvl 5: Legend'
    }

    os.system('clear')
    width, height = gts()

    screen = make_screen(width, height)
    insert_text(
        screen,
        'Now you are going to choose a level to play.',
        4,
        2
    )
    insert_text(
        screen,
        'Remember that Higher level means Harder Questions.',
        5,
        2
    )
    insert_text(
        screen,
        'For choosing, use arrow keys to navigate to a button. And Press "enter" to click on the button.',
        7,
        2
    )
    insert_text(
        screen,
        'When a button is selected, a box will be drawn around it...if it is not selected it will be just like: [button text] (Wrapped in []) The OK button below is selected. Now press Enter!!',
        9,
        2
    )
    insert_text_in_box(
        screen,
        '[OK]',
        12,
        len(screen[0])//2 - 3,
        6,
        3
    )
    print_screen(screen)
    get_key()

    while 1:
        os.system('clear')

        screen = make_screen(
            gts().columns,
            22
        )

        insert_text(screen,
                    'Choose Level',
                    4,
                    len(screen[0])//2 - 6)

        brow = 5

        for idx, b in enumerate(buttons.keys()):

            draw_button(screen,
                        buttons[b],
                        brow,
                        2,
                        focused=(idx == focus))
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
    cursor_pos = 0
    while 1:
        os.system('clear')
        width, height = gts()

        screen = make_screen(width, height)

        insert_text(
            screen,
            'How many questions will you answer in this session?',
            4,
            2
        )
        insert_text(
            screen,
            '**Please note that you only have to enter an integer.**',
            6,
            2
        )
        insert_text(
            screen,
            'Number of Questions:',
            7,
            len(screen[0])//2 - 10
        )
        insert_text_in_box(
            screen,
            set_visible(
                noq,
                'Enter number of questions....',
                cursor_pos
            ),
            8,
            len(screen[0])//2 - 16,
            32,
            3
        )
        print_screen(screen)
        key = get_key()
        if key in digits:
            noq = noq[:(len(noq) + cursor_pos)] + key + \
                noq[(len(noq) + cursor_pos):]
        elif (key == '\r' or
              key == '\n'):
            if noq:
                return int(noq)
        elif key == '\x7f':  # Backspace.

            # remove the char right before the cursor.
            cursor_index = len(noq) + cursor_pos
            noq = noq[:cursor_index - 1] + noq[cursor_index:]
            # memory.
            del cursor_index
        elif key == '\x1b':  # escape sequence.
            get_key()  # throw away part.
            key = get_key()  # the real key.
            if key == 'D':  # left arrow.
                if cursor_pos > (0-len(noq)):
                    cursor_pos -= 1  # move cursor left.
            elif key == 'C':  # right arrow.
                if cursor_pos < 0:
                    cursor_pos += 1  # move it right.
            elif key == '3':  # delete key.
                get_key()  # throw away part.

                # delete the char right after the cursor.
                if cursor_pos < 0:
                    cursor_index = len(noq) + cursor_pos
                    noq = noq[:cursor_index + 1] + \
                        noq[cursor_index + 2:]
                    cursor_pos += 1
        else:
            pass


def ask_and_calculate(level: int,
                      qn: int,
                      ques: int) -> None:
    global SCORE, FORGIVEN, TIMES, Multiplier, CORRECT

    question = generate_questions(level)
    answer = int(eval(question))
    user_answer = ""
    start = time()
    cursor_pos = 0
    while 1:
        os.system('clear')
        size = gts()
        screen = make_screen(*size)
        insert_text(
            screen,
            f'Question: {qn}/{ques}',
            3,
            2
        )
        insert_text(
            screen,
            question,
            4,
            len(screen[0])//2 -
            (len(question)//2)
        )
        insert_text(
            screen,
            'Your answer:',
            6,
            len(screen[0])//2 - 6
        )
        visible = set_visible(
            user_answer,
            "Enter your answer....",
            cursor_pos
        )
        insert_text_in_box(
            screen,
            visible,
            8,
            len(screen[0])//2 - 12,
            24,
            3
        )
        print_screen(screen)

        key = get_key()
        if (key == '-' and
                user_answer):
            continue
        if key in digits + '-':
            user_answer = user_answer[:(len(
                user_answer) + cursor_pos)] + key + user_answer[(len(user_answer) + cursor_pos):]
        elif key == '\x7f':  # Backspace.

            # remove the char right before the cursor.
            cursor_index = len(user_answer) + cursor_pos
            user_answer = user_answer[:cursor_index -
                                      1] + user_answer[cursor_index:]
            # memory.
            del cursor_index
        elif key == '\x1b':  # escape sequence.
            get_key()  # throw away part.
            key = get_key()  # the real key.
            if key == 'D':  # left arrow.
                if cursor_pos > (0-len(user_answer)):
                    cursor_pos -= 1  # move cursor left.
            elif key == 'C':  # right arrow.
                if cursor_pos < 0:
                    cursor_pos += 1  # move it right.
            elif key == '3':  # delete key.
                get_key()  # throw away part.

                # delete the char right after the cursor.
                if cursor_pos < 0:
                    cursor_index = len(user_answer) + cursor_pos
                    user_answer = user_answer[:cursor_index + 1] + \
                        user_answer[cursor_index + 2:]
                    cursor_pos += 1
        elif key == '\r' or key == '\n':
            if not user_answer:
                continue
            if user_answer.strip() == '-':
                continue
            end = time()
            user_answer = int(user_answer)
            break
        else:
            pass

    if user_answer == answer:
        os.system('clear')
        size = gts()
        screen = make_screen(*size)
        time_taken = end - start
        TIMES.append(float(f'{time_taken:.3f}'))
        CORRECT += 1
        x = text2art("CORRECT").splitlines()
        yay = [
            [
                j for j in i
            ] for i in x
        ]
        for i in range(len(yay)):
            for j in range(len(yay[0])):
                screen[4 + i][2 + j] = yay[i][j]
        dynamic_text(
            screen,
            f'You took {time_taken:.3f} seconds!',
            10,
            5
        )
        os.system('clear')
        if time_taken < 1:
            insert_text(
                screen,
                'Whoa!! You just did it under 1 second! Score + 100',
                12,
                2
            )
            SCORE += (100*Multiplier)
        elif time_taken < 2:
            insert_text(
                screen,
                'Awesome! You just did it under 2 seconds. Score + 50',
                12,
                2
            )
            SCORE += (50*Multiplier)
        elif time_taken < 3:
            insert_text(
                screen,
                'time taken less than 3 seconds. Score + 10',
                12,
                2)
            SCORE += (10*Multiplier)
        elif time_taken < 5:
            insert_text(
                screen,
                "Score + 8, time taken less than 5 seconds...",
                12,
                2
            )
            SCORE += (8*Multiplier)
        elif time_taken < 10:
            insert_text(
                screen,
                "Score + 5, time taken less than 10 seconds...",
                12,
                2
            )
            SCORE += (5*Multiplier)
        else:
            insert_text(
                screen,
                "Score + 1, VERY SLOW!! But it's okay practice will make you perfect.",
                12,
                2
            )
            SCORE += (1*Multiplier)

        print_screen(screen)
    else:
        os.system('clear')
        width, height = gts()
        screen = make_screen(width, height)
        x = text2art("WRONG").splitlines()
        boo = [
            [
                j for j in i
            ] for i in x
        ]
        for i in range(len(boo)):
            for j in range(len(boo[0])):
                screen[4 + i][2 + j] = boo[i][j]
        dynamic_text(
            screen,
            f'Wrong answer! The correct answer was {answer}',
            10,
            5
        )

        if FORGIVEN not in [0, None]:
            FORGIVEN -= 1
            dynamic_text(
                screen,
                f"It's alright, wrong answer forgiven because of your '{BADGE}' badge. Score + 5",
                12,
                2
            )
            SCORE += (5*Multiplier)
        print_screen(screen)
    sleep(1.5)


def stats(name: str,
          ques: int,
          badge_unlocked: bool = False) -> None:
    width, height = gts()
    screen = make_screen(width, height)
    score_in_this_session = SCORE
    total = get(name, "quick_solver_scores")
    insert_text(
        screen,
        'Press Ctrl + C to skip.',
        len(screen)-4,
        2
    )
    dynamic_text(
        screen,
        f'Player: {name}',
        4,
        2
    )
    dynamic_text(
        screen,
        f'Scored in this session: {score_in_this_session}',
        5,
        2
    )
    dynamic_text(
        screen,
        f'Total Score: {total}',
        6,
        2
    )
    if badge_unlocked:
        dynamic_text(
            screen,
            'NEW BADGE UNLOCKED!',
            7,
            2
        )

    dynamic_text(
        screen,
        f'Player Badge: {badges(name)}',
        8,
        2
    )
    badge_list = list(Badges_scores.keys())
    nt_badge = badge_list[
        badge_list.index(badges(name)) + 1
    ]
    score_needed = Badges_scores[nt_badge]
    dynamic_text(
        screen,
        f'next badge coming: "{nt_badge}"(minimum score needed: {
            score_needed})',
        9,
        2
    )
    dynamic_text(
        screen,
        f'Answered correct: {CORRECT}/{ques}',
        11,
        2
    )
    dynamic_text(
        screen,
        f'Answered wrong: {ques - CORRECT}/{ques}',
        12,
        2
    )
    insert_text(
        screen,
        f'Total questions answered: {ques}',
        13,
        2
    )
    print_screen(screen)
    sleep(4)
    if TIMES:
        os.system('clear')
        width, height = gts()
        screen = make_screen(width, height)
        insert_text(
            screen,
            'Press Ctrl + C to skip.',
            len(screen)-6,
            2
        )
        insert_text(
            screen,
            'TIMES',
            4,
            len(screen[0])//2 - 2
        )
        dynamic_text(
            screen,
            f'Best time in this session: {min(TIMES)}',
            6,
            2
        )
        dynamic_text(
            screen,
            f'Average: {sum(TIMES)/len(TIMES)}',
            8,
            2
        )
        dynamic_text(
            screen,
            f'Slowest: {max(TIMES)}',
            10,
            2
        )
        print_screen(screen)


def leaderboard(name: str):
    os.system('clear')
    print("\n\n\t\\:: Quick Solver 3.6.0::/\n\n")
    print('\nPress Ctrl + C to skip.\n')
    with open(
            f"{expuser('~')}/.qsi/quick_solver_scores.json"
    ) as f:
        data = json.load(f)
    data = {
        k: float(v)
        for k, v in data.items()
    }
    data = dict(
        sorted(
            data.items(),
            key=lambda x: x[1],
            reverse=True
        )
    )
    if len(data.keys()) == 1:
        print("\n\nNOTE: More than one player can play on this device with different usernames, so the leader board doesn't have only one player to show!\n")
        print("Even you can compete with yourself with different usernames!!\n")
    print(
        "_"*66 +
        "\nLeaderboard:-" +
        (" "*53) +
        "|"
    )
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

        spaces_to_add2 = (
            66 -
            (
                2 +
                len(str(idx)) +
                3 +
                len(curname) +
                18 +
                len(str(score))
            )
        )

        if umcn == name:
            print(
                f"| {idx} | {curname}(You)    | score: {score}",
                end=""
            )
            print(
                " "*spaces_to_add2 + "|"
            )
        else:
            print(
                f'| {idx} | {curname}         | score: {score}',
                end=""
            )
            print(
                " "*spaces_to_add2 + "|"
            )
        sleep(1)
    print("_"*66 + "|\n\n")

    print("PLAYER BADGES: ")
    sleep(1)
    with open(
            expuser(
                "~/.qsi/quick_badges.json"
            )
    ) as f:
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

        spaces_to_add2 = (
            66 -
            (
                2 +
                len(str(idx)) +
                3 +
                len(player) +
                13 +
                len(str(pbadges[umpn])) +
                1
            )
        )

        print(
            f"| {idx} | {player}    | badge: {pbadges[umpn]} ",
            end=""
        )
        print(" "*spaces_to_add2 + "|")
        sleep(1)
    print("_"*66 + "|\n\n")


def account() -> bool | None:
    global NAME
    log_out = False
    focus = 0
    buttons = {
        0: 'change username',
        1: 'log out',
        2: 'back',
        3: 'Delete account'
    }
    new_name = None
    while 1:
        name = NAME
        os.system('clear')
        width, height = gts()
        if height < 21:
            height = 21
        screen = make_screen(
            width,
            height
        )
        n = name
        if len(name) > 15:
            n = name[:13] + '...'
        insert_text(
            screen,
            f'Name: {n}',
            3,
            2
        )
        insert_text(
            screen,
            'Badge: ' +
            str(get(
                name,
                "quick_badges"
            ) +
                f'        Score: {get(name, "quick_solver_scores")}'
            ),
            4,
            2
        )
        brow = 6
        for i in buttons:
            draw_button(
                screen,
                buttons[i],
                brow,
                2,
                focused=(focus == i)
            )
            brow += 3
        print_screen(screen)
        key = get_key()
        if key == '\x1b':
            get_key()
            key = get_key()
            if key == 'A':
                if focus > 0:
                    focus -= 1
            elif key == 'B':
                if focus < 3:
                    focus += 1
        elif (key == '\n' or
              key == '\r'):
            chosen = buttons[focus]
            if chosen == 'change username':
                new_name = username(changing=True)
                NAME = new_name
                with open(
                        expuser(
                            '~/.qsi/quick_solver_scores.json'
                        )
                ) as f:
                    data = json.load(f)
                score = data[name]
                data.pop(name)
                data[new_name] = score
                with open(
                        expuser(
                            '~/.qsi/quick_solver_scores.json'
                        ),
                        'w'
                ) as f:
                    json.dump(
                        data,
                        f,
                        indent=4
                    )

                with open(
                        expuser(
                            '~/.qsi/quick_badges.json'
                        )
                ) as f:
                    data = json.load(f)
                badge = data[name]
                data.pop(name)
                data[new_name] = badge

                with open(
                        expuser(
                            '~/.qsi/quick_badges.json'
                        ),
                        'w'
                ) as f:
                    json.dump(
                        data,
                        f,
                        indent=4
                    )

            elif chosen == 'log out':
                log_out = True
                break
            elif chosen == 'Delete account':
                screen2 = make_screen(*gts())
                buttons2 = {
                    0: 'Yes',
                    1: 'No'
                }
                insert_text(
                    screen2, 'Are you sure you want to delete your account?', 4, 2)

                focus2 = 0
                while 1:
                    os.system('clear')
                    bcol = 2

                    for i in range(2):
                        draw_button(
                            screen2,
                            buttons2[i],
                            6,
                            bcol,
                            (focus2 == i)
                        )
                        bcol += 8
                    print_screen(screen2)
                    key2 = get_key()
                    if key2 == '\n' or key2 == '\r':
                        chosen2 = buttons2[focus2]
                        break
                    elif key2 == '\x1b':
                        get_key()
                        key2 = get_key()
                        if key2 == 'D':
                            if focus2 == 1:
                                focus2 = 0
                        elif key2 == 'C':
                            if focus2 == 0:
                                focus2 = 1
                if chosen2 == 'Yes':
                    with open(expuser('~/.qsi/quick_badges.json'), 'r') as f:
                        data = json.load(f)

                    data.pop(NAME)
                    with open(expuser('~/.qsi/quick_solver_scores.json'), 'r') as f:
                        data2 = json.load(f)
                    data2.pop(NAME)

                    with open(expuser('~/.qsi/quick_badges.json'), 'w') as f:
                        json.dump(data, f, indent=4)

                    with open(expuser('~/.qsi/quick_solver_scores.json'), 'w') as f:
                        json.dump(data2, f, indent=4)
                    log_out = True
                    break
                elif chosen2 == 'No':
                    continue
            else:
                break

    return log_out


def home_screen() -> None:
    global SCORE, CORRECT, TIMES, BADGE, FORGIVEN, Multiplier, Bonus, NAME
    SCORE = 0
    CORRECT = 0
    TIMES = []
    FORGIVEN = None
    Multiplier = 1
    Bonus = 0
    focus = 0
    buttons = {
        0: 'Play',
        1: 'Account',
        2: 'Leaderboard',
        3: 'Exit'
    }
    if not NAME:
        NAME = username()
    while 1:

        os.system('clear')
        screen = make_screen(
            *gts()
        )
        insert_text(
            screen,
            'Home',
            4,
            len(screen[0])//2 - 2
        )
        insert_text(
            screen,
            'Use arrow keys to navigate and "Enter" to click.',
            5,
            len(screen[0])//2 - 24
        )
        nme = NAME
        if len(nme) > 18:
            nme = nme[:15] + '...'
        insert_text(
            screen,
            'Player: ' +
            nme,
            7,
            len(screen[0])//2 -
            (
                (
                    8 + len(nme)
                ) // 2
            )
        )
        brow = 9
        bcol1 = len(screen[0])//2 - 12

        draw_button(
            screen,
            buttons[0],
            brow,
            bcol1,
            focused=(
                focus == 0
            )
        )
        draw_button(
            screen,
            buttons[1],
            brow,
            bcol1 +
            14,
            focused=(
                focus == 1
            )
        )
        draw_button(
            screen,
            buttons[2],
            brow + 4,
            bcol1,
            focused=(
                focus == 2
            )
        )
        draw_button(
            screen,
            buttons[3],
            brow + 4,
            bcol1 + 16,
            focused=(
                focus == 3
            )
        )
        print_screen(screen)
        key = get_key()
        if key == '\x1b':
            get_key()
            key = get_key()
            if key == 'A':
                if focus == 2:
                    focus = 0
                elif focus == 3:
                    focus = 1
            elif key == 'D':
                if focus == 1:
                    focus = 0
                elif focus == 3:
                    focus = 2
            elif key == 'C':
                if focus == 0:
                    focus = 1
                elif focus == 2:
                    focus = 3
            elif key == 'B':
                if focus == 0:
                    focus = 2
                elif focus == 1:
                    focus = 3

        elif key == '\n' or key == '\r':
            chosen = buttons[focus]

            if chosen == 'Play':
                play(NAME)
            elif chosen == 'Account':
                if account():
                    NAME = None
                    break
            elif chosen == 'Leaderboard':
                leaderboard(NAME)
            else:
                sys.exit()


def play(name: str) -> None:
    global CORRECT
    global SCORE
    global FORGIVEN
    global Multiplier
    global Bonus
    global TIMES
    global Badges_scores

    CORRECT = 0
    SCORE = 0
    TIMES = []
    FORGIVEN = None
    Multiplier = 1
    Bonus = 0

    if BADGE != 'No Badge Yet':
        os.system('clear')
        screen = make_screen(
            *gts()
        )

        badge_bonus(
            get(
                name,
                'quick_badges'
            )
        )
        dynamic_text(
            screen,
            'Dear ' +
            name +
            ',',
            4,
            2
        )
        dynamic_text(
            screen,
            'In this session, the advantages you will get because of your badge are: ',
            6,
            2
        )
        insert_text(
            screen,
            f'Score Multiplier: {
                Multiplier} This means the score you get after each correct answer will be multiplied by the same.',
            8,
            2
        )
        insert_text(
            screen,
            'Bonus score added: ' +
            str(Bonus),
            10,
            2
        )
        if FORGIVEN:
            insert_text(
                screen,
                'In this session ' +
                str(FORGIVEN) +
                ' mistakes will be forgiven.',
                12,
                2
            )
        insert_text(
            screen,
            'Press any key to proceed.',
            len(screen) - 2,
            2
        )

        print_screen(screen)
        get_key()

    lvl = level()
    ques = questions()
    for i in range(5, 0, -1):
        os.system('clear')
        width, height = gts()
        screen = make_screen(width, height)
        insert_text(
            screen,
            'We are starting in....',
            4,
            len(screen[0])//2 - 11
        )
        num = text2art(
            str(i)
        ).splitlines()
        num = [
            [
                j
                for j in i
            ] for i in num
        ]
        for i in range(len(num)):
            for j in range(len(num[0])):
                screen[6 + i][
                    (
                        len(screen[0]) // 2 -
                        (
                            len(num[0]) // 2
                        )
                    ) + j
                ] = num[i][j]
        print_screen(screen)
        sleep(1)
    for i in range(1, ques + 1):
        ask_and_calculate(lvl, i, ques)
    store(
        str(
            float(
                get(
                    name,
                    "quick_solver_scores"
                )
            ) +
            SCORE
        ),
        name,
        "quick_solver_scores"
    )
    if BADGE != badges(name):

        store(
            badges(name),
            name,
            "quick_badges"
        )
        stats(name, ques, True)
    else:
        stats(name, ques)
    sleep(3)
    leaderboard(name)
    sleep(3)


def want_desktop() -> None:

    buttons = {
        0: "Yes",
        1: "No"
    }
    focus = 0
    while 1:
        os.system('clear')
        size = gts()
        screen = make_screen(*size)
        insert_text(
            screen,
            'Do you want the game icon in your desktop screen??',
            4,
            2
        )
        insert_text(
            screen,
            'Use arrow keys to choose from buttons and press enter to click.',
            6,
            2
        )
        bcol = 3
        for i, b in enumerate(buttons):
            draw_button(
                screen,
                buttons[b],
                7,
                bcol,
                focused=(
                    i == focus
                )
            )
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
        os.system(
            expuser(
                "bash ~/.qsi/qsi4dsktp.sh"
            )
        )


def ask_update() -> bool:
    if not os.path.exists(
            expuser(
                "~/.qsi/update_manager.json"
            )
    ):
        with open(
                expuser(
                    "~/.qsi/update_manager.json"
                ),
                "w"
        ) as f:
            data = {
                "wait time": 0,
                "last update": date.today().isoformat()
            }
            json.dump(
                data,
                f,
                indent=4
            )
        return True

    with open(
            expuser(
                "~/.qsi/update_manager.json"
            )
    ) as f:
        data = json.load(f)
    last_update = date.fromisoformat(
        data["last update"]
    )
    now = date.today()
    days_passed = (now - last_update).days
    if days_passed >= data["wait time"]:
        data["last update"] = now
        return True
    return False


def check_updates() -> None:
    if ask_update():
        try:
            with open(
                    f"{expuser('~')}/.Quick_Solver/version.txt") as f:
                current_version = f.read().strip()
            url = LATEST_VERSION_URL

            response = requests.get(url)

            if response.status_code == 200:
                latest_version = response.text.strip()

                if (latest_version !=
                        current_version):
                    url2 = RELEASE_NOTES_URL
                    new = requests.get(url2)
                    if new.status_code == 200:
                        new = new.text.strip()
                    else:
                        new = "\n\nError: failed to fetch 'what's new' section, kindly check your internet connection, if your connection is good, continue by ignoring...\n\n"
                    print(
                        f"""
{"="*67}
\\:: IMPORTANT NOTE ::/
Update Available!!

Version {latest_version} is available.
Your currently installed version: {current_version}
{new}
                    """
                    )
                    screen = [
                        [
                            ' '
                            for _ in range(
                                gts().columns
                            )
                        ] for _ in range(8)
                    ]
                    focus = 0
                    buttons = {
                        0: "Yes",
                        1: 'No'
                    }
                    sleep(2)
                    while 1:
                        insert_text(
                            screen,
                            'Do you want to update?',
                            0,
                            len(screen[0])//2 - 11)
                        insert_text(
                            screen,
                            'Use arrow keys to choose from buttons and press enter to click.',
                            2,
                            2
                        )
                        bcol = 4
                        for b in buttons:
                            draw_button(
                                screen,
                                buttons[b],
                                4,
                                bcol,
                                focused=(
                                    b == focus
                                )
                            )
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
                        elif (key == '\r' or
                              key == '\n'):
                            chosen = buttons[focus]
                            break
                        os.system('clear')
                    if chosen == 'Yes':
                        with open(
                                expuser(
                                    "~/.qsi/update_manager.json"
                                )
                        ) as f:
                            data = json.load(f)
                        if data["wait time"] > 0:
                            data["wait time"] -= 1
                            with open(
                                    expuser(
                                        "~/.qsi/update_manager.json"
                                    ),
                                    "w"
                            ) as f:
                                json.dump(
                                    data,
                                    f,
                                    indent=4
                                )
                        os.system(
                            expuser(
                                'bash ~/.qsi/qsi4update.sh'
                            )
                        )
                        sys.exit()
                    with open(
                            expuser(
                                "~/.qsi/update_manager.json"
                            )
                    ) as f:
                        data = json.load(f)
                    if data["wait time"] < 10:
                        data["wait time"] += 1
                    with open(
                            expuser(
                                "~/.qsi/update_manager.json"
                            ),
                            "w"
                    ) as f:
                        json.dump(
                            data,
                            f,
                            indent=4
                        )

            else:
                print("\n\nError: Couldn't check for updates, make sure your internet connection is good. If it is, then the server might be down or some other problem to check for updates.\n\n")
        except Exception as e:
            print('Error: ', e)
            print("\n\nTo CHECK FOR UPDATES you need internet connection and if your internet is good, then it might be the server having issues.")


def main():
    while 1:
        try:
            home_screen()
        except (
                KeyboardInterrupt,
                EOFError
        ):
            pass


if __name__ == "__main__":
    if not os.path.exists(
        expuser(
            '~/.Quick_Solver/first.txt'
        )
    ):
        want_desktop()

    check_updates()
    main()
