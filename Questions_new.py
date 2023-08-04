import os
import re
import csv

# Function to read text from a plain text file
def read_plain_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

# Function to check if the text ends with "?"
def ends_with_question(text):
    return text.endswith("?")

# Function to find text between "Debug Info" and "Google Workspace logo\nGoogle Workspace"
def find_debug_info(text):
    pattern = r"Debug Info(.*?)Google Workspace logo\nGoogle Workspace"
    regex = re.compile(pattern, re.DOTALL)
    match = regex.search(text)
    return match.group(1).strip() if match else ""

# Function to extract text based on interrogative words or specific keywords
def extract_text_with_conditions(text):
    sentences = text.split(".")
    extracted_text = []

    for sentence in sentences:
        sentence = sentence.strip()
        if ends_with_question(sentence) or sentence.startswith(('please', 'summarize', 'find', 'will','Please', 'Summarize', 'Find', 'Will','summarise','summarize','can','how','when','where','why','Can','How','When','Where','Why','what','What','bard','Bard')):
            extracted_text.append(sentence)

    return "\n".join(extracted_text)

# Create a list to store the extracted text and corresponding file names
extracted_data = []

# Path to the Transcripts folder
transcripts_folder = r"C:\Users\sneha\Desktop\All\PulseLabs\Transcripts"

# Iterate through all ".txt" files in the Transcripts folder
for file_name in os.listdir(transcripts_folder):
    if file_name.lower().endswith('.txt'):
        try:
            file_path = os.path.join(transcripts_folder, file_name)

            # Read the text from the plain text file
            text = read_plain_text(file_path)

            # Extract text based on conditions
            extracted_text = extract_text_with_conditions(text)

            # Extract text between "Debug Info" and "Google Workspace logo\nGoogle Workspace"
            debug_info_text = find_debug_info(text)
            if debug_info_text:
                extracted_text += "\n" + debug_info_text

            # Store the extracted text and corresponding file name in the list
            extracted_data.append((file_name, extracted_text))

        except Exception as e:
            print(f"Error reading text from {file_name}: {e}")

# Write the extracted data to a CSV file
output_csv_file = 'Questions.csv'
with open(output_csv_file, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['File Name', 'Extracted Text'])
    csv_writer.writerows(extracted_data)

print(f"Data extracted from all files and saved to {output_csv_file}")
