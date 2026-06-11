# Testing Data
import random
import math
import os
import time
from dotenv import load_dotenv
import heapq
import numpy as np
import statistics
from collections import deque
import sys
from pathlib import Path


def calculate_local_obstacle_ratio(map_file_path, block_size=10):
    try:
        with open(map_file_path, 'r') as f:
            lines = f.read().splitlines()
    except FileNotFoundError:
        print(f"Error: Could not find file at {map_file_path}")
        return None, None

    map_start = 0
    for i, line in enumerate(lines):
        if line.startswith('map'):
            map_start = i + 1
            break

    if map_start == 0 or map_start >= len(lines):
        print("Error: Invalid MovingAI map format.")
        return None, None

    grid = lines[map_start:]
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0

    obstacle_chars = {'@', 'O', 'T', 'W'}
    obstacle_ratios = []

    for y in range(0, height, block_size):
        for x in range(0, width, block_size):
            current_width = min(block_size, width - x)
            current_height = min(block_size, height - y)
            S = current_width * current_height

            obstacles_in_block = 0

            for by in range(current_height):
                for bx in range(current_width):
                    char = grid[y + by][x + bx]
                    if char in obstacle_chars:
                        obstacles_in_block += 1

            ratio = obstacles_in_block / S
            obstacle_ratios.append(ratio)

    if not obstacle_ratios:
        return 0.0, 0.0

    mean_obs = np.mean(obstacle_ratios)
    std_obs = np.std(obstacle_ratios)

    return mean_obs, std_obs

def process_local_obstacle_directory(directory_path, block_size=10):
    means, std_deviations = [], []
    processed_count = 0

    for filename in os.listdir(directory_path):
        if filename.endswith(".map"):
            file_path = os.path.join(directory_path, filename)
            mean, std = calculate_local_obstacle_ratio(file_path, block_size)

            if mean is not None and std is not None:
                means.append(mean)
                std_deviations.append(std)
                processed_count += 1

    if processed_count == 0:
        return 0.0, 0.0

    return np.mean(means), np.mean(std_deviations)



def calculate_local_agent_ratio(scen_file_path, block_size=10):
    try:
        with open(scen_file_path, 'r') as f:
            lines = f.read().splitlines()
    except FileNotFoundError:
        print(f"Error: Could not find file at {scen_file_path}")
        return None, None

    agent_lines = [line for line in lines if line.strip() and not line.startswith('version')]

    if not agent_lines:
        return 0.0, 0.0

    first_agent_data = agent_lines[0].split()
    map_width = int(first_agent_data[2])
    map_height = int(first_agent_data[3])

    agents_per_block = {}

    for line in agent_lines:
        data = line.split()
        start_x, start_y = int(data[4]), int(data[5])

        bx = start_x // block_size
        by = start_y // block_size

        agents_per_block[(bx, by)] = agents_per_block.get((bx, by), 0) + 1

    agent_ratios = []

    for y in range(0, map_height, block_size):
        for x in range(0, map_width, block_size):
            current_width = min(block_size, map_width - x)
            current_height = min(block_size, map_height - y)
            S = current_width * current_height

            bx = x // block_size
            by = y // block_size

            agents_in_block = agents_per_block.get((bx, by), 0)

            ratio = agents_in_block / S
            agent_ratios.append(ratio)

    if not agent_ratios:
        return 0.0, 0.0

    mean_agent = np.mean(agent_ratios)
    std_agent = np.std(agent_ratios)

    return mean_agent, std_agent

def process_local_agent_directory(directory_path, block_size=10):
    means, std_deviations = [], []
    processed_count = 0

    for filename in os.listdir(directory_path):
        if filename.endswith(".scen"):
            file_path = os.path.join(directory_path, filename)
            mean, std = calculate_local_agent_ratio(file_path, block_size)

            if mean is not None and std is not None:
                means.append(mean)
                std_deviations.append(std)
                processed_count += 1

    if processed_count == 0:
        return 0.0, 0.0

    return np.mean(means), np.mean(std_deviations)

def generate_uniform_scen(map_file, width, height, density, output_file):
    total_tiles = width * height
    # Calculate the exact number of agents based on density
    num_agents = int(total_tiles * density)

    print(f"Generating {num_agents} agents for {width}x{height} map (Density: {density})")

    # Generate a list of all valid coordinates
    all_coords = [(x, y) for x in range(width) for y in range(height)]

    starts = random.sample(all_coords, num_agents)
    goals = random.sample(all_coords, num_agents)

    with open(output_file, 'w') as f:
        f.write("version 1\n")

        for i in range(num_agents):
            sx, sy = starts[i]
            gx, gy = goals[i]

            manhattan = abs(sx - gx) + abs(sy - gy)

            f.write(f"0\t{map_file}\t{width}\t{height}\t{sx}\t{sy}\t{gx}\t{gy}\t{manhattan}\n")

    print(f"Saved to {output_file}")

