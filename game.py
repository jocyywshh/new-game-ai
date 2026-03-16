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
        self.level = 1
        self.sword_color = None

    def show_stats(self):
        print(f"\n{self.name} stats:")
        print(f" Level:  {self.level}")
        print(f" Health: {self.health}")
        print(f" Food:   {self.food}")
        print(f" Money:  {self.money}")
        if self.sword_color:
            print(f" Sword:  {self.sword_color}")


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
            player.show_stats()
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
            visit_market(player)
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


def visit_market(player):
    import random
    print("\n--- Market ---")
    print("At the market, you find Haganezuka.")
    print("You ask him if he could forge you a nichirin blade.")
    print("He is angry but does it anyways and charges 200 for it.")
    if player.money >= 200:
        player.money -= 200
        colors = ['black', 'red', 'light blue', 'pink']
        player.sword_color = random.choice(colors)
        print(f"When you grab the sword, it turns {player.sword_color}.")
        print("You now have a nichirin blade!")
    else:
        print("You don't have enough money for the nichirin blade.")
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
                # special storyline for Tokyo
                if town == 'Tokyo':
                    tokyo_encounter(player)
                # special storyline for Hiroshima
                if town == 'Hiroshima':
                    hiroshima_encounter(player)
                # special storyline for Kyoto
                if town == 'Kyoto':
                    kyoto_encounter(player)
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


def tokyo_encounter(player):
    print("\nYou wander Tokyo's beautiful streets late at night, lantern light reflecting off wet pavement.")
    print("Around a corner you bump into Tanjiro, Nezuko, Zenitsu, and Inosuke.")
    print("They're frantically searching—the bamboo muzzle that keeps Nezuko in check has gone missing!")
    # help search
    while True:
        help_choice = input("Will you help them look for the bamboo? (yes/no): ")
        if help_choice.lower() in ('yes','y'):
            print("You split up and scour the nearby alleys, peering under carts and behind barrels.")
            print("After a tense few minutes, you spot the bamboo piece wedged under a stack of crates.")
            print("Nezuko gasps with relief and hugs you briefly.")
            player.health = min(100, player.health + 10)
            print("Finding it restores 10 health because your heart feels lighter.")
            break
        elif help_choice.lower() in ('no','n'):
            print("You decline to get involved; the group continues their search without you.")
            break
        else:
            print("Please answer yes or no.")
    # demon alert
    print("Suddenly Tanjiro freezes and sniff the air.\n'There's a demon nearby,' he whispers.")
    while True:
        fight_choice = input("Do you join the demon slayers in battle? (yes/no): ")
        if fight_choice.lower() in ('yes','y'):
            print("You step forward as the demon lunges from the shadows!")
            print("Tanjiro unleashes a Water Breathing form while Zenitsu sparks to life and Inosuke charges berserk.")
            print("You fight alongside them, slicing and dodging until the demon crumbles to ashes.")
            player.health = max(0, player.health - 30)
            player.money += 25
            print("The fight takes its toll (-30 health) but you earn 25 coins and the gratitude of the slayers.")
            break
        elif fight_choice.lower() in ('no','n'):
            print("You decide discretion is the better part of valor and slip away into the night.")
            player.money = max(0, player.money - 15)
            print("In the chaos you lose 15 coins escaping the area.")
            break
        else:
            print("Please answer yes or no.")


