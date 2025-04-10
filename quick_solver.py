#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 03:32:08 2025

@author: Dhananjoy Bhuyan
"""
import requests
from random import randint, choice
from time import time, sleep
import sys
import json
import os

SCORE = 0
CORRECT = 0
TIMES = []
NAME = None
BADGE = None
FORGIVEN = None
Multiplier = 1
Bonus = 0


def badge_bonus(badge: str):
    global FORGIVEN
    global Multiplier
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


def want_desktop():
    print("Do you want the game icon to appear in the desktop as well?")
    a = input("Yes/No (default is yes): ").lower().strip()
    nos = ["no", "nah", "nopy", "nh", "na"]
    for i in nos:
        if i in a:
            print("Alright\n\n")
            return None
    if a == 'n':
        print("Alright....")
        return None
    os.system(os.path.expanduser("bash ~/.qsi/qsi4dsktp.sh"))


def check_updates():

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
            while 1:
                update = input(
                    "Do you want to update it?\n(Yes/No): ").lower().strip()
                if update:
                    if 'no' in update.lower() or 'nope' in update or 'nah' in update or 'nopy' in update or update == 'no' or update == 'n' or 'nh' in update:
                        print("Alright.")
                        break
                    else:
                        print("Updating.....")
                        os.system(os.path.expanduser(
                            "bash ~/.qsi/qsi4update.sh"))

                        sys.exit()

                else:
                    print("\nPlease enter either yes or no.\n")
    else:
        print("\n\nError: Couldn't check for updates, if you internet is not turned on then please connect to internet.. if you're already connected to internet, then continue by ignoring this message....\n\n")


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


def ask_and_calculate(level: int = 1):
    global SCORE
    global CORRECT
    global TIMES
    global Multiplier
    global FORGIVEN

    print("Question: -")
    question = generate_questions(level)
    answer = str(int(eval(question)))

    print("\n"+question+"\n")
    start = time()
    user_answer = input("Your answer: ")
    end = time()

    if user_answer == answer:
        print("Correct!!")
        time_taken = end - start
        TIMES.append(float(f"{time_taken:.3f}"))
        print(f'You took: {time_taken:.3f} seconds!!')
        sleep(1)
        CORRECT += 1
        print("\n")
        if time_taken < 1:
            print("Whoa!! You just did it under 1 second! Score + 100.")
            SCORE += (100*Multiplier)

        elif time_taken < 2:
            print("Score + 50!! You did it under 2 seconds, wow!!")
            SCORE += (50*Multiplier)
        elif time_taken < 3:
            print("Score + 10, time taken less than 3 seconds...")
            SCORE += (10*Multiplier)
        elif time_taken < 5:
            print("Score + 8, time taken less than 5 seconds...")
            SCORE += (8*Multiplier)
        elif time_taken < 10:
            print("Score + 5, time taken less than 10 seconds...")
            SCORE += (5*Multiplier)
        else:
            print("Score + 1, VERY SLOW!! But it's okay practice will make you perfect.")
            SCORE += (1*Multiplier)
    else:
        if FORGIVEN not in [None, 0]:
            FORGIVEN -= 1
            print(
                f"\nWrong answer forgiven...Score + 2\nThe correct answer was {answer}")
            SCORE += (2*Multiplier)
        else:
            print(f"Wrong answer!!\nThe correct answer was {answer}")


def get_name():
    while 1:
        name = input("Enter your username: ")
        if not name:
            print("Please enter your username.")
            continue
        else:
            return name


def log_in():
    global BADGE
    global SCORE
    global FORGIVEN
    name = get_name()

    try:
        score = get(name, "quick_solver_scores")
        BADGE = get(name, "quick_badges")
        print("Logging in....")
        sleep(1.5)
        print(f"\nWelcome back {name} your current score is {score}\n")
        sleep(1)
    except:
        print("\nNew user detected, creating account.....")
        sleep(1.5)
        store("0", name, 'quick_solver_scores')
        BADGE = badges(name)
        store(badges(name), name, "quick_badges")
        print(f"\n\nHello {name}!!\n\n")
        sleep(1)
    if BADGE != "No Badge Yet":
        badge_bonus(BADGE)
        print(f"{BADGE} Badge Daily Login Bonus:\n")
        sleep(1)
        print(f"Score + {Bonus}")
        SCORE += Bonus
        sleep(1)
        print(
            f"\n{BADGE} badge score multiplier: {Multiplier}, this means everytime you answer a question, your score gets multiplied by {Multiplier}!!")
        sleep(1)
        if FORGIVEN:
            print(
                f"\nIn this session, {FORGIVEN} wrong answers will be forgiven because you have a {BADGE} badge!!")
            sleep(1)
    return name


def leaderboard(name):
    global SCORE
    with open(f"{os.path.expanduser('~')}/.qsi/quick_solver_scores.json") as f:
        data = json.load(f)
    data = {k: float(v) for k, v in data.items()}
    data = dict(sorted(data.items(), key=lambda x: x[1], reverse=True))
    if len(data.keys()) == 1:
        print("\n\nNOTE: More than one player can play on this device with different usernames, so the leader board doesn't have only one player to show!\n")
        print("Even you can compete with yourself with different usernames!!\n")
    print("_"*67 + "\nLeaderboard:-")
    print("_"*67)
    sleep(1)
    for idx, curname in enumerate(data, 1):
        score = data[curname]
        if curname == name:
            print(f"| {idx} | {curname}(You)          score: {score}")
        else:
            print(f'| {idx} | {curname}               score: {score}')
        sleep(1)
    print("_"*67 + "\n\n")


def questions():
    while 1:
        try:
            noq = int(input(
                "How many questions are you willing to solve in this session?\nNumber of questions: "))
            return noq
        except ValueError:
            print("Invalid input!!")
            continue


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


def play():
    global BADGE
    global CORRECT
    global SCORE
    global NAME

    CORRECT = 0
    SCORE = 0
    TIMES = []

    if not os.path.exists(os.path.expanduser("~/.Quick_Solver/first.txt")):
        with open(os.path.expanduser("~/.Quick_Solver/first.txt"), "w") as f:
            f.write(
                "This file was created when the game was first launched on this device.")

    print("\\:: Quick Solver 2.3.0 ::/")
    sleep(0.2)
    print("Starting....")
    sleep(0.8)
    name = log_in()

    level = input("""
