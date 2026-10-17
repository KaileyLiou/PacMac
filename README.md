# PacMac

A Pac-Man style arcade game created with Python and Pygame for A.I. for Game Programming to practice vectors, physics, and simple game AI.

In this game, you wake up as a cat and have to collect all the sushi on the map before time runs out while avoiding four dogs. Some sushi give the cat special buffs, and portals on the map can teleport the cat to a new spot. The cat moves using acceleration, velocity, and drag. Each dog uses distance and a dot product to decide whether the cat is close enough and in front of it. When it sees the cat, it switches from patrolling to chasing.

## Features

- A cat that moves with acceleration, drag, and a maximum speed
- Four dogs that switch between patrol and chase using distance and a dot product field of view
- 20 sushi to collect, with tuna giving a speed boost and the first sushi roll giving temporary invincibility
- A special sushi roll that lets you shoot sushi at the dogs to freeze them
- Walls the cat and dogs can't pass through
- Portals that teleport the cat and move to new spots over time
- 9 lives, a 90 second timer, and an on-screen score and fish counter
- A start screen with instructions, plus win and game over screens

## How to Play

Use the arrow keys to move the cat. Click the X on the start screen to begin, and collect all the sushi before the timer runs out or you lose all 9 lives. After you pick up the special sushi roll, left click to shoot sushi toward the mouse. Press R on the win or game over screen to play again.

<img width="1340" height="891" alt="Screenshot 2026-10-17 at 10 51 46 AM" src="https://github.com/user-attachments/assets/0704153b-9ee1-44fb-8ae0-17057bb5ad83" />
<img width="1336" height="879" alt="Screenshot 2026-10-17 at 10 56 36 AM" src="https://github.com/user-attachments/assets/3f7d71fd-39f0-4303-93ac-2f2451f0e2f5" />
