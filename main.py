from pickle import NONE
import numpy as np
import pandas as pd
from os.path import exists
import warnings
from string import ascii_uppercase

from src.sits import Seats
from src.users import Users

warnings.filterwarnings("ignore")


def menu():
    print("----------------- MENU OPTIONS ------------------")
    print("    A. View All Plane Seats")
    print("    B. View User's Reservation")
    print("    C. Create new Reservations")
    print("    D. Update my Reservations")
    print("    E. Delete my Reservations")
    print("    F. Exit")
    print("-------------------------------------------------")


users_db_path = "src/db/users.txt"


users = Users()


def display_users():
    print("Users: \n")
    for user in users.get_all_user():
        print(user)
    print()


def save_user(name):
    users = pd.DataFrame(
        pd.read_csv(users_db_path, sep="\t", index_col=0)
        if exists(users_db_path)
        else {},
        columns=["name", "seats"],
    )
    new_user = pd.DataFrame([(name, np.nan)], columns=["name", "seats"])
    save_user = pd.concat([users, new_user], ignore_index=True)
    save_user.to_csv(users_db_path, sep="\t")


def check_if_user_exist(name):
    user = pd.read_csv(users_db_path, "\t", index_col=0)
    if name not in user.values:
        save_user(name)


def display_seats(name):
    seats = Seats(name)
    print(seats)
    print()


def start():
    global name
    name = input("Before we start, what is your name? ")
    if exists(users_db_path):
        check_if_user_exist(name)
    else:
        save_user(name)
    print()
    print(f"Welcome to Plane Seat Reservation program, {name}!")
    print()


start()

while True:
    menu()
    selection = input("How may I assist you today? ")
    print()

    if selection == "A":
        display_seats(name)

    elif selection == "B":
        while True:
            display_users()
            selected_user = input("Please select a user by typing their name: ")

            if selected_user == "!exit":
                break

            if selected_user not in users.get_all_user():
                while True:
                    selected_user = input(
                        "Error, Name does not exist! Please type the name agai: "
                    )
                    if selected_user in users.get_all_user():
                        display_seats(selected_user)
                        break
                    if selected_user == "!exit":
                        break
            else:
                display_seats(selected_user)
        print()

    elif selection == "C":

        reserved_seats = []
        for i in users.get_all_seats():
            s = i.split(",")
            reserved_seats += s

        while True:
            display_seats(name)
            reserve_seats_input = input("Which sits do you want to reserve?: ")

            if reserve_seats_input == "!exit":
                break

            if not any(
                map(lambda v: v in reserved_seats, reserve_seats_input.split(" "))
            ):
                seats = Seats(name)
                seats.reserve(reserve_seats_input)
                display_seats(name)
                print("Success")
            else:
                print("Not Available")

    elif selection == "D":
        letter = list(ascii_uppercase[:6])

        display_seats(name)
        change_input = input("What seats do you want to change? ")
        if change_input == "!exit":
            None

        number = change_input[:-1]
        char = change_input[-1]

        while int(number) >= 100 or char not in letter:
            change_input = input("Invalid chosen seat number. Please input again: ")
            if change_input == "!exit":
                break
            number = change_input[:-1]
            char = change_input[-1]
        else:
            change_to_input = input(f"Changing seat number {change_input} to: ")
            number = change_to_input[:-1]
            char = change_to_input[-1]
            while int(number) >= 100 or char not in letter:
                change_to_input = input(f"Changing seat number {change_input} to: ")
                number = change_to_input[:-1]
                char = change_to_input[-1]
                if change_input == "!exit":
                    break

            else:
                seats = Seats(name)
                seats.update(change_input, change_to_input)
                print("Successfully updated")
                display_seats(name)

    elif selection == "E":
        letter = list(ascii_uppercase[:6])

        display_seats(name)
        delete_input = input("What seats do you want to delete? ")
        if delete_input == "!exit":
            None

        number = delete_input[:-1]
        char = delete_input[-1]

        while int(number) >= 100 or char not in letter:
            delete_input = input("Invalid chosen seat number. Please input again: ")
            if delete_input == "!exit":
                break
            number = delete_input[:-1]
            char = delete_input[-1]

        else:

            seats = Seats(name)
            seats.delete(delete_input)
            print("Successfully delete seats")
            display_seats(name)
            print()

    elif selection == "F":
        print(f"Thank you, {name}!")
        print()
        print("-------------------------------------------------")
        start()
    else:
        print(
            "There seems to be an error in the code you entered. Please try again.\n(Note: Choice must be CAPITALIZED.)"
        )
        print()
