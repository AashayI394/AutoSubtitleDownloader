import os
import pandas as pd

def add_imdb_id_column():
    """
    Opens each .csv or .xlsx file in the current folder, adds a new column titled "IMDB ID",
    and populates it with the filename (without extension) for all rows.
    """
    current_folder = os.getcwd()

    # Process each .csv or .xlsx file in the folder
    files_processed = []
    for file_name in os.listdir(current_folder):
        # Check for .csv or .xlsx files
        if file_name.endswith(('.csv', '.xlsx')):
            file_path = os.path.join(current_folder, file_name)
            try:
                # Read file into a DataFrame
                if file_name.endswith('.csv'):
                    df = pd.read_csv(file_path)
                else:
                    df = pd.read_excel(file_path)

                # Add "IMDB ID" column with the filename (without extension)
                imdb_id = os.path.splitext(file_name)[0]  # Filename without extension
                df.insert(0, "IMDB ID", imdb_id)

                # Save back to file
                if file_name.endswith('.csv'):
                    df.to_csv(file_path, index=False)
                else:
                    df.to_excel(file_path, index=False)

                files_processed.append(file_name)
                print(f"Processed file: {file_name}")
            except Exception as e:
                print(f"Failed to process {file_name}: {e}")

    if files_processed:
        print(f"Successfully processed {len(files_processed)} file(s): {', '.join(files_processed)}")
    else:
        print("No .csv or .xlsx files found in the folder.")

if __name__ == "__main__":
    add_imdb_id_column()

