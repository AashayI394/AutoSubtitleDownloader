import os
import pandas as pd

# Name of the master CSV file
master_file_name = "master.csv"

# Get the current working directory
current_folder = os.getcwd()

# Path to master.csv in the current directory
master_file_path = os.path.join(current_folder, master_file_name)

# Load the existing master.csv file
if os.path.exists(master_file_path):
    master_df = pd.read_csv(master_file_path)
else:
    print(f"Error: {master_file_name} not found in the current directory.")
    exit()

# Iterate through all CSV files in the current folder
for filename in os.listdir(current_folder):
    if filename.endswith(".csv") and filename != master_file_name:  # Exclude master.csv itself
        file_path = os.path.join(current_folder, filename)
        # Load the current CSV file
        try:
            current_df = pd.read_csv(file_path)
            # Append the data to master_df
            master_df = pd.concat([master_df, current_df], ignore_index=True)
            print(f"Merged: {filename}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")

# (Optional) Remove duplicate rows if needed
# master_df = master_df.drop_duplicates()

# Save the updated master_df back to master.csv
master_df.to_csv(master_file_path, index=False)

print(f"All CSV files merged successfully into {master_file_name}.")