Which level of questions do you want?
1. Beginner
2. Intermediate
3. Pro
4. Master
5. Legend
Enter level number (1-5): """).strip()

    if level in "1 2 3 4 5".split(" "):
        ques = questions()

        print("""
Points to remember:-

1. "*" means multiply
2. "/" means divide

Read the above points clearly, or you might screw up.\n""")

        for i in range(5, 0, -1):
            sleep(1)
            sys.stdout.write(f"\r We are starting in {i:.0f}")
        print()

        for _ in range(ques):
            ask_and_calculate(int(level))
            sleep(1.5)

    else:
        print("\nYou should've entered a level number from 1 to 5..\n")
        sleep(1)
        raise ValueError("Invalid input was given.")

    store(str(float(get(name, "quick_solver_scores")) + SCORE),
          name, "quick_solver_scores")

    print("\nPlayer Name: ", name)
    sleep(1)
    print("\nToday's score: ", SCORE)
    sleep(1)
    print("\nTotal score: ", get(name, "quick_solver_scores"))
    sleep(1)
    if BADGE != badges(name):
        print("\nNEW BADGE UNLOCKED!!!")
        sleep(1)
    BADGE = badges(name)
    store(badges(name), name, "quick_badges")
    print("\nPlayer badge: ", BADGE)
    sleep(1)
    print(f'\nAnswered correct: {CORRECT}/{ques}')
    sleep(1)
    print(f"\nAnswered wrong: {ques - CORRECT}/{ques}")
    sleep(1)
    print(f"\nTotal questions attempted: {ques}")
    sleep(1)
    if TIMES:

        print("\nToday's best time: ", min(TIMES))
        sleep(1)

        sleep(1)
        print("\nAverage time: ", sum(TIMES)/len(TIMES))
        sleep(1)
        print("\nSlowest time: ", max(TIMES))
        sleep(1)

    leaderboard(name)

    NAME = name


def main():
    while 1:
        try:
            play()
        except ValueError:
            raise
            sleep(1.8)
            continue
        again = input(
            f"Do you want to play again?\nSolve more {NAME}?? (Yes/No): ").lower().strip()
        if 'no' in again or 'na' in again or 'nh' in again or again == "n" or 'nopy' in again:
            break


if not os.path.exists(os.path.expanduser("~/.Quick_Solver/first.txt")):
    want_desktop()
check_updates()
main()
