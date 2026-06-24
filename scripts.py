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
import glob


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

def parse_movingai_map(filepath):
    """
    Helper function to read a standard MovingAI .map file.
    Returns the width, height, and the 2D grid of the map.
    """
    with open(filepath, 'r') as f:
        lines = f.read().splitlines()
    
    height = int(lines[1].split()[1])
    width = int(lines[2].split()[1])
    
    # The actual map grid starts at line 4 (index 4)
    map_grid = lines[4:4+height]
    return width, height, map_grid


# --- FUNCTION 1: The Core Scene Generator ---
def generate_heatmap_scen(map_filepath, output_file, base_density=0.05, num_hotspots=3):
    """
    Generates a .scen file for a specific map using heatmap starts and random walk goals.
    """
    width, height, map_grid = parse_movingai_map(map_filepath)
    passable_chars = {'.', 'G', 'S'}
    
    # 1. Generate random hotspots
    hotspots = []
    for _ in range(num_hotspots):
        hotspots.append((
            random.randint(0, width - 1),
            random.randint(0, height - 1),
            random.uniform(0.5, 1.0),
            random.uniform(3.0, 8.0)
        ))

    # 2. Build the heatmap probability field
    heatmap = []
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

    # 3. Roll for agent start locations
    starts = []
    for y in range(height):
        for x in range(width):
            if map_grid[y][x] in passable_chars and random.random() < heatmap[y][x]:
                starts.append((x, y))

    num_agents = len(starts)
    if num_agents == 0:
        print(f"Skipping {os.path.basename(map_filepath)}: 0 agents generated.")
        return

    # 4. Generate goal locations via Random Walk
    goals = []
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    map_area = width * height
    taken_goals = set()

    for (sx, sy) in starts:
        unique_goal_found = False
        max_retries = 50 
        
        for attempt in range(max_retries):
            cx, cy = sx, sy
            steps = random.randint(1, map_area)

            for _ in range(steps):
                valid_moves = []
                for dx, dy in directions:
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < width and 0 <= ny < height and map_grid[ny][nx] in passable_chars:
                        valid_moves.append((nx, ny))

                if not valid_moves:
                    break 

                cx, cy = random.choice(valid_moves)

            if (cx, cy) not in taken_goals:
                goals.append((cx, cy))
                taken_goals.add((cx, cy))
                unique_goal_found = True
                break 
        
        if not unique_goal_found:
            goals.append((cx, cy)) # Fallback to a duplicate if map is too crowded

    # 5. Write to .scen file
    map_filename = os.path.basename(map_filepath)
    with open(output_file, 'w') as f:
        f.write("version 1\n")
        for i in range(num_agents):
            sx, sy = starts[i]
            gx, gy = goals[i]
            manhattan = abs(sx - gx) + abs(sy - gy)
            f.write(f"0\t{map_filename}\t{width}\t{height}\t{sx}\t{sy}\t{gx}\t{gy}\t{manhattan}\n")

    print(f"Generated {output_file} with {num_agents} agents.")


# --- FUNCTION 2: Directory Batch Processor ---
def generate_for_directory(input_dir, output_dir, base_density=0.05, num_hotspots=3):
    """
    Finds all .map files in the input directory and generates a .scen for every single one.
    """
    os.makedirs(output_dir, exist_ok=True)
    map_files = glob.glob(os.path.join(input_dir, "*.map"))
    
    if not map_files:
        print(f"No .map files found in {input_dir}")
        return

    print(f"Processing {len(map_files)} maps...")
    for map_filepath in map_files:
        filename = os.path.basename(map_filepath)
        scen_filename = filename.replace(".map", ".scen")
        output_filepath = os.path.join(output_dir, scen_filename)
        
        generate_heatmap_scen(map_filepath, output_filepath, base_density, num_hotspots)


# --- FUNCTION 3: Probabilistic Batch Processor ---
def generate_with_probability(input_dir, output_dir, probability, base_density, num_hotspots):
    """
    Finds all .map files in a directory, but only generates a .scen file 
    if a random roll falls below the given probability (0.0 to 1.0).
    """
    if not (0.0 <= probability <= 1.0):
        raise ValueError("Probability must be between 0.0 and 1.0")

    os.makedirs(output_dir, exist_ok=True)
    map_files = glob.glob(os.path.join(input_dir, "*.map"))
    
    if not map_files:
        print(f"No .map files found in {input_dir}")
        return

    processed_count = 0
    print(f"Evaluating {len(map_files)} maps with a {probability*100:.1f}% selection chance...")
    
    for map_filepath in map_files:
        if random.random() < probability:
            filename = os.path.basename(map_filepath)
            scen_filename = filename.replace(".map", ".scen")
            output_filepath = os.path.join(output_dir, scen_filename)
            
            generate_heatmap_scen(map_filepath, output_filepath, base_density, num_hotspots)
            processed_count += 1

    print(f"\nDone! Generated scenes for {processed_count} out of {len(map_files)} maps.")
	
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



def random_delete_lines(input_directory: str, drop_probability: float):
    """
    Iterates through all files in a directory, keeping the first line of each file, 
    and deleting subsequent lines with the given probability.
    
    Args:
        input_directory (str): The path to the target directory.
        drop_probability (float): A float between 0.0 and 1.0 representing the 
                                  chance of deleting a line.
    """
    # Validate the probability input
    if not (0.0 <= drop_probability <= 1.0):
        raise ValueError("Drop probability must be a float between 0.0 and 1.0")

    # Traverse the directory tree
    for root, _, files in os.walk(input_directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            
            try:
                # Read all lines from the file
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                # Skip if the file is completely empty
                if not lines:
                    continue
                    
                # Keep the first line, process the rest
                new_lines = [lines[0]]
                for line in lines[1:]:
                    # random.random() generates a float between 0.0 and 1.0
                    # If it's greater than or equal to the drop probability, we keep the line
                    if random.random() >= drop_probability:
                        new_lines.append(line)
                        
                # Write the surviving lines back to the file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(new_lines)
                    
            except UnicodeDecodeError:
                # Silently skip binary files (like .png, .pyc, etc.) or non-UTF-8 files
                pass
            except Exception as e:
                # Catch permission errors or other I/O issues
                print(f"Error processing {file_path}: {e}")


if __name__ == "__main__":
	generate_with_probability("./heatmapbasedmapgeneration", "./newmapsSEND", 0.1, 0.1, 10)
	generate_with_probability("./heatmapbasedmapgeneration", "./newmapsSEND", 0.1, 0.6, 3)
	generate_with_probability("./heatmapbasedmapgeneration", "./newmapsSEND", 0.1, 0.1, 5)
	generate_with_probability("./latticewarehousemapgeneration", "./newmapsSEND", 0.1, 0.1, 10)
	generate_with_probability("./latticewarehousemapgeneration", "./newmapsSEND", 0.1, 0.6, 3)
	generate_with_probability("./latticewarehousemapgeneration", "./newmapsSEND", 0.1, 0.1, 5)