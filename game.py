import json
import os
import sys
import time

SAVE_DIR = "saves"
SAVE_SLOTS = 3


def slow_print(text, delay=0.1):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()


def main_menu():
    slow_print("\n=== Demon Slayer Adventure ===")
    slow_print("1. Start New Journey")
    slow_print("2. Load Saved Journey")
    slow_print("3. Delete Save Slot")
    slow_print("4. Help")
    slow_print("5. Quit")
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
        slow_print(f"\n{self.name} stats:")
        slow_print(f" Level:  {self.level}")
        slow_print(f" Health: {self.health}")
        slow_print(f" Food:   {self.food}")
        slow_print(f" Money:  {self.money}")
        if self.sword_color:
            slow_print(f" Sword:  {self.sword_color}")
        if self.has_kimono:
            slow_print(" Kimono: New stylish kimono")
        if self.has_bird:
            slow_print(" Bird:   Cute companion bird")
        if self.has_weird_object:
            slow_print(" Object: Mysterious weird object")
        if self.has_tenzin_sword:
            slow_print(" Sword2: Tenzin's sword replica")
        if self.has_flower:
            slow_print(" Flower: Pretty flower")


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
        slow_print("Save cancelled.")
        return

    path = _save_file_path(slot)
    if os.path.exists(path):
        overwrite = input(f"Slot {slot} already has a save. Overwrite? (yes/no): ")
        if overwrite.lower() not in ("yes", "y"):
            slow_print("Save cancelled.")
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
        slow_print(f"Journey saved to slot {slot}.")
    except OSError:
        slow_print("Failed to save the journey.")


def journey_loop(player):
    # simple game loop to demonstrate stat tracking
    while True:
        slow_print("\n=== Journey Menu ===")
        slow_print("1. View stats")
        slow_print("2. Rest (lose food, regain health)")
        slow_print("3. Visit JINYA Ramen Bar")
        slow_print("4. Travel to a town")
        slow_print("5. Visit market (spend money to gain food or health)")
        slow_print("6. Save journey")
        slow_print("7. End journey")
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
            slow_print("Ending journey and returning to main menu.")
            break
        else:
            slow_print("Invalid selection, try again.")
        input("Press Enter to continue.")


def start_new_journey():
    slow_print("\nStarting a new journey through the Taisho era...")
    name = input("Enter your demon slayer's name: ")
    player = Character(name)
    journey_loop(player)


def rest(player):
    """Offer different places to rest and restore health."""
    while True:
        slow_print("\n--- Rest Options ---")
        slow_print("1. Sleep in a quiet cave")
        slow_print("2. Stay at a posh inn (cute receptionist)")
        slow_print("3. Visit a healing house")
        slow_print("4. Cancel")
        choice = input("Choose how you'd like to rest: ")

        if choice == '1':
            player.food = max(0, player.food - 10)
            player.health = min(100, player.health + 15)
            slow_print("You hide in a quiet cave, stretch out on Japanese sleeping mats,")
            slow_print("and sleep peacefully until morning.")
            break
        elif choice == '2':
            player.money += 10
            player.food = max(0, player.food - 5)
            player.health = min(100, player.health + 25)
            slow_print("A cute receptionist greets you with a smile and shows you to a cozy room.")
            slow_print("You sleep soundly on soft futons and wake refreshed.")
            slow_print("While resting, you find 10 coins tucked away in a drawer!")
            break
        elif choice == '3':
            # Healing houses offer food and healing without charging money
            player.food = min(100, player.food + 15)
            player.health = min(100, player.health + 35)
            slow_print("Healers in the house feed you restorative meals and mend your wounds.")
            slow_print("You leave feeling much stronger and well-nourished.")
            break
        elif choice == '4':
            slow_print("You decide not to rest right now.")
            break
        else:
            slow_print("Invalid option.")

    input("Press Enter to continue.")


def visit_ramen_bar(player):
    # ramen options with effects and cost
    prices = {
        '1': ('classic ramen', 15, {'food': 30, 'health': 0}),
        '2': ('snack tower', 25, {'food': 50, 'health': 0}),
        '3': ('rose mochi', 10, {'food': 10, 'health': 10}),
    }
    while True:
        slow_print("\n--- JINYA Ramen Bar ---")
        slow_print("1. Classic ramen (15 coins)")
        slow_print("2. Snack tower (25 coins)")
        slow_print("3. Rose mochi (10 coins)")
        slow_print("4. Leave ramen bar")
        choice = input("Choose an item: ")
        if choice in prices:
            name, cost, effects = prices[choice]
            if player.money >= cost:
                player.money -= cost
                player.food += effects.get('food', 0)
                player.health = min(100, player.health + effects.get('health', 0))
                slow_print(f"You buy {name} and enjoy it.")

                # special event for rose mochi
                if choice == '3':
                    slow_print("Suddenly, Mitsuri appears and sits down beside you!")
                    slow_print("She shares some of your rose mochi and smiles warmly.")
                    slow_print("\"Your kindness and strength are inspiring,\""
                          " she says with a blush.")
                    # perhaps bonus health
                    player.health = min(100, player.health + 5)
            else:
                slow_print("Not enough money.")
        elif choice == '4':
            slow_print("Leaving ramen bar.")
            break
        else:
            slow_print("Invalid option.")
        input("Press Enter to continue.")


def visit_market(player):
    import random
    while True:
        slow_print("\n--- Market ---")
        slow_print(f"You have {player.money} coins.")
        slow_print("What would you like to buy?")
        slow_print("1. Nichirin sword (200 coins) - Forged by Haganezuka")
        slow_print("2. New kimono (50 coins) - Stylish and protective")
        slow_print("3. Cute bird (30 coins) - A charming companion")
        slow_print("4. Weird object (40 coins) - Mysterious item that might help in battle")
        slow_print("5. Leave market")
        choice = input("Choose an item: ")

        if choice == '1':
            cost = 200
            slow_print(f"This costs {cost} coins. You have {player.money} coins.")
            if player.sword_color:
                slow_print("You already have a nichirin sword.")
            elif player.money >= cost:
                player.money -= cost
                colors = ['black', 'red', 'light blue', 'pink']
                player.sword_color = random.choice(colors)
                slow_print(f"Haganezuka forges you a nichirin blade. When you grab it, it turns {player.sword_color}.")
                slow_print("You now have a nichirin sword!")
            else:
                slow_print("You don't have enough money for the nichirin sword.")
        elif choice == '2':
            cost = 50
            slow_print(f"This costs {cost} coins. You have {player.money} coins.")
            if player.has_kimono:
                slow_print("You already have a new kimono.")
            elif player.money >= cost:
                player.money -= cost
                player.has_kimono = True
                slow_print("You buy a beautiful new kimono. It makes you feel more confident.")
            else:
                slow_print("You don't have enough money for the kimono.")
        elif choice == '3':
            cost = 30
            slow_print(f"This costs {cost} coins. You have {player.money} coins.")
            if player.has_bird:
                slow_print("You already have a cute bird.")
            elif player.money >= cost:
                player.money -= cost
                player.has_bird = True
                slow_print("You buy a cute bird. It chirps happily and perches on your shoulder.")
            else:
                slow_print("You don't have enough money for the bird.")
        elif choice == '4':
            cost = 40
            slow_print(f"This costs {cost} coins. You have {player.money} coins.")
            if player.has_weird_object:
                slow_print("You already have the weird object.")
            elif player.money >= cost:
                player.money -= cost
                player.has_weird_object = True
                slow_print("You buy a strange, glowing object. You're not sure what it does, but it feels powerful.")
            else:
                slow_print("You don't have enough money for the weird object.")
        elif choice == '5':
            slow_print("Leaving the market.")
            break
        else:
            slow_print("Invalid option.")
        input("Press Enter to continue.")


