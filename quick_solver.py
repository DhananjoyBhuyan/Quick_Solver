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

    _add2json(f"{os.path.expanduser('~')
                 }/.Quick_Solver/{database_name}", key, data)


def get(key: str,
        database_name: str):

    database_name += '.json'
    if os.path.exists(f"{os.path.expanduser('~')}/.Quick_Solver/{database_name}"):
        with open(f"{os.path.expanduser('~')}/.Quick_Solver/{database_name}") as f:
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
            print("Alright")
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
                        break

                else:
                    print("\nPlease enter either yes or no.\n")
    else:
        print("\n\nError: Couldn't check for updates, if you internet is not turned on then please connect to internet.. if you're already connected to internet, then continue by ignoring this message....\n\n")


def generate_questions(level: int = 1):
    operations = ["+", "-", "*", "/"]
    chosen_op = choice(operations)

    if chosen_op == '/':
        num2 = randint(1, 10)
        num1 = num2*randint(1, 10)
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
            SCORE += 100
        elif time_taken < 2:
            print("Score + 50!! You did it under 2 seconds, wow!!")
            SCORE += 50
        elif time_taken < 3:
            print("Score + 10, time taken less than 3 seconds...")
            SCORE += 10
        elif time_taken < 5:
            print("Score + 8, time taken less than 5 seconds...")
            SCORE += 8
        elif time_taken < 10:
            print("Score + 5, time taken less than 10 seconds...")
            SCORE += 5
        else:
            print("Score + 1, VERY SLOW!! But it's okay practice will make you perfect.")
            SCORE += 1
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
    name = get_name()

    try:
        score = get(name, "quick_solver_scores")
        print("Logging in....")
        sleep(1.5)
        print(f"\nWelcome back {name} your current score is {score}\n")
        sleep(1)
    except:
        print("\nNew user detected, creating account.....")
        sleep(1.5)
        store("0", name, 'quick_solver_scores')
        print(f"\n\nHello {name}!!\n\n")
        sleep(1)
    return name


def leaderboard(name):
    global SCORE
    with open(f"{os.path.expanduser('~')}/.Quick_Solver/quick_solver_scores.json") as f:
        data = json.load(f)
    data[name] = str(int(data[name]) + SCORE)
    data = {k: int(v) for k, v in data.items()}
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


def play():
    global CORRECT
    global SCORE
    global NAME

    CORRECT = 0
    SCORE = 0
    TIMES = []

    if not os.path.exists(os.path.expanduser("~/.Quick_Solver/first.txt")):
        with open(os.path.expanduser("~/.Quick_Solver/first.txt"), "w") as f:
            f.write("This file was created when the game was first launched on this device.")

    print("\\:: Quick Solver ::/")
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

    print("\nPlayer Name: ", name)
    sleep(1)
    print("\nToday's score: ", SCORE)
    sleep(1)
    print("\nTotal score: ", int(get(name, "quick_solver_scores")) + SCORE)
    sleep(1)
    print(f'\nAnswered correct: {CORRECT}/{ques}')
    sleep(1)
    print(f"\nAnswered wrong: {ques - CORRECT}/{ques}")
    sleep(1)
    print(f"\nTotal questions attempted: {ques}")
    sleep(1)
    if TIMES:

        print("\nBest time: ", min(TIMES))
        sleep(1)
        print("\nAverage time: ", sum(TIMES)/len(TIMES))
        sleep(1)
        print("\nSlowest time: ", max(TIMES))
    leaderboard(name)

    store(str(int(get(name, "quick_solver_scores")) + SCORE),
          name, "quick_solver_scores")
    sleep(1.8)
    NAME = name


def main():
    while 1:
        try:
            play()
        except ValueError:
            print("Error: INVALID INPUT, game crashed, restarting...")
            sleep(1.8)
            continue
        again = input(f"Do you want to play again?\nSolve more {
                      NAME}?? (Yes/No): ").lower().strip()
        if 'no' in again or 'na' in again or 'nh' in again or again == "n" or 'nopy' in again:
            break


if not os.path.exists(os.path.expanduser("~/.Quick_Solver/first.txt")):
    want_desktop()
check_updates()
main()
