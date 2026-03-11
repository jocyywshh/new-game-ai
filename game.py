import sys


def main_menu():
    print("\n=== Demon Slayer Adventure ===")
    print("1. Start New Journey")
    print("2. Load Saved Journey")
    print("3. Help")
    print("4. Quit")
    choice = input("Choose an option: ")
    return choice


class Character:
    def __init__(self, name: str):
        self.name = name
        self.health = 100
        self.food = 100
        self.money = 50

    def show_stats(self):
        print(f"\n{self.name} stats:")
        print(f" Health: {self.health}")
        print(f" Food:   {self.food}")
        print(f" Money:  {self.money}")


def start_new_journey():
    print("\nStarting a new journey through the Taisho era...")
    name = input("Enter your demon slayer's name: ")
    player = Character(name)

    # simple game loop to demonstrate stat tracking
    while True:
        print("\n=== Journey Menu ===")
        print("1. View stats")
        print("2. Rest (lose food, regain health)")
        print("3. Visit JINYA Ramen Bar")
        print("4. Travel to a town")
        print("5. Visit market (spend money to gain food or health)")
        print("6. End journey")
        choice = input("Choose an action: ")
        if choice == '1':
            print()
            print(f"Name: {player.name}")
            print(f" Health: {player.health}")
            print(f" Food:   {player.food}")
            print(f" Money:  {player.money}")
        elif choice == '2':
            player.food = max(0, player.food - 10)
            player.health = min(100, player.health + 15)
            print("You hide in a quiet cave, stretch out on Japanese sleeping mats,")
            print("and sleep peacefully until morning.")
        elif choice == '3':
            visit_ramen_bar(player)
        elif choice == '4':
            visit_town(player)
        elif choice == '5':
            print("Market not implemented yet.")
        elif choice == '6':
            print("Ending journey and returning to main menu.")
            break
        else:
            print("Invalid selection, try again.")
        input("Press Enter to continue.")



def visit_ramen_bar(player):
    # ramen options with effects and cost
    prices = {
        '1': ('classic ramen', 15, {'food': 30, 'health': 0}),
        '2': ('snack tower', 25, {'food': 50, 'health': 0}),
        '3': ('rose mochi', 10, {'food': 10, 'health': 10}),
    }
    while True:
        print("\n--- JINYA Ramen Bar ---")
        print("1. Classic ramen (15 coins)")
        print("2. Snack tower (25 coins)")
        print("3. Rose mochi (10 coins)")
        print("4. Leave ramen bar")
        choice = input("Choose an item: ")
        if choice in prices:
            name, cost, effects = prices[choice]
            if player.money >= cost:
                player.money -= cost
                player.food += effects.get('food', 0)
                player.health = min(100, player.health + effects.get('health', 0))
                print(f"You buy {name} and enjoy it.")

                # special event for rose mochi
                if choice == '3':
                    print("Suddenly, Mitsuri appears and sits down beside you!")
                    print("She shares some of your rose mochi and smiles warmly.")
                    print("\"Your kindness and strength are inspiring,\""
                          " she says with a blush.")
                    # perhaps bonus health
                    player.health = min(100, player.health + 5)
            else:
                print("Not enough money.")
        elif choice == '4':
            print("Leaving ramen bar.")
            break
        else:
            print("Invalid option.")
        input("Press Enter to continue.")


def visit_town(player):
    towns = {
        '1': ('Osaka', 20),
        '2': ('Tokyo', 25),
        '3': ('Hiroshima', 15),
        '4': ('Kyoto', 10),
    }
    while True:
        print("\n--- Travel to a Town ---")
        for key, (town, cost) in towns.items():
            print(f"{key}. {town} ({cost} coins travel)")
        print("5. Return to journey menu")
        choice = input("Where would you like to go? ")
        if choice in towns:
            town, cost = towns[choice]
            if player.money >= cost:
                player.money -= cost
                print(f"You travel to {town} and explore its streets.")
                # simple effect: regain small amount of health
                player.health = min(100, player.health + 10)
                print("Visiting a town restores some health.")

                # special storyline for Osaka
                if town == 'Osaka':
                    osaka_encounter(player)
            else:
                print("You don't have enough money to travel there.")
        elif choice == '5':
            break
        else:
            print("Invalid option.")
        input("Press Enter to continue.")


def osaka_encounter(player):
    print("\nWhile walking through Osaka, you meet Tenzin.")
    print("He tells you one of his wives is fighting a Lower Moon 12 demon nearby.")
    while True:
        choice = input("Will you attack the demon with him? (yes/no): ")
        if choice.lower() in ('yes','y'):
            print("You join Tenzin and rush to the fight.")
            # enhanced combat description
            print("The Lower Moon 12 demon lunges at you, crushing your ribs with its massive claw!")
            print("Pain shoots through your body but you grit your teeth and keep fighting alongside Tenzin.")
            print("Together you charge and, with a synchronized special move, both of you slice clean through the demon's head.")
            print("The head falls, the demon collapses, and silence returns.")
            # consequences
            player.health = max(0, player.health - 40)  # heavier damage
            player.money += 20
            print("You lose a fair amount of health but earn 20 coins as reward.")
            break
        elif choice.lower() in ('no','n'):
            print("You decide not to get involved and walk away.")
            print("Tenzin glares at you, clearly angered by your refusal.")
            print("He mutters that he'll handle it himself and you feel the tension between you.")
            # temporary relationship penalty could be represented as lost money or health
            player.money = max(0, player.money - 10)
            print("You lose 10 coins in the fallout of his anger.")
            break
        else:
            print("Please answer yes or no.")

def load_journey():
    print("\nLoad feature not implemented yet.")
    input("Press Enter to return to menu.")


def show_help():
    print("\nWelcome to Demon Slayer Adventure!")
    print("This text-based game is inspired by the Oregon Trail style.")
    print("Navigate through choices and try to survive the journey.")
    input("Press Enter to return to menu.")


def main():
    while True:
        choice = main_menu()
        if choice == '1':
            start_new_journey()
        elif choice == '2':
            load_journey()
        elif choice == '3':
            show_help()
        elif choice == '4':
            print("Goodbye, demon slayer!")
            sys.exit()
        else:
            print("Invalid selection, please try again.")


if __name__ == '__main__':
    main()
