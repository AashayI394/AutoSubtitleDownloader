import os
import pandas as pd

def merge_csv_files():
    """
    Combines all .csv files in the current folder into a single 'master.csv' file.
    The master file retains the structure: IMDB ID, Start Timestamp, End Timestamp, Dialogue.
    """
    current_folder = os.getcwd()
    master_file = os.path.join(current_folder, "master.csv")

    # List to hold DataFrames from each file
    dataframes = []
    files_processed = []

    for file_name in os.listdir(current_folder):
        # Process only .csv files
        if file_name.endswith('.csv') and file_name != "master.csv":
            file_path = os.path.join(current_folder, file_name)
            try:
                # Read the CSV file
                df = pd.read_csv(file_path)

                # Ensure the structure matches the expected columns
                expected_columns = ["IMDB ID", "Start Timestamp", "End Timestamp", "Dialogue"]
                if list(df.columns) != expected_columns:
                    print(f"Skipping {file_name}: Unexpected columns {list(df.columns)}")
                    continue

                # Add to the list of DataFrames
                dataframes.append(df)
                files_processed.append(file_name)
            except Exception as e:
                print(f"Failed to process {file_name}: {e}")

    if dataframes:
        # Concatenate all DataFrames
        master_df = pd.concat(dataframes, ignore_index=True)

        # Save the combined DataFrame to master.csv
        master_df.to_csv(master_file, index=False)
        print(f"Master file created: {master_file} ({len(master_df)} rows)")
    else:
        print("No valid .csv files found to merge.")

    if files_processed:
        print(f"Successfully merged {len(files_processed)} file(s): {', '.join(files_processed)}")
    else:
        print("No .csv files were merged.")

if __name__ == "__main__":
    merge_csv_files()