def visit_town(player):
    towns = {
        '1': ('Osaka', 20),
        '2': ('Tokyo', 25),
        '3': ('Hiroshima', 15),
        '4': ('Kyoto', 10),
    }
    while True:
        slow_print("\n--- Travel to a Town ---")
        for key, (town, cost) in towns.items():
            slow_print(f"{key}. {town} ({cost} coins travel)")
        slow_print("5. Return to journey menu")
        choice = input("Where would you like to go? ")
        if choice in towns:
            town, cost = towns[choice]
            if player.money >= cost:
                player.money -= cost
                slow_print(f"You travel to {town} and explore its streets.")
                # simple effect: regain small amount of health
                player.health = min(100, player.health + 10)
                slow_print("Visiting a town restores some health.")

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
                slow_print("You don't have enough money to travel there.")
        elif choice == '5':
            break
        else:
            slow_print("Invalid option.")
        input("Press Enter to continue.")


def osaka_encounter(player):
    slow_print("\nWhile walking through Osaka, you meet Tenzin.")
    slow_print("He tells you one of his wives is fighting a Lower Moon 12 demon nearby.")
    fought = False
    while True:
        choice = input("Will you attack the demon with him? (yes/no): ")
        if choice.lower() in ('yes','y'):
            fought = True
            slow_print("You join Tenzin and rush to the fight.")
            # enhanced combat description
            slow_print("The Lower Moon 12 demon lunges at you, crushing your ribs with its massive claw!")
            damage = 30 if player.has_weird_object else 40
            if player.has_tenzin_sword:
                damage -= 5
            bonus_money = 5 if player.has_weird_object else 0
            if player.has_weird_object:
                slow_print("Your weird object glows and helps mitigate the demon's powerful attacks!")
            slow_print("Pain shoots through your body but you grit your teeth and keep fighting alongside Tenzin.")
            slow_print("Together you charge and, with a synchronized special move, both of you slice clean through the demon's head.")
            slow_print("The head falls, the demon collapses, and silence returns.")
            # consequences
            player.health = max(0, player.health - damage)
            player.money += 20 + bonus_money
            slow_print(f"You lose a fair amount of health (-{damage}) but earn {20 + bonus_money} coins as reward.")
            break
        elif choice.lower() in ('no','n'):
            slow_print("You decide not to get involved and walk away.")
            slow_print("Tenzin glares at you, clearly angered by your refusal.")
            slow_print("He mutters that he'll handle it himself and you feel the tension between you.")
            # temporary relationship penalty could be represented as lost money or health
            player.money = max(0, player.money - 10)
            slow_print("You lose 10 coins in the fallout of his anger.")

            slow_print("\nAs you walk away, you run into a suspicious man.")
            slow_print("He looks at you weirdly and runs away.")
            slow_print("Curious, you follow him and realize he's just a bookkeeper, frantically organizing his ledgers.")
            while True:
                follow_choice = input("Move on? or continue to follow him? (move/continue): ")
                if follow_choice.lower() in ('move', 'm'):
                    slow_print("You decide to move on and leave the bookkeeper alone.")
                    break
                elif follow_choice.lower() in ('continue', 'c'):
                    slow_print("You continue following him. He notices and panics, dropping some coins in his haste.")
                    player.money += 15
                    slow_print("You pick up 15 coins he dropped.")
                    break
                else:
                    slow_print("Please choose move or continue.")
            break
        else:
            slow_print("Please answer yes or no.")

    if fought:
        slow_print("\nTenzin thanks you for your help in the fight.")
        slow_print("He asks you to come with him to wander around Osaka.")
        slow_print("As you explore the city together, you bond over stories of battles and bravery.")
        slow_print("Afterwards, you guys find another demon lurking in the shadows!")
        slow_print("Tenzin notices your skill and praises you: 'You fight with great strength and courage!'")
        slow_print("He gives you a replica of his sword. 'This will aid you in battle.'")
        player.has_tenzin_sword = True
        player.health = min(100, player.health + 10)  # improved health
        slow_print("The replica sword boosts your attack damage and improves your health (+10).")

        while True:
            continue_choice = input("Would you like to continue walking through Osaka? (yes/no): ")
            if continue_choice.lower() in ('yes', 'y'):
                slow_print("\nYou wander the beautiful streets of Osaka.")
                slow_print("Many ladies are staring at you, charmed by your presence.")
                slow_print("You talk to one of them, and she smiles warmly, giving you a pretty flower.")
                player.has_flower = True
                slow_print("You receive a pretty flower as a token of admiration.")
                break
            elif continue_choice.lower() in ('no', 'n'):
                slow_print("You decide not to continue walking.")
                break
            else:
                slow_print("Please answer yes or no.")

    input("Press Enter to continue.")


def tokyo_encounter(player):
    slow_print("\nYou wander Tokyo's beautiful streets late at night, lantern light reflecting off wet pavement.")
    slow_print("Around a corner you bump into Tanjiro, Nezuko, Zenitsu, and Inosuke.")
    slow_print("They're frantically searching—the bamboo muzzle that keeps Nezuko in check has gone missing!")
    # help search
    while True:
        help_choice = input("Will you help them look for the bamboo? (yes/no): ")
        if help_choice.lower() in ('yes','y'):
            slow_print("You split up and scour the nearby alleys, peering under carts and behind barrels.")
            slow_print("After a tense few minutes, you spot the bamboo piece wedged under a stack of crates.")
            slow_print("Nezuko gasps with relief and hugs you briefly.")
            player.health = min(100, player.health + 10)
            slow_print("Finding it restores 10 health because your heart feels lighter.")
            break
        elif help_choice.lower() in ('no','n'):
            slow_print("You decline to get involved; the group continues their search without you.")
            slow_print("\nSuddenly, you find yourself stuck in a huge hotel.")
            slow_print("You wonder what's going on and why it feels like you're going in a loop?")
            slow_print("After wandering the endless corridors, you find an EXIT.")
            while True:
                exit_choice = input("Do you decide to go through it? (yes/no): ")
                if exit_choice.lower() in ('yes','y'):
                    slow_print("You go through the exit and find yourself back on the streets.")
                    break
                elif exit_choice.lower() in ('no','n'):
                    slow_print("You decide not to go through. You wander more, feeling disoriented.")
                    player.food = max(0, player.food - 10)
                    slow_print("The confusion costs you 10 food.")
                    break
                else:
                    slow_print("Please answer yes or no.")
            break
        else:
            slow_print("Please answer yes or no.")
    # demon alert
    slow_print("Suddenly Tanjiro freezes and sniff the air.\n'There's a demon nearby,' he whispers.")
    while True:
        fight_choice = input("Do you join the demon slayers in battle? (yes/no): ")
        if fight_choice.lower() in ('yes','y'):
            slow_print("You step forward as the demon lunges from the shadows!")
            slow_print("Tanjiro unleashes a Water Breathing form while Zenitsu sparks to life and Inosuke charges berserk.")
            damage = 20 if player.has_weird_object else 30
            if player.has_tenzin_sword:
                damage -= 5
            bonus_money = 10 if player.has_weird_object else 0
            if player.has_weird_object:
                slow_print("Your weird object glows and helps deflect some of the demon's attacks!")
            slow_print("You fight alongside them, slicing and dodging until the demon crumbles to ashes.")
            player.health = max(0, player.health - damage)
            player.money += 25 + bonus_money
            slow_print(f"The fight takes its toll (-{damage} health) but you earn {25 + bonus_money} coins and the gratitude of the slayers.")
            break
        elif fight_choice.lower() in ('no','n'):
            slow_print("You decide discretion is the better part of valor and slip away into the night.")
            player.money = max(0, player.money - 15)
            slow_print("In the chaos you lose 15 coins escaping the area.")
            break
        else:
            slow_print("Please answer yes or no.")


def hiroshima_encounter(player):
    if player.has_tenzin_sword:
        slow_print("Having Tenzin's sword increases your speed!")
        slow_print("\nYou arrive at Hiroshima. The solemn ruins of the Atomic Bomb Dome stand quietly.")
        slow_print("Nearby, you meet Rengoku, the Flame Hashira.")
        slow_print("He suggests going to the ocean to relax and avoid any demons.")
        slow_print("You agree and head to the beautiful ocean shores.")
        slow_print("The waves crash gently, and the sun sets in a spectacular display.")
        slow_print("You have a really nice time, enjoying the peace and beauty.")
        slow_print("Rengoku talks to you about life: 'Life is like a flame, burning brightly and fiercely. It teaches us that every moment is precious, every battle a chance to protect what we cherish. I've seen the darkness of demons, but also the light in people's hearts. Remember, true strength comes from compassion, from fighting not just for survival, but for the smiles of those you love. Let your spirit burn with purpose, and you'll never falter.'")
        slow_print("His words are profound and inspiring, filling you with renewed determination.")
        slow_print("Afterward, you both enjoy some delicious food by the sea.")
        player.health = min(100, player.health + 30)
        player.money += 50
        player.level += 1
        slow_print("You gain 30 health, 50 coins, and level up!")
    else:
        slow_print("\nYou arrive at Hiroshima. The solemn ruins of the Atomic Bomb Dome stand quietly.")
        slow_print("Nearby, a lunch box stand is in chaos. A booming voice cries, 'Tasty, Tasty!, Tasty!!'" )
        slow_print("Rengoku has already devoured twenty lunch boxes and the vendors are frantic.")
        slow_print("The manager yells, 'Please get this crazy man out of here!'")
        while True:
            escort = input("Will you escort Rengoku away? (yes/no): ")
            if escort.lower() in ('yes','y'):
                slow_print("You gently guide the Flame Hashira out of the stall.")
                slow_print("He laughs heartily, 'My apologies, the food was too good to resist!'")
                break
            elif escort.lower() in ('no','n'):
                slow_print("You hesitate; the manager curses under his breath and the guards eventually haul Rengoku outside.")
                slow_print("The scene fades and the opportunity passes.")
                return
            else:
                slow_print("Please answer yes or no.") 
        slow_print("\nAfterwards you ask Rengoku if he'd like to get mochi ice cream and sweet rice cakes.")
        slow_print("He brightens and agrees; you wander together to a shop named 'YUMMIE$'.")
        slow_print("Inside the cozy shop, you both savor cold mochi ice cream and sticky sweet rice cakes.")
        slow_print("Rengoku sets down his cup and begins to speak, his voice warm and earnest:")
        slow_print("\"A Hashira burns not because he hates demons, but because he loves people. Let your compassion be your flame.\"")
        slow_print("\"Train until your muscles tremble and your spirit feels as though it might crack. That pain is the forge of strength.\"")
        slow_print("\"Breathing is not just air; it's resolve flowing through your veins. Learn your style, let it flow like fire.\"")
        slow_print("\"When fear tries to bind you, remember who you protect. Your friends, your family, the faces of those who believe in you.\"")
        slow_print("He tells stories of standing on the precipice of defeat, of the glow of his blade when he held true to his convictions, and of the day he vowed to never let his flame die out.")
        slow_print("The advice is vivid, detailed, and it settles into your mind as you nibble on rice cakes.")
        input("Press Enter to continue.")

        slow_print("\nRengoku rises, patting the air with practiced motion. 'I must go. Duty calls.'")
        slow_print("You follow him out and notice his expression harden -- he senses danger.")
        slow_print("From mid‑air Azaka descends with a guttural shriek, claws aimed at Rengoku!")
        while True:
            action = input("Do you rush in to help him? (yes/no): ")
            if action.lower() in ('yes','y'):
                slow_print("You draw your blade and dive forward, matching Rengoku's furious rhythm.")
                slow_print("Steel flashes, fire meets shadow, and Azaka howls as you strike true.")
                slow_print("The demon is cut down, disintegrating into sparks of dark energy.")
                player.level += 1
                player.health = min(100, player.health + 20)
                slow_print("You feel a surge run through you – you have leveled up from a starter demon slayer!")
                slow_print("(+20 health)")
                break
            elif action.lower() in ('no','n'):
                slow_print("You hold back; Azaka's claw plunges into Rengoku's chest.")
                slow_print("The Flame Hashira screams, then collapses. Darkness takes him.")
                slow_print("Guilt and sorrow wash over you. The journey ends here.")
                player.health = 0
                sys.exit()
            else:
                slow_print("Please answer yes or no.")




def kyoto_encounter(player):
    slow_print("\nYou arrive in Kyoto and wander through hotels and food stands.")
    slow_print("Eventually, you end up in a random cemetery. You get an eerie feeling and assume it's a haunted cemetery.")
    slow_print("You don't realize there are multiple flowers as if you were in a garden...")
    slow_print("You smell the strong scent of a demon near. It's Doma. He appears from behind you.")
    slow_print("The cold mist brushes your face.")
    while True:
        choice = input("Do you run away or fight him? (run/fight): ")
        if choice.lower() in ('run', 'r'):
            slow_print("You run away, but he chases after you and absorbs you.")
            slow_print("Game over.")
            player.health = 0
            sys.exit()
        elif choice.lower() in ('fight', 'f'):
            slow_print("You decide to fight him. You battle for an hour, you're exhausted.")
            slow_print("You see an open spot and go for the kill. You kill him and after get promoted to a Hashira.")
            slow_print("Ubuyashiki talks to you and he gives you inspiring words.")
            slow_print("You won the game!")
            player.level = 10  # Max level or something
            player.health = 100
            slow_print("Congratulations! You have completed the game.")
            sys.exit()
        else:
            slow_print("Please choose run or fight.")


def delete_save_slot():
    """Delete a save slot file."""
    if not os.path.isdir(SAVE_DIR):
        slow_print("\nNo saved journey found.")
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
            slow_print(f"Slot {slot} deleted.")
        except OSError:
            slow_print("Failed to delete the save slot.")
    else:
        slow_print("Delete cancelled.")

    input("Press Enter to return to menu.")


def load_journey():
    """Load a previously saved journey from disk."""
    if not os.path.isdir(SAVE_DIR):
        slow_print("\nNo saved journey found.")
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
        slow_print("\nFailed to load saved journey.")
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

    slow_print(f"\nLoaded journey for {player.name}.")
    player.show_stats()

    cont = input("Continue this journey now? (yes/no): ")
    if cont.lower() in ("yes", "y"):
        journey_loop(player)
    else:
        slow_print("Returning to main menu.")
        input("Press Enter to continue.")


def show_help():
    slow_print("\nWelcome to Demon Slayer Adventure!")
    slow_print("This text-based game is inspired by the Oregon Trail style.")
    slow_print("Navigate through choices and try to survive the journey.")
    slow_print("Travel to Tokyo late at night and you might bump into Tanjiro & co—help them or fight a demon!")
    slow_print("Visit Hiroshima to meet Rengoku in a lunch box stand and earn wisdom (and possibly a level up) if you help defeat Azaka!")
    slow_print("Go to Hiroshima and you'll run into Rengoku causing a scene at a lunch box stand.")
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
            slow_print("Goodbye, demon slayer!")
            sys.exit()
        else:
            slow_print("Invalid selection, please try again.")


if __name__ == '__main__':
    main()
