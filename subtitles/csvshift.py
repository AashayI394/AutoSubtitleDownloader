import os
import shutil

def move_csv_and_excel_files():
    """
    Creates a 'csvs' directory in the current folder and moves all .csv and .xlsx files into it.
    """
    # Get the current folder
    current_folder = os.getcwd()
    target_folder = os.path.join(current_folder, "csvs")

    # Create the 'csvs' directory if it doesn't exist
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
        print(f"Created directory: {target_folder}")
    else:
        print(f"Directory already exists: {target_folder}")

    # Get all .csv and .xlsx files in the current folder
    files_moved = []
    for file_name in os.listdir(current_folder):
        if file_name.endswith(('.csv', '.xlsx')) and os.path.isfile(file_name):
            # Source and destination paths
            source_path = os.path.join(current_folder, file_name)
            destination_path = os.path.join(target_folder, file_name)
            
            # Move the file
            shutil.move(source_path, destination_path)
            files_moved.append(file_name)

    # Output results
    if files_moved:
        print(f"Moved {len(files_moved)} file(s): {', '.join(files_moved)}")
    else:
        print("No .csv or .xlsx files found to move.")

if __name__ == "__main__":
    move_csv_and_excel_files()
