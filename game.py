from pet import Pet
from pet_map import create_map, display_map, place_pet, place_item, move_pet, place_exit
from emoji_map import emoji_dict
import random

def get_random_empty_positions(grid, avoid_positions, count):
    placeholder = emoji_dict["Floor"]
    rows, cols = len(grid), len(grid[0])
    all_positions = [
        (r, c)
        for r in range(rows) for c in range(cols)
        if (r, c) not in avoid_positions and grid[r][c] == placeholder
    ]
    if len(all_positions) < count:
        raise ValueError(f"only {len(all_positions)} empty cells but need {count}")
    return random.sample(all_positions, count)

def main():
    symbol = emoji_dict["Egg"]
    name = input("Enter your pet's name: ").strip()
    pet = Pet(name)

    rows, cols = 6, 8
    grid = create_map(rows, cols)
    pet_pos = (rows // 2, cols // 2)
    place_pet(grid, pet_pos, symbol)

    avoid = {pet_pos}
    food_pos, home_pos, toy_pos = get_random_empty_positions(grid, avoid, 3)
    place_item(grid, emoji_dict["Food"], food_pos)
    place_item(grid, emoji_dict["Home"], home_pos)
    place_item(grid, emoji_dict["Toy"], toy_pos)

    print(f"\n{pet.name} has entered its world!\n")
    display_map(grid)

    while pet.is_alive():
        pet.status()
        print("Commands: feed | play | sleep | w/a/s/d | status | quit(0)")
        cmd = input("Enter command: ").strip().lower()

        # 🥚 Egg stage control
        if pet.stage == "egg":
            if cmd == 'feed':
                pet.feed()

                # Check if ready to hatch
                if symbol == emoji_dict["Egg"] and pet.hunger >= 7:
                    symbol = emoji_dict["baby"]
                    grid[pet_pos[0]][pet_pos[1]] = symbol
                    pet.stage = "baby"
                    print(f"\n{pet.name} has hatched into a baby pet!")

                    # Generate one random region
                    region_keys = ["region_1", "region_2", "region_3", "region_4"]
                    chosen_key = random.choice(region_keys)
                    region_emoji = emoji_dict[chosen_key]

                    avoid = {pet_pos}
                    empty_positions = [
                        (r, c)
                        for r in range(rows) for c in range(cols)
                        if (r, c) not in avoid and grid[r][c] == emoji_dict["Floor"]
                    ]
                    if empty_positions:
                        region_pos = random.choice(empty_positions)
                        grid[region_pos[0]][region_pos[1]] = region_emoji
                        print(f"A new region has appeared at {region_pos}: {region_emoji}")

                # Display updated map after feeding
                print()
                display_map(grid)
                print()
                pet.tick()
                continue

            elif cmd in ('play', 'sleep', 'w', 'a', 's', 'd'):
                print(f"{pet.name} is still an egg. Try feeding it more.")
                continue
            elif cmd == '0':
                print("Goodbye!")
                break
            else:
                print("Error: unrecognised command")
                continue


        if cmd == 'feed':
            pet.feed()
        elif cmd == 'play':
            pet.play()
        elif cmd == 'sleep':
            pet.sleep()
        elif cmd in ('w', 'a', 's', 'd'):
            if symbol == emoji_dict["Egg"]:
                print(f"{pet.name} cannot move yet! Please feed it until it hatches.")
                continue

            drdc = {'w': (-1, 0), 's': (1, 0), 'a': (0, -1), 'd': (0, 1)}
            r, c = pet_pos
            dr, dc = drdc[cmd]
            nr, nc = r + dr, c + dc

            if 0 <= nr < rows and 0 <= nc < cols:
                target = grid[nr][nc]
                pet_pos = move_pet(grid, pet_pos, cmd, symbol)

                if target == emoji_dict["Food"]:
                    pet.feed_event()
                elif target == emoji_dict["Toy"]:
                    pet.play_event()
                elif target == emoji_dict["Home"]:
                    pet.home_event()
                elif target == emoji_dict["region_1"]:
                    symbol = emoji_dict["Eagle"]
                    grid[nr][nc] = symbol
                    print("The pet becomes an Eagle!")
                    pet.stage = "eagle"
                    place_exit(grid)
                elif target == emoji_dict["region_2"]:
                    symbol = emoji_dict["Dove"]
                    grid[nr][nc] = symbol
                    print("The pet becomes a Dove!")
                    pet.stage = "dove"
                    place_exit(grid)
                elif target == emoji_dict["region_3"]:
                    symbol = emoji_dict["flamingo"]
                    grid[nr][nc] = symbol
                    print("The pet becomes a Flamingo!")
                    pet.stage = "flamingo"
                    place_exit(grid)
                elif target == emoji_dict["region_4"]:
                    symbol = emoji_dict["peacock"]
                    grid[nr][nc] = symbol
                    print("The pet becomes a Peacock!")
                    pet.stage = "peacock"
                    place_exit(grid)
                elif target == emoji_dict["Exit"]:
                    print("Congratulations on getting off the map!")
                    break
            else:
                print("Error: cannot move out of bounds")

        elif cmd == 'status':
            pass
        elif cmd == '0':
            print("Goodbye!")
            break
        else:
            print("Error: unrecognised command")

        print()
        display_map(grid)
        print()
        pet.tick()

    if not pet.is_alive():
        print(f"Sadly, {pet.name} has passed away. Take better care next time!")

if __name__ == '__main__':
    main()
