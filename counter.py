import pandas as pd

def analyze_solver_stats(csv_file, main_col, sub_col1, sub_col2, sub_col3, aux_col, aux_val):
    # 1. Load the CSV into a pandas DataFrame
    df = pd.read_csv(csv_file)
    
    # Group the sub columns into a list for easy checking
    sub_cols = [sub_col1, sub_col2, sub_col3]
    
    # --- Define Base Conditions ---
    # Condition: The main column equals 1
    main_condition = (df[main_col] == 1)
    
    # Condition: At least ONE of the sub columns equals 1
    sub_condition = (df[sub_cols] == 1).any(axis=1)
    
    # Condition: ALL of the sub columns equal 0
    all_subs_zero_condition = (df[sub_cols] == 0).all(axis=1)
    
    # Condition: Auxiliary column matches the specific target string
    aux_condition = (df[aux_col] == aux_val)

    # --- Calculate the Three Metrics ---
    
    # 1. Total number of 1s in the main column
    count_main_ones = main_condition.sum()
    
    # 2. Main column is 1 AND at least one sub-column is 1
    count_main_and_subs = (main_condition & sub_condition).sum()
    
    # 3. Auxiliary column equals the target value AND all sub-columns are 0
    count_aux_and_no_subs = (aux_condition & all_subs_zero_condition).sum()
    
    return count_main_ones, count_main_and_subs, count_aux_and_no_subs

# --- Example Usage ---
csv_path = 'recalculated_maps_analytics.csv'

# Unpack the three returned values
main_ones, main_and_subs, aux_and_no_subs = analyze_solver_stats(
    csv_file=csv_path, 
    main_col='solved_by_sat', 
    sub_col1='solved_by_cbs', 
    sub_col2='solved_by_bcp', 
    sub_col3='solved_by_cbsh',
    aux_col='fastest_solver',
    aux_val='SAT'
)

print(f"Total times 'solved_by_sat' equals 1: {main_ones}")
print(f"Total times 'solved_by_sat' equals 1 AND a sub-solver equals 1: {main_and_subs}")
print(f"Total times 'fastest_solver' is 'SAT' AND all sub-solvers are 0: {aux_and_no_subs}")