def hiroshima_encounter(player):
    print("\nYou arrive at Hiroshima. The solemn ruins of the Atomic Bomb Dome stand quietly.")
    print("Nearby, a lunch box stand is in chaos. A booming voice cries, 'Tasty, Tasty!, Tasty!!'" )
    print("Rengoku has already devoured twenty lunch boxes and the vendors are frantic.")
    print("The manager yells, 'Please get this crazy man out of here!'")
    while True:
        escort = input("Will you escort Rengoku away? (yes/no): ")
        if escort.lower() in ('yes','y'):
            print("You gently guide the Flame Hashira out of the stall.")
            print("He laughs heartily, 'My apologies, the food was too good to resist!'")
            break
        elif escort.lower() in ('no','n'):
            print("You hesitate; the manager curses under his breath and the guards eventually haul Rengoku outside.")
            print("The scene fades and the opportunity passes.")
            return
        else:
            print("Please answer yes or no.") 
    print("\nAfterwards you ask Rengoku if he'd like to get mochi ice cream and sweet rice cakes.")
    print("He brightens and agrees; you wander together to a shop named 'YUMMIE$'.")
    print("Inside the cozy shop, you both savor cold mochi ice cream and sticky sweet rice cakes.")
    print("Rengoku sets down his cup and begins to speak, his voice warm and earnest:")
    print("\"A Hashira burns not because he hates demons, but because he loves people. Let your compassion be your flame.\"")
    print("\"Train until your muscles tremble and your spirit feels as though it might crack. That pain is the forge of strength.\"")
    print("\"Breathing is not just air; it's resolve flowing through your veins. Learn your style, let it flow like fire.\"")
    print("\"When fear tries to bind you, remember who you protect. Your friends, your family, the faces of those who believe in you.\"")
    print("He tells stories of standing on the precipice of defeat, of the glow of his blade when he held true to his convictions, and of the day he vowed to never let his flame die out.")
    print("The advice is vivid, detailed, and it settles into your mind as you nibble on rice cakes.")
    input("Press Enter to continue.")

    print("\nRengoku rises, patting the air with practiced motion. 'I must go. Duty calls.'")
    print("You follow him out and notice his expression harden -- he senses danger.")
    print("From mid‑air Azaka descends with a guttural shriek, claws aimed at Rengoku!")
    while True:
        action = input("Do you rush in to help him? (yes/no): ")
        if action.lower() in ('yes','y'):
            print("You draw your blade and dive forward, matching Rengoku's furious rhythm.")
            print("Steel flashes, fire meets shadow, and Azaka howls as you strike true.")
            print("The demon is cut down, disintegrating into sparks of dark energy.")
            player.level += 1
            player.health = min(100, player.health + 20)
            print("You feel a surge run through you – you have leveled up from a starter demon slayer!")
            print("(+20 health)")
            break
        elif action.lower() in ('no','n'):
            print("You hold back; Azaka's claw plunges into Rengoku's chest.")
            print("The Flame Hashira screams, then collapses. Darkness takes him.")
            print("Guilt and sorrow wash over you. The journey ends here.")
            player.health = 0
            sys.exit()
        else:
            print("Please answer yes or no.")




def kyoto_encounter(player):
    print("\nYou arrive in Kyoto and wander through hotels and food stands.")
    print("Eventually, you end up in a random cemetery. You get an eerie feeling and assume it's a haunted cemetery.")
    print("You don't realize there are multiple flowers as if you were in a garden...")
    print("You smell the strong scent of a demon near. It's Doma. He appears from behind you.")
    print("The cold mist brushes your face.")
    while True:
        choice = input("Do you run away or fight him? (run/fight): ")
        if choice.lower() in ('run', 'r'):
            print("You run away, but he chases after you and absorbs you.")
            print("Game over.")
            player.health = 0
            sys.exit()
        elif choice.lower() in ('fight', 'f'):
            print("You decide to fight him. You battle for an hour, you're exhausted.")
            print("You see an open spot and go for the kill. You kill him and after get promoted to a Hashira.")
            print("Ubuyashiki talks to you and he gives you inspiring words.")
            print("You won the game!")
            player.level = 10  # Max level or something
            player.health = 100
            print("Congratulations! You have completed the game.")
            sys.exit()
        else:
            print("Please choose run or fight.")


def load_journey():
    print("\nLoad feature not implemented yet.")
    input("Press Enter to return to menu.")


def show_help():
    print("\nWelcome to Demon Slayer Adventure!")
    print("This text-based game is inspired by the Oregon Trail style.")
    print("Navigate through choices and try to survive the journey.")
    print("Travel to Tokyo late at night and you might bump into Tanjiro & co—help them or fight a demon!")
    print("Visit Hiroshima to meet Rengoku in a lunch box stand and earn wisdom (and possibly a level up) if you help defeat Azaka!")
    print("Go to Hiroshima and you'll run into Rengoku causing a scene at a lunch box stand.")
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
