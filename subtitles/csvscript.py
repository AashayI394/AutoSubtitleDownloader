import os
import csv
import re

def srt_to_csv(srt_file):
    """
    Converts an .srt file to a .csv file in the same folder as the .srt file.
    The CSV file will have columns: Start Timestamp, End Timestamp, Dialogue.
    """
    # Regular expression to match SRT timestamps
    timestamp_pattern = r"(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})"
    
    # Determine the CSV file name
    csv_file = os.path.splitext(srt_file)[0] + ".csv"
    print(f"Processing file: {srt_file}")

    try:
        # Read the SRT file
        with open(srt_file, 'r', encoding='utf-8') as srt:
            lines = srt.readlines()
        
        rows = []
        i = 0
        while i < len(lines):
            # Skip line numbers
            if lines[i].strip().isdigit():
                i += 1
            
            # Extract timestamps
            if re.match(timestamp_pattern, lines[i]):
                timestamps = re.findall(timestamp_pattern, lines[i])
                start, end = timestamps[0]
                i += 1
                
                # Collect the dialogue lines
                dialogue_lines = []
                while i < len(lines) and lines[i].strip():
                    dialogue_lines.append(lines[i].strip())
                    i += 1
                
                dialogue = " ".join(dialogue_lines)
                rows.append([start, end, dialogue])
            
            i += 1
        
        # Write to a CSV file in the same directory
        with open(csv_file, 'w', newline='', encoding='utf-8') as csv_output:
            writer = csv.writer(csv_output)
            # Write header
            writer.writerow(["Start Timestamp", "End Timestamp", "Dialogue"])
            # Write rows
            writer.writerows(rows)

        print(f"Converted {srt_file} to {csv_file}")

    except Exception as e:
        print(f"Failed to process {srt_file}: {e}")


def convert_all_srt_in_folder(folder_path):
    """
    Converts all .srt files in the specified folder to .csv files.
    """
    srt_files = [file for file in os.listdir(folder_path) if file.endswith('.srt')]
    
    if not srt_files:
        print("No .srt files found in the folder.")
        return
    
    for file_name in srt_files:
        srt_file = os.path.join(folder_path, file_name)
        srt_to_csv(srt_file)


# Example Usage: Specify the current directory
if __name__ == "__main__":
    current_folder = os.getcwd()
    print(f"Looking for .srt files in folder: {current_folder}")
    convert_all_srt_in_folder(current_folder)
    print("Processing complete.")
