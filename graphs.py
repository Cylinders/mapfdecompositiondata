import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

# 1. Read the CSV file into a Pandas DataFrame
df = pd.read_csv('recalculated_maps_analytics.csv')

# --- NEW: Filter the data by Map ---
# Replace 'Map_Name_Column' with the actual header for your map names
# Replace 'Target_Map' with the exact name of the map you want to graph
map_column = 'map_class'
selected_map = 'den520d'

# This creates a new, smaller DataFrame containing ONLY rows matching your map
df_filtered = df[df[map_column] == selected_map]

# Failsafe: Check if the spelling was wrong and the new dataframe is empty
if df_filtered.empty:
    print(f"Error: No data found. Please check if '{selected_map}' and '{map_column}' are spelled correctly.")
else:
    # 2. Define your base X-axis data using the FILTERED dataframe
    x = df_filtered['number_of_agents']

    # --- Helper function to calculate R-squared ---
    def get_r_squared(x_data, y_data):
        # Failsafe: Ensure there are enough points to calculate a trendline
        if len(x_data) < 2:
            return 0.0
        slope, intercept, r_value, p_value, std_err = linregress(x_data, y_data)
        return r_value**2

    # 3. Filter out '-1' values for EACH algorithm independently using the FILTERED dataframe
    mask_bcp = df_filtered['bcp_runtime'] != -1
    x_bcp, y_bcp = x[mask_bcp], df_filtered['bcp_runtime'][mask_bcp]

    mask_cbs = df_filtered['cbs_runtime'] != -1
    x_cbs, y_cbs = x[mask_cbs], df_filtered['cbs_runtime'][mask_cbs]

    mask_cbsh = df_filtered['cbsh_runtime'] != -1
    x_cbsh, y_cbsh = x[mask_cbsh], df_filtered['cbsh_runtime'][mask_cbsh]

    mask_sat = df_filtered['sat_runtime'] != -1
    x_sat, y_sat = x[mask_sat], df_filtered['sat_runtime'][mask_sat]

    # 4. Calculate R^2 using the newly filtered data
    r2_bcp = get_r_squared(x_bcp, y_bcp)
    r2_cbs = get_r_squared(x_cbs, y_cbs)
    r2_cbsh = get_r_squared(x_cbsh, y_cbsh)
    r2_sat = get_r_squared(x_sat, y_sat)

    # 5. Plot each column as a scatter plot
    plt.scatter(x_bcp, y_bcp, color='red', alpha=0.7, label=f'BCP ($R^2={r2_bcp:.3f}$)')
    plt.scatter(x_cbs, y_cbs, color='blue', alpha=0.7, label=f'CBS ($R^2={r2_cbs:.3f}$)')
    plt.scatter(x_cbsh, y_cbsh, color='green', alpha=0.7, label=f'CBSH ($R^2={r2_cbsh:.3f}$)')
    plt.scatter(x_sat, y_sat, color='purple', alpha=0.7, label=f'SAT ($R^2={r2_sat:.3f}$)')

    # 6. Format the graph for readability
    # The title will now dynamically update to show which map you are looking at!
    plt.title(f'Comparing TIME VS AGENT SPARSITY ({selected_map})')
    plt.xlabel('Number of Agents')
    plt.ylabel('Time (Seconds)')

    # Display the legend
    plt.legend()

    # Add a grid
    plt.grid(True)

    # 7. Render the final plot
    plt.show()