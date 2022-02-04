# ******************************************************************************
# Author:           Proxima-L3
# Date:             August 2, 2020
# Description:      A program that simulates the bounty terminals seen in Star
#                   Wars cantinas and bars.
# Input:            Login information for both bounty hunter and benefactor
#                   accounts as well as accept, create, and delete bounty options
# Output:           Information regarding bounty boards and posters (for bounty
#                   hunters) and information regarding hunter and benefactor
#                   accounts.
# Sources:          None. (Except minimal review from one of my Udemy courses)
# ******************************************************************************

# CONSTANTS
BOUNTY_BOARD = 1
HUNTER_LOGIN = 2
BENEFACTOR_LOGIN = 3
HUNTER_SETUP = 4
BENEFACTOR_SETUP = 5
QUIT = 6


def main():
    # variables
    menu_choice = 0
    hunter_list = []
    benefactor_list = []
    target_list = []

    # pre loop operations
    print("Bounty Terminal")
    input("\n(press enter to continue)")
    print("\033[H\033[J")

    # main program loop
    while menu_choice != QUIT:

        # display main menu and give user 6 options
        menu()
        menu_choice = get_main_menu_choice()

        # option pathways
        if menu_choice == BOUNTY_BOARD:
            while True:
                board_choice = bounty_board(target_list)
                if board_choice in ['b', 'B']:
                    print("\033[H\033[J")
                    break
                else:
                    board_choice = int(board_choice) - 1
                    while True:
                        login_decision = bounty_poster(board_choice,
                                                       target_list)
                        if login_decision in ['b', 'B']:
                            print("\033[H\033[J")
                            break
                        else:
                            selected_hunter = hunter_login(hunter_list)
                            accept_bounty(selected_hunter, board_choice,
                                          target_list)
                            break
        elif menu_choice == HUNTER_LOGIN:
            selected_hunter = hunter_login(hunter_list)
            hunter_account(selected_hunter)
        elif menu_choice == BENEFACTOR_LOGIN:
            selected_benefactor = benefactor_login(benefactor_list)
            while True:
                bounty_decision = benefactor_account(selected_benefactor)
                if bounty_decision == 1:
                    post_bounty(selected_benefactor, target_list)
                elif bounty_decision == 2:
                    if selected_benefactor.posted_bounties == []:
                        print("\033[H\033[J")
                        print("You have no bounties to delete\n")
                        input("(Press enter to go back to benefactor profile)")
                    else:
                        delete_bounty(selected_benefactor, target_list)
                else:
                    break
        elif menu_choice == HUNTER_SETUP:
            hunter_setup(hunter_list)
        elif menu_choice == BENEFACTOR_SETUP:
            benefactor_setup(benefactor_list)
        else:
            menu_choice = QUIT

    print("\n\nGo get 'em killer!")


# CLASSES

# class for bounty hunter objects
class BountyHunter():

    def __init__(self, name, password, current_bounties):
        self.name = name
        self.password = password
        self.current_bounties = current_bounties

    def __str__(self):
        print(self.name)
        print("Current bounties:")
        for bounty in self.current_bounties:
            print('\t' + bounty)

    def add_target(self, target_name):
        self.current_bounties.append(target_name)


# class for target objects
class Target():

    def __init__(self, name, aliases, species, homeworld, sex, age, height,
                 weight, last_seen, reward, benefactor, hunters):
        self.name = name
        self.aliases = aliases
        self.species = species
        self.homeworld = homeworld
        self.sex = sex
        self.age = age
        self.height = height
        self.weight = weight
        self.last_seen = last_seen
        self.reward = reward
        self.benefactor = benefactor
        self.hunters = hunters

    def __str__(self):
        return f"Name: {self.name}\t\tSex: {self.sex}\n" \
               f"Aliases: {self.aliases}\t\tAge: {self.age}\n" \
               f"Species: {self.species}\t\tHeight: {self.height}\n" \
               f"Homeworld: {self.homeworld}\t\tWeight: {self.weight}\n" \
               f"Last Seen: {self.last_seen}\n\n\nReward: {self.reward}\n" \
               f"Benefactor: {self.benefactor}\n" \
               f"Hunters in Pursuit: {self.hunters}"

    def add_hunter(self, new_hunter):
        self.hunters.append(new_hunter)

    def location_update(self, new_loc):
        self.last_seen = new_loc


# class for benefactor objects
class Benefactor():

    def __init__(self, name, password, posted_bounties):
        self.name = name
        self.password = password
        self.posted_bounties = posted_bounties

    def __str__(self):
        return f"{self.name}"


# FUNCTIONS

# This function displays the main menu
def menu():
    print(
        "1: Bounty Board\n2: Bounty Hunter Account (login)\n"
        "3: Benefactor Account (login)\n4: Setup Bounty Hunter Account\n"
        "5: Setup Benefactor Account\n6: Quit")


# This function validates the user's main menu choice and returns it
def get_main_menu_choice():
    while True:
        try:
            x = int(input("\n\nEnter option: "))
            if 0 < x < 7:
                break
            else:
                print("Invalid option.")
        except:
            print("Invalid option.")
    return x


# This function displays the bounty board and allows the user to pick a
# bounty to see more details
def bounty_board(target_list):
    print("\033[H\033[J")
    print("Bounty Board\n\n\n\n\tBounty\t\tTarget\t\tBenefactor\n")
    counter = 1
    for target in target_list:
        print(f"{counter}. {target.reward}\t\t{target.name}"
              f"\t\t{target.benefactor}")
        counter += 1

    while True:
        bounty_choice = input("\n\nEnter bounty number for more details\n"
                              "(enter b to go back to the menu)\n")
        if bounty_choice in str(list(range(1, len(target_list) + 1))):
            if bounty_choice in [',', '[', ']', ' ', '']:
                print("Invalid option.")
            else:
                break
        elif bounty_choice in ['b', 'B']:
            return bounty_choice
        else:
            print("Invalid option.")

    return bounty_choice


# This function displays the poster for the bounty that the user chose on the
# bounty board and allows them to decide whether they want to login to accept
# the bounty or return to the bounty board
def bounty_poster(bounty_choice, target_list):
    print("\033[H\033[J")
    print("Wanted\n(Dead or Alive)\n\n")
    print(target_list[bounty_choice])

    print("\n\n(Login to accept bounty)")
    while True:
        user_choice = input("(Press Enter to login. Press b to return to the "
                            "bounty board.)\n")
        if user_choice in ['', 'b', 'B']:
            break
        else:
            print("Invalid option.\n")

    return user_choice


# This function allows the user to accept or decline a bounty that they are
# looking at
def accept_bounty(selected_hunter, bounty_choice, target_list):

    selected_target = target_list[bounty_choice]

    print("\033[H\033[J")
    print(selected_target)
    print("\n\n\t\tAccept\t\tDecline")

    while True:
        user_choice = input("\n\t\t  Enter a or d\n").lower()
        if user_choice in ['a', 'd', 'accept', 'decline']:
            break
        else:
            print("Invalid option")

    if user_choice in ['a', 'accept']:
        if selected_hunter.name not in selected_target.hunters:
            selected_target.add_hunter(selected_hunter.name)
            selected_hunter.add_target(selected_target.name)
            print("\n\nTarget added to personal list")
            input("(Press enter to go back to bounty board)")
    else:
        pass


# This function allows the user to login to their bounty hunter account
def hunter_login(hunter_list):

    selected_hunter = ""
    print("\033[H\033[J")
    print("Bounty Hunter login\n\n")

    # Ask for hunter name
    while selected_hunter == "":
        name = input("Please enter your name: ")
        for obj in hunter_list:
            if obj.name == name:
                selected_hunter = obj
        if selected_hunter == "":
            print("Hunter not in database\n")

    # Ask for password
    while True:
        try:
            password = input("Please enter your password: ")
            if password == selected_hunter.password:
                break
            else:
                print("Password incorrect. Please try again\n")
        except:
            print("Error!")

    return selected_hunter


# This function displays information in the currently logged in bounty hunter
# account
def hunter_account(selected_hunter):

    print("\033[H\033[J")
    print(f"Profile: {selected_hunter.name}\n")

    print("Current bounties:")
    for item in selected_hunter.current_bounties:
        print(f"\t- {item}")

    input("\n\n(Press enter to return to the main menu)")
    print("\033[H\033[J")


# This function allows the user to login to their benefactor account
def benefactor_login(benefactor_list):

    selected_benefactor = ""
    print("\033[H\033[J")
    print("Benefactor login\n\n")

    # Ask for benefactor name
    while selected_benefactor == "":
        name = input("Please enter your name: ")
        for obj in benefactor_list:
            if obj.name == name:
                selected_benefactor = obj
        if selected_benefactor == "":
            print("Benefactor not in database\n")

    # Ask for password
    while True:
        try:
            password = input("Please enter your password: ")
            if password == selected_benefactor.password:
                break
            else:
                print("Password incorrect. Please try again\n")
        except:
            print("Error!\n")

    return selected_benefactor


# This function displays information in the currently logged in benefactor
# account and also allows the user to choose whether they want to post or
# delete a bounty or return to the main menu
def benefactor_account(selected_benefactor):

    print("\033[H\033[J")
    print(f"Profile: {selected_benefactor.name}\n")
    print("Your posted bounties:")
    for item in selected_benefactor.posted_bounties:
        print(f"- {item}")
    print("\n\n\n\n1: Post bounty\n2: Delete bounty\n3: Main menu\n\n")

    while True:
        try:
            user_choice = int(input("Enter option: "))
            if user_choice in [1, 2, 3]:
                break
            else:
                print("Invalid option.\n")
        except:
            print("Invalid option.\n ")

    print("\033[H\033[J")

    return user_choice


# This function collects information from the user to create and post a bounty
def post_bounty(selected_benefactor, target_list):

    print("\033[H\033[J")
    print("Post Bounty\n\n")

    print("Please enter as much information as you can about the target\n")
    name = input("Target name: ")
    aliases = input("Other aliases: ")
    species = input("Target species: ")
    homeworld = input("Target homeworld: ")
    sex = input("Target sex: ")
    age = input("Target age: ")
    height = input("Target height: ")
    weight = input("Target weight: ")
    last_seen = input("Last seen location: ")
    reward = input("Reward amount: ")
    benefactor = selected_benefactor.name
    hunters = []

    target_list.append(
        Target(name, aliases, species, homeworld, sex, age, height, weight,
               last_seen, reward, benefactor, hunters))

    selected_benefactor.posted_bounties.append(name)

    print("\n\nTarget added to public bounty board")
    input("\n(press enter to go back to benefactor profile)")


# This function displays all bounties that the currently logged in benefactor
# has posted and allows them to delete any one of them
def delete_bounty(selected_benefactor, target_list):

    print("\033[H\033[J")
    print("Delete Bounty\n\n")

    print("Your posted bounties:")
    benefactor_bounties = selected_benefactor.posted_bounties
    counter = 1
    for item in benefactor_bounties:
        print(f"{counter}. {item}")
        counter += 1

    while True:
        try:
            delete_choice = int(input("\nEnter bounty number to remove "
                                      "target from public bounty board: "))
            if delete_choice in range(1, len(benefactor_bounties) + 1):
                break
            else:
                print("Invalid option.")
        except:
            print("Invalid option.")

    name = benefactor_bounties.pop(delete_choice - 1)

    # deletes target from target list
    selected_target = [obj for obj in target_list if obj.name == name][0]
    target_list.remove(selected_target)

    print("Target removed from public bounty board")
    input("\n\n(press enter to go back to benefactor profile)")


# This function allows the user to setup a new bounty hunter account
def hunter_setup(hunter_list):

    bounty_list = []
    print("\033[H\033[J")
    print("(Enter b anytime to return to main menu)\n\n")

    while True:
        name = input("Please enter your name: ")
        if name == 'b':
            print("\033[H\033[J")
            break

        password = input("Please choose a password: ")
        if password == 'b':
            print("\033[H\033[J")
            break

        hunter_list.append(BountyHunter(name, password, bounty_list))

        print("\n\nWelcome to the Guild, killer!")
        input("\n")
        print("\033[H\033[J")
        break


# This function allows the user to setup a new benefactor account
def benefactor_setup(benefactor_list):

    bounty_list = []
    print("\033[H\033[J")
    print("(Enter b anytime to return to main menu)\n\n")

    while True:

        name = input("Please enter benefactor title: ")
        if name == 'b':
            print("\033[H\033[J")
            break

        password = input("Please choose a password: ")
        if password == 'b':
            print("\033[H\033[J")
            break

        benefactor_list.append(Benefactor(name, password, bounty_list))

        print("\n\nLooking forward to doing business with you, friend!")
        input("\n")
        print("\033[H\033[J")
        break




main()
