import json
import os
import sys

SAVE_DIR = "saves"
SAVE_SLOTS = 3


def main_menu():
    print("\n=== Demon Slayer Adventure ===")
    print("1. Start New Journey")
    print("2. Load Saved Journey")
    print("3. Delete Save Slot")
    print("4. Help")
    print("5. Quit")
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
        self.has_kimono = False
        self.has_bird = False
        self.has_weird_object = False
        self.has_tenzin_sword = False
        self.has_flower = False

    def show_stats(self):
        print(f"\n{self.name} stats:")
        print(f" Level:  {self.level}")
        print(f" Health: {self.health}")
        print(f" Food:   {self.food}")
        print(f" Money:  {self.money}")
        if self.sword_color:
            print(f" Sword:  {self.sword_color}")
        if self.has_kimono:
            print(" Kimono: New stylish kimono")
        if self.has_bird:
            print(" Bird:   Cute companion bird")
        if self.has_weird_object:
            print(" Object: Mysterious weird object")
        if self.has_tenzin_sword:
            print(" Sword2: Tenzin's sword replica")
        if self.has_flower:
            print(" Flower: Pretty flower")


def _ensure_save_dir():
    os.makedirs(SAVE_DIR, exist_ok=True)


def _save_file_path(slot: int) -> str:
    return os.path.join(SAVE_DIR, f"save_{slot}.json")


def _list_save_slots():
    slots = {}
    for i in range(1, SAVE_SLOTS + 1):
        slots[i] = os.path.exists(_save_file_path(i))
    return slots


def _choose_save_slot(prompt: str, require_existing: bool = False):
    while True:
        slots = _list_save_slots()
        print("\nSave slots:")
        for i, exists in slots.items():
            status = "occupied" if exists else "empty"
            print(f" {i}. Slot {i} ({status})")

        choice = input(f"{prompt} (1-{SAVE_SLOTS}, or q to cancel): ")
        if choice.lower() in ("q", "quit", "exit"):
            return None

        if not choice.isdigit():
            print("Please enter a number.")
            continue
        slot = int(choice)
        if slot < 1 or slot > SAVE_SLOTS:
            print(f"Please pick a slot between 1 and {SAVE_SLOTS}.")
            continue
        if require_existing and not slots[slot]:
            print("That slot is empty. Choose another.")
            continue
        return slot


def save_journey(player):
    """Save the current journey state to disk."""
    _ensure_save_dir()
    slot = _choose_save_slot("Choose a slot to save to", require_existing=False)
    if slot is None:
        print("Save cancelled.")
        return

    path = _save_file_path(slot)
    if os.path.exists(path):
        overwrite = input(f"Slot {slot} already has a save. Overwrite? (yes/no): ")
        if overwrite.lower() not in ("yes", "y"):
            print("Save cancelled.")
            return

    data = {
        "name": player.name,
        "health": player.health,
        "food": player.food,
        "money": player.money,
        "level": player.level,
        "sword_color": player.sword_color,
        "has_kimono": player.has_kimono,
        "has_bird": player.has_bird,
        "has_weird_object": player.has_weird_object,
        "has_tenzin_sword": player.has_tenzin_sword,
        "has_flower": player.has_flower,
    }

    try:
        with open(path, "w") as f:
            json.dump(data, f)
        print(f"Journey saved to slot {slot}.")
    except OSError:
        print("Failed to save the journey.")


def journey_loop(player):
    # simple game loop to demonstrate stat tracking
    while True:
        print("\n=== Journey Menu ===")
        print("1. View stats")
        print("2. Rest (lose food, regain health)")
        print("3. Visit JINYA Ramen Bar")
        print("4. Travel to a town")
        print("5. Visit market (spend money to gain food or health)")
        print("6. Save journey")
        print("7. End journey")
        choice = input("Choose an action: ")
        if choice == '1':
            player.show_stats()
        elif choice == '2':
            rest(player)
        elif choice == '3':
            visit_ramen_bar(player)
        elif choice == '4':
            visit_town(player)
        elif choice == '5':
            visit_market(player)
        elif choice == '6':
            save_journey(player)
        elif choice == '7':
            save_choice = input("Save your journey before returning to the main menu? (yes/no): ")
            if save_choice.lower() in ('yes', 'y'):
                save_journey(player)
            print("Ending journey and returning to main menu.")
            break
        else:
            print("Invalid selection, try again.")
        input("Press Enter to continue.")


def start_new_journey():
    print("\nStarting a new journey through the Taisho era...")
    name = input("Enter your demon slayer's name: ")
    player = Character(name)
    journey_loop(player)


