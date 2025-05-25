def get_maze_template():
    # Return the fixed 20x20 map layout as a 2D list
    layout = [
        "P⬜⬜⬜⬜⬜🧱⬜⬜🧱⬜⬜⬜⬜🧱⬜⬜⬜⬜⬜",
        "🧱🧱🧱⬜🧱⬜🧱🧱🧱⬜🧱⬜🧱🧱🧱⬜🧱⬜🧱⬜",
        "⬜🧱⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🧱⬜⬜🧱⬜",
        "⬜🧱🧱🧱🧱🧱⬜🧱🧱🧱⬜🧱⬜🧱🧱🧱⬜🧱⬜🧱",
        "⬜⬜⬜⬜⬜⬜🩹⬜🧱⬜⬜🧱⬜⬜⬜⬜⬜⬜⬜🧱",
        "🧱🧱🧱⬜🧱🧱🧱⬜🧱🧱🧱🧱🧱⬜🧱🧱🧱⬜🧱⬜",
        "⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🧱⬜⬜⬜⬜⬜⬜⬜⬜",
        "⬜🧱🧱🧱⬜🧱🧱🧱🧱⬜🧱🧱🧱🧱🧱⬜🧱⬜🧱⬜",
        "⬜⬜⬜⬜⬜⬜⬜⬜⬜🩹⬜⬜⬜⬜⬜⬜⬜⬜🧱⬜",
        "⬜🧱🧱⬜🧱🧱🧱⬜🧱🧱🧱🧱🧱⬜🧱🩹🧱🧱🧱⬜",
        "⬜🧱⬜⬜🧱⬜⬜⬜⬜🧱⬜⬜🧱⬜⬜⬜⬜⬜🧱⬜",
        "⬜🧱⬜🧱🧱🧱🧱🧱⬜🧱⬜🧱🧱⬜🧱🧱⬜⬜🧱⬜",
        "⬜🧱⬜⬜⬜🧱🧱⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🧱⬜",
        "⬜🧱🧱🧱⬜⬜⬜🧱🧱🧱⬜🧱🧱🧱⬜🧱🧱⬜🧱🧱",
        "⬜⬜⬜⬜⬜🧱⬜🧱⬜⬜⬜⬜⬜🧱⬜⬜⬜⬜⬜⬜",
        "🧱🧱🧱⬜⬜🧱🧱🧱🧱🧱⬜🧱🧱🧱🧱⬜🧱🧱🧱⬜",
        "⬜⬜⬜🧱⬜⬜⬜⬜⬜⬜⬜🧱⬜⬜⬜⬜⬜⬜⬜⬜",
        "⬜🧱🧱🧱🧱🧱🧱🧱⬜🧱🧱🧱🧱🧱⬜🧱🧱🧱🧱⬜",
        "⬜⬜⬜⬜🩹⬜⬜⬜⬜⬜⬜⬜⬜⬜🩹⬜⬜⬜⬜🚪",
        "🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱"
    ]
    return [list(row) for row in layout]

# Initialize the game
# Locate player position marked by 'P'
grid = get_maze_template()
player_pos = next(((x, y) for y in range(20) for x in range(20) if grid[y][x] == 'P'), None)
if player_pos is None:
    raise ValueError("Player 'P' not found!")

# Set initial zombie positions and their cooldowns after attacking
zombie_states = {(0,10): 0, (19,12): 0}
medkits = 5
hp = 3
round_num = 1

# Display the current map and status
def display():
    print(f"\nRound {round_num} | HP: {hp} | 🩹: {medkits}")
    print("=" * 63)
    for y, row in enumerate(grid):
        print("|" + "|".join(
            "🚶" if (x, y) == player_pos else
            "🧟" if (x, y) in zombie_states else
            ch for x, ch in enumerate(row)
        ) + "|")
    print("=" * 63)

# Move all zombies toward the player each round
def move_zombies():
    global zombie_states
    px, py = player_pos
    new_states = {}
    for (zx, zy), cd in zombie_states.items():
        if cd > 0:
            new_states[(zx, zy)] = cd - 1
            continue
        moved = False
        for dx, dy in sorted([(0,-1),(0,1),(-1,0),(1,0)], key=lambda d: abs(zx + d[0] - px) + abs(zy + d[1] - py)):
            nx, ny = zx + dx, zy + dy
            if 0 <= nx < 20 and 0 <= ny < 20 and grid[ny][nx] not in ['🧱', '🚪']:
                if (nx, ny) == player_pos:
                    print("☠️  A zombie bit you!")
                    new_states[(zx, zy)] = 2  # zombie rests 2 rounds
                else:
                    new_states[(nx, ny)] = 0
                moved = True
                break
        if not moved:
            new_states[(zx, zy)] = 0
    zombie_states.clear()
    zombie_states.update(new_states)

# Main game loop
def play_game():
    global player_pos, hp, medkits, round_num
    while True:
        grid[player_pos[1]][player_pos[0]] = '⬜'
        display()
        cmd = input("Move (n/s/e/w) or use 🩹: ").strip().lower()

        if cmd == 'use':
            if medkits > 0 and hp < 3:
                medkits -= 1
                hp += 1
                print("🩹 Used a medkit. HP +1")
            elif hp == 3:
                print("🩺 You're already at full HP.")
            else:
                print("❌ No medkits left.")
            continue

        dx, dy = {"n":(0,-1), "s":(0,1), "e":(1,0), "w":(-1,0)}.get(cmd, (0,0))
        nx, ny = player_pos[0] + dx, player_pos[1] + dy
        if not (0 <= nx < 20 and 0 <= ny < 20):
            print("❌ Out of bounds.")
            continue
        if grid[ny][nx] == '🧱':
            print("🧱 Wall blocks the way.")
            continue
        if (nx, ny) in zombie_states:
            hp -= 1
            print("☠️  You ran into a zombie! HP -1")
            if hp <= 0:
                print("💀 You died! Game over.")
                break
        elif grid[ny][nx] == '🩹':
            medkits += 1
            print("🩹 Picked up a medkit!")
        elif grid[ny][nx] == '🚪':
            print("🏆 You escaped! You win!")
            break

        player_pos = (nx, ny)
        move_zombies()
        for (zx, zy) in zombie_states:
            if (zx, zy) == player_pos:
                hp -= 1
                print("☠️  A zombie attacked you! HP -1")
                if hp <= 0:
                    print("💀 You died! Game Over.")
                    break
        round_num += 1

# Start the game
if __name__ == "__main__":
    play_game()