def generate_heatmap_scen(map_file, width, height, base_density, num_hotspots, output_file):
    hotspots = []
    for _ in range(num_hotspots):
        hotspots.append((
            random.randint(0, width - 1),
            random.randint(0, height - 1),
            random.uniform(0.5, 1.0),   # Peak probability of this spot
            random.uniform(3.0, 8.0)    # How wide the hotspot spreads
        ))

    heatmap = []

    # 1. Build the heatmap probability field
    for y in range(height):
        row = []
        for x in range(width):
            prob = 0
            for hx, hy, intensity, spread in hotspots:
                dist_sq = (x - hx)**2 + (y - hy)**2
                prob += intensity * math.exp(-dist_sq / (2 * spread**2))

            final_prob = min(1.0, prob) * base_density
            row.append(final_prob)
        heatmap.append(row)

    chars = " .:-=+*#%@"
    print(f"--- Heatmap Visualization (Base Density: {base_density}) ---")
    for y in range(height):
        line = ""
        for x in range(width):
            val = heatmap[y][x]
            char_idx = int((val / base_density) * (len(chars) - 1)) if base_density > 0 else 0
            char_idx = max(0, min(len(chars) - 1, char_idx))
            line += chars[char_idx] + " "
        print(line)

    # 2. Generate strictly unique start points
    starts = []
    for y in range(height):
        for x in range(width):
            if random.random() < heatmap[y][x]:
                starts.append((x, y))

    num_agents = len(starts)
    print(f"\nAgents generated: {num_agents}")

    # 3. Generate goals that DO NOT overlap with starts
    # Convert all coordinates and starts to sets to easily find the difference
    all_coords_set = set((x, y) for x in range(width) for y in range(height))
    starts_set = set(starts)

    # The available coordinates for goals are all coordinates MINUS the start coordinates
    available_goal_coords = list(all_coords_set - starts_set)

    # Safety check: ensure the map is big enough to support this many unique goals
    if len(available_goal_coords) < num_agents:
        raise ValueError("Map is too small/dense! Not enough empty coordinates for goals.")

    # Sample goals from the safe list
    goals = random.sample(available_goal_coords, num_agents)

    # 4. Write to file
    with open(output_file, 'w') as f:
        f.write("version 1\n")
        for i in range(num_agents):
            sx, sy = starts[i]
            gx, gy = goals[i]

            manhattan = abs(sx - gx) + abs(sy - gy)

            f.write(f"0\t{map_file}\t{width}\t{height}\t{sx}\t{sy}\t{gx}\t{gy}\t{manhattan}\n")

    print(f"Saved to {output_file}")

def generate_uniform_scen(map_file, width, height, density, output_file):
    """
    Generates a .scen file with randomly distributed agents based on a flat density.
    """
    total_tiles = width * height
    # Calculate the exact number of agents based on density
    num_agents = int(total_tiles * density)

    print(f"Generating {num_agents} agents for {width}x{height} map (Density: {density})")

    # Generate a list of all valid coordinates
    all_coords = [(x, y) for x in range(width) for y in range(height)]

    # Randomly select unique starts and unique goals
    starts = random.sample(all_coords, num_agents)
    goals = random.sample(all_coords, num_agents)

    with open(output_file, 'w') as f:
        # Standard MAPF scene file header
        f.write("version 1\n")

        for i in range(num_agents):
            sx, sy = starts[i]
            gx, gy = goals[i]

            # Manhattan distance instead of A*
            manhattan = abs(sx - gx) + abs(sy - gy)

            # bucket map_file width height start_x start_y goal_x goal_y optimal_length
            f.write(f"0\t{map_file}\t{width}\t{height}\t{sx}\t{sy}\t{gx}\t{gy}\t{manhattan}\n")

    print(f"Saved to {output_file}")