def rest(player):
    """Offer different places to rest and restore health."""
    while True:
        print("\n--- Rest Options ---")
        print("1. Sleep in a quiet cave")
        print("2. Stay at a posh inn (cute receptionist)")
        print("3. Visit a healing house")
        print("4. Cancel")
        choice = input("Choose how you'd like to rest: ")

        if choice == '1':
            player.food = max(0, player.food - 10)
            player.health = min(100, player.health + 15)
            print("You hide in a quiet cave, stretch out on Japanese sleeping mats,")
            print("and sleep peacefully until morning.")
            break
        elif choice == '2':
            player.money += 10
            player.food = max(0, player.food - 5)
            player.health = min(100, player.health + 25)
            print("A cute receptionist greets you with a smile and shows you to a cozy room.")
            print("You sleep soundly on soft futons and wake refreshed.")
            print("While resting, you find 10 coins tucked away in a drawer!")
            break
        elif choice == '3':
            # Healing houses offer food and healing without charging money
            player.food = min(100, player.food + 15)
            player.health = min(100, player.health + 35)
            print("Healers in the house feed you restorative meals and mend your wounds.")
            print("You leave feeling much stronger and well-nourished.")
            break
        elif choice == '4':
            print("You decide not to rest right now.")
            break
        else:
            print("Invalid option.")

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
    while True:
        print("\n--- Market ---")
        print("What would you like to buy?")
        print("1. Nichirin sword (200 coins) - Forged by Haganezuka")
        print("2. New kimono (50 coins) - Stylish and protective")
        print("3. Cute bird (30 coins) - A charming companion")
        print("4. Weird object (40 coins) - Mysterious item that might help in battle")
        print("5. Leave market")
        choice = input("Choose an item: ")

        if choice == '1':
            if player.sword_color:
                print("You already have a nichirin sword.")
            elif player.money >= 200:
                player.money -= 200
                colors = ['black', 'red', 'light blue', 'pink']
                player.sword_color = random.choice(colors)
                print(f"Haganezuka forges you a nichirin blade. When you grab it, it turns {player.sword_color}.")
                print("You now have a nichirin sword!")
            else:
                print("You don't have enough money for the nichirin sword.")
        elif choice == '2':
            if player.has_kimono:
                print("You already have a new kimono.")
            elif player.money >= 50:
                player.money -= 50
                player.has_kimono = True
                print("You buy a beautiful new kimono. It makes you feel more confident.")
            else:
                print("You don't have enough money for the kimono.")
        elif choice == '3':
            if player.has_bird:
                print("You already have a cute bird.")
            elif player.money >= 30:
                player.money -= 30
                player.has_bird = True
                print("You buy a cute bird. It chirps happily and perches on your shoulder.")
            else:
                print("You don't have enough money for the bird.")
        elif choice == '4':
            if player.has_weird_object:
                print("You already have the weird object.")
            elif player.money >= 40:
                player.money -= 40
                player.has_weird_object = True
                print("You buy a strange, glowing object. You're not sure what it does, but it feels powerful.")
            else:
                print("You don't have enough money for the weird object.")
        elif choice == '5':
            print("Leaving the market.")
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
    fought = False
    while True:
        choice = input("Will you attack the demon with him? (yes/no): ")
        if choice.lower() in ('yes','y'):
            fought = True
            print("You join Tenzin and rush to the fight.")
            # enhanced combat description
            print("The Lower Moon 12 demon lunges at you, crushing your ribs with its massive claw!")
            damage = 30 if player.has_weird_object else 40
            if player.has_tenzin_sword:
                damage -= 5
            bonus_money = 5 if player.has_weird_object else 0
            if player.has_weird_object:
                print("Your weird object glows and helps mitigate the demon's powerful attacks!")
            print("Pain shoots through your body but you grit your teeth and keep fighting alongside Tenzin.")
            print("Together you charge and, with a synchronized special move, both of you slice clean through the demon's head.")
            print("The head falls, the demon collapses, and silence returns.")
            # consequences
            player.health = max(0, player.health - damage)
            player.money += 20 + bonus_money
            print(f"You lose a fair amount of health (-{damage}) but earn {20 + bonus_money} coins as reward.")
            break
        elif choice.lower() in ('no','n'):
            print("You decide not to get involved and walk away.")
            print("Tenzin glares at you, clearly angered by your refusal.")
            print("He mutters that he'll handle it himself and you feel the tension between you.")
            # temporary relationship penalty could be represented as lost money or health
            player.money = max(0, player.money - 10)
            print("You lose 10 coins in the fallout of his anger.")

            print("\nAs you walk away, you run into a suspicious man.")
            print("He looks at you weirdly and runs away.")
            print("Curious, you follow him and realize he's just a bookkeeper, frantically organizing his ledgers.")
            while True:
                follow_choice = input("Move on? or continue to follow him? (move/continue): ")
                if follow_choice.lower() in ('move', 'm'):
                    print("You decide to move on and leave the bookkeeper alone.")
                    break
                elif follow_choice.lower() in ('continue', 'c'):
                    print("You continue following him. He notices and panics, dropping some coins in his haste.")
                    player.money += 15
                    print("You pick up 15 coins he dropped.")
                    break
                else:
                    print("Please choose move or continue.")
            break
        else:
            print("Please answer yes or no.")

    if fought:
        print("\nTenzin thanks you for your help in the fight.")
        print("He asks you to come with him to wander around Osaka.")
        print("As you explore the city together, you bond over stories of battles and bravery.")
        print("Afterwards, you guys find another demon lurking in the shadows!")
        print("Tenzin notices your skill and praises you: 'You fight with great strength and courage!'")
        print("He gives you a replica of his sword. 'This will aid you in battle.'")
        player.has_tenzin_sword = True
        player.health = min(100, player.health + 10)  # improved health
        print("The replica sword boosts your attack damage and improves your health (+10).")

        print("\nYou wander the beautiful streets of Osaka.")
        print("Many ladies are staring at you, charmed by your presence.")
        print("You talk to one of them, and she smiles warmly, giving you a pretty flower.")
        player.has_flower = True
        print("You receive a pretty flower as a token of admiration.")

    input("Press Enter to continue.")


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
            print("\nSuddenly, you find yourself stuck in a huge hotel.")
            print("You wonder what's going on and why it feels like you're going in a loop?")
            print("After wandering the endless corridors, you find an EXIT.")
            while True:
                exit_choice = input("Do you decide to go through it? (yes/no): ")
                if exit_choice.lower() in ('yes','y'):
                    print("You go through the exit and find yourself back on the streets.")
                    break
                elif exit_choice.lower() in ('no','n'):
                    print("You decide not to go through. You wander more, feeling disoriented.")
                    player.food = max(0, player.food - 10)
                    print("The confusion costs you 10 food.")
                    break
                else:
                    print("Please answer yes or no.")
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
            damage = 20 if player.has_weird_object else 30
            if player.has_tenzin_sword:
                damage -= 5
            bonus_money = 10 if player.has_weird_object else 0
            if player.has_weird_object:
                print("Your weird object glows and helps deflect some of the demon's attacks!")
            print("You fight alongside them, slicing and dodging until the demon crumbles to ashes.")
            player.health = max(0, player.health - damage)
            player.money += 25 + bonus_money
            print(f"The fight takes its toll (-{damage} health) but you earn {25 + bonus_money} coins and the gratitude of the slayers.")
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


