import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt

# 1. Load the dataset
file_path = 'recalculated_maps_analytics.csv'
df = pd.read_csv(file_path)

# 2. Select features and replace -1 with NaN for runtime calculations
features = ['map_dim_rows', 'map_dim_cols', 'num_static_obstacles', 'obstacle_density', 'Agent Spars', 'ROD']
runtime_cols = ['bcp_runtime', 'cbs_runtime', 'cbsh_runtime', 'sat_runtime']

# Replace -1 with np.nan for runtime columns so they don't skew averages
df_clean = df.copy()
df_clean[runtime_cols] = df_clean[runtime_cols].replace(-1, np.nan)

# 3. K-means Clustering
X_clust = df[features].fillna(0) 
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_clust)

num_clusters = 6
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
df['cluster_label'] = kmeans.fit_predict(X_scaled)

# 4. Global Display Options
pd.set_option('display.max_columns', None)  
pd.set_option('display.width', 1000)        
pd.set_option('display.max_colwidth', None) 

# Print your previous cluster metrics
print("--- Success Rate (%) per Cluster ---")
print((df[runtime_cols] != -1).groupby(df['cluster_label']).mean() * 100)
print("\n--- Average Runtime (Successful instances only) per Cluster ---")
print(df_clean.groupby(df['cluster_label'])[runtime_cols].mean())
print("\n--- Average Map Features per Cluster ---")
print(df.groupby('cluster_label')[features].mean())
print("\n" + "="*50 + "\n")

# =====================================================================
# NEW: Feature Importance Loop for Every Single Solver
# =====================================================================
print("--- Feature Importance Scores per Solver ---")

for target in runtime_cols:
    # Drop rows where this specific solver failed (is NaN)
    df_model = df_clean.dropna(subset=[target])
    
    # Check if we have enough data points to train
    if len(df_model) < 10:
        print(f"Skipping {target}: Not enough successful instances to calculate importance.")
        continue
        
    X_rf = df_model[features]
    y_rf = df_model[target]
    
    # Train the Random Forest
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_rf, y_rf)
    
    # Extract importances
    importances = rf.feature_importances_
    indices = np.argsort(importances)[::-1]
    
    # Print the text breakdown
    print(f"\n> Top Features driving {target}:")
    for rank, idx in enumerate(indices):
        print(f"  {rank+1}. {features[idx]}: {importances[idx]:.4f}")
        
    # Generate and save a plot for this specific solver
    plt.figure(figsize=(8, 5))
    plt.title(f"Feature Importance: What drives {target}?")
    plt.bar(range(X_rf.shape[1]), importances[indices], align="center", color='skyblue', edgecolor='black')
    plt.xticks(range(X_rf.shape[1]), [features[i] for i in indices], rotation=30, ha='right')
    plt.ylabel('Relative Importance Score')
    plt.tight_layout()
    
    # Saves as bcp_runtime_importance.png, cbs_runtime_importance.png, etc.
    plt.savefig(f'{target}_importance.png')
    plt.close() # Close plot to free up memory for the next loop

print("\nAll plots have been saved to your directory!")