def generate_heatmap_scen(map_file, width, height, base_density, num_hotspots, output_file):
    """
    Generates a .scen file by creating a probability heatmap for start locations,
    printing the map visually, and assigning entirely random goal locations.
    """
    # 1. Generate random hotspots: (x, y, intensity, spread)
    hotspots = []
    for _ in range(num_hotspots):
        hotspots.append((
            random.randint(0, width - 1),
            random.randint(0, height - 1),
            random.uniform(0.5, 1.0),   # Peak probability of this spot
            random.uniform(3.0, 8.0)    # How wide the hotspot spreads
        ))

    heatmap = []

    # 2. Build the heatmap probability field
    for y in range(height):
        row = []
        for x in range(width):
            prob = 0
            for hx, hy, intensity, spread in hotspots:
                dist_sq = (x - hx)**2 + (y - hy)**2
                # Gaussian-like decay from the hotspot center
                prob += intensity * math.exp(-dist_sq / (2 * spread**2))

            # Cap the max probability at 1.0, then scale by the requested overall density
            final_prob = min(1.0, prob) * base_density
            row.append(final_prob)
        heatmap.append(row)

    # 3. Print the heatmap to the console
    chars = " .:-=+*#%@"
    print(f"--- Heatmap Visualization (Base Density: {base_density}) ---")
    for y in range(height):
        line = ""
        for x in range(width):
            val = heatmap[y][x]
            # Map the probability to an ASCII character index
            char_idx = int((val / base_density) * (len(chars) - 1)) if base_density > 0 else 0
            char_idx = max(0, min(len(chars) - 1, char_idx))
            line += chars[char_idx] + " "
        print(line)

    # 4. Roll for agent start locations based on the heatmap
    starts = []
    for y in range(height):
        for x in range(width):
            if random.random() < heatmap[y][x]:
                starts.append((x, y))

    num_agents = len(starts)
    print(f"\nAgents generated: {num_agents}")

    # 5. Generate random goal locations (completely ignoring the heatmap)
    all_coords = [(x, y) for x in range(width) for y in range(height)]
    # Random sample ensures goals don't overlap, which is standard for MAPF
    goals = random.sample(all_coords, num_agents)

    # 6. Write to .scen file
    with open(output_file, 'w') as f:
        f.write("version 1\n")
        for i in range(num_agents):
            sx, sy = starts[i]
            gx, gy = goals[i]

            # Manhattan distance
            manhattan = abs(sx - gx) + abs(sy - gy)

            f.write(f"0\t{map_file}\t{width}\t{height}\t{sx}\t{sy}\t{gx}\t{gy}\t{manhattan}\n")

    print(f"Saved to {output_file}")
	def get_map_dimensions(map_path):

    width, height = 0, 0
    with open(map_path, 'r') as f:
        for line in f:
            if line.startswith("width"):
                width = int(line.split()[1])
            elif line.startswith("height"):
                height = int(line.split()[1])
            if width > 0 and height > 0:
                break
    return width, height

def batch_uniform_directory(input_dir, output_dir, density):
    """
    Finds all .map files in input_dir and generates a uniform .scen file in output_dir.
    """
    in_path = Path(input_dir)
    out_path = Path(output_dir)

    # Ensure the output directory exists
    out_path.mkdir(parents=True, exist_ok=True)

    map_files = list(in_path.glob("*.map"))

    if not map_files:
        print(f"No .map files found in '{input_dir}'.")
        return

    print(f"Found {len(map_files)} map(s). Generating Uniform scenarios in '{output_dir}'...")

    for map_file in map_files:
        width, height = get_map_dimensions(map_file)

        if width == 0 or height == 0:
            print(f"Skipping {map_file.name} - Could not parse valid dimensions.")
            continue

        # Route the output file to the user-defined output directory
        output_name = out_path / f"{map_file.stem}_uniform.scen"

        # Calls the generator from the first script
        generate_uniform_scen(str(map_file), width, height, density, str(output_name))

def batch_heatmap_directory(input_dir, output_dir, base_density, num_hotspots):
    """
    Finds all .map files in input_dir and generates a heatmap .scen file in output_dir.
    """
    in_path = Path(input_dir)
    out_path = Path(output_dir)

    # Ensure the output directory exists
    out_path.mkdir(parents=True, exist_ok=True)

    map_files = list(in_path.glob("*.map"))

    if not map_files:
        print(f"No .map files found in '{input_dir}'.")
        return

    print(f"\nFound {len(map_files)} map(s). Generating Heatmap scenarios in '{output_dir}'...")

    for map_file in map_files:
        width, height = get_map_dimensions(map_file)

        if width == 0 or height == 0:
            print(f"Skipping {map_file.name} - Could not parse valid dimensions.")
            continue

        # Route the output file to the user-defined output directory
        output_name = out_path / f"{map_file.stem}_heatmap.scen"

        # Calls the generator from the second script
        generate_heatmap_scen(str(map_file), width, height, base_density, num_hotspots, str(output_name))