def delete_save_slot():
    """Delete a save slot file."""
    if not os.path.isdir(SAVE_DIR):
        print("\nNo saved journey found.")
        input("Press Enter to return to menu.")
        return

    slot = _choose_save_slot("Choose a slot to delete", require_existing=True)
    if slot is None:
        return

    path = _save_file_path(slot)
    confirm = input(f"Are you sure you want to delete slot {slot}? (yes/no): ")
    if confirm.lower() in ("yes", "y"):
        try:
            os.remove(path)
            print(f"Slot {slot} deleted.")
        except OSError:
            print("Failed to delete the save slot.")
    else:
        print("Delete cancelled.")

    input("Press Enter to return to menu.")


def load_journey():
    """Load a previously saved journey from disk."""
    if not os.path.isdir(SAVE_DIR):
        print("\nNo saved journey found.")
        input("Press Enter to return to menu.")
        return

    slot = _choose_save_slot("Choose a slot to load", require_existing=True)
    if slot is None:
        return

    path = _save_file_path(slot)
    try:
        with open(path, "r") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError):
        print("\nFailed to load saved journey.")
        input("Press Enter to return to menu.")
        return

    player = Character(data.get("name", "Unknown"))
    player.health = data.get("health", 100)
    player.food = data.get("food", 100)
    player.money = data.get("money", 50)
    player.level = data.get("level", 1)
    player.sword_color = data.get("sword_color")
    player.has_kimono = data.get("has_kimono", False)
    player.has_bird = data.get("has_bird", False)
    player.has_weird_object = data.get("has_weird_object", False)
    player.has_tenzin_sword = data.get("has_tenzin_sword", False)
    player.has_flower = data.get("has_flower", False)

    print(f"\nLoaded journey for {player.name}.")
    player.show_stats()

    cont = input("Continue this journey now? (yes/no): ")
    if cont.lower() in ("yes", "y"):
        journey_loop(player)
    else:
        print("Returning to main menu.")
        input("Press Enter to continue.")


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
            delete_save_slot()
        elif choice == '4':
            show_help()
        elif choice == '5':
            print("Goodbye, demon slayer!")
            sys.exit()
        else:
            print("Invalid selection, please try again.")


if __name__ == '__main__':
    main()
