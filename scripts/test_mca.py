import pandas as pd
import prince
from utils.data_loader import load_data, clean_data

print("--- Test Technique MCA ---")

# 1. Load Data
df = load_data()
df = clean_data(df)
print(f"Data Loaded: {df.shape}")

# 2. Select Variables (same default as app)
selected_actives = ['C_leg', 'C_frui', 'C_viaR', 'C_viaB', 'C_indu', 'C_poi']
print(f"Active Vars: {selected_actives}")

# 3. Prepare Data
X = df[selected_actives].fillna("Non répondu")
print("Data Prepared for Prince.")

# 4. Fit MCA
try:
    mca = prince.MCA(
        n_components=2,
        n_iter=3,
        copy=True,
        check_input=True,
        engine='sklearn',
        random_state=42
    )
    mca = mca.fit(X)
    print("MCA Fit Success!")
    
    coords = mca.column_coordinates(X)
    print("Coordinates computed.")
    print(coords.head())
    
except Exception as e:
    print(f"ERROR MCA: {e}")
    import traceback
    traceback.print_exc()

print("--- End Test ---")
