import os
import csv
from collections import defaultdict

def create_dictionary_from_csv(input_file, output_dir="dictionary_by_letter"):
    """
    Convert CSV dictionary to Webster's format in A-Z files.
    Handles multi-line definitions properly.
    """

    os.makedirs(output_dir, exist_ok=True)
    words_by_letter = defaultdict(list)

    print(f"Reading {input_file}...")
    try:
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.DictReader(f)  # Use DictReader to handle header automatically

            for row in reader:
                word = row['word'].strip() if row['word'] else None

                if not word:
                    continue

                wordtype = row['wordtype'].strip() if row['wordtype'] else ""
                definition = row['definition'].strip() if row['definition'] else ""

                # Clean up newlines in definition
                definition = definition.replace('\n', ' ').replace('   ', ' ')

                # Format: word (wordtype) definition
                if wordtype:
                    formatted_entry = f"{word} ({wordtype}) {definition}"
                else:
                    formatted_entry = f"{word} {definition}"

                first_letter = word[0].upper()
                words_by_letter[first_letter].append(formatted_entry)

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        return
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # Write files for each letter
    print(f"Creating files in {output_dir}...")
    for letter in sorted(words_by_letter.keys()):
        output_file = os.path.join(output_dir, f"{letter}.txt")
        with open(output_file, 'w', encoding='utf-8') as f:
            # Sort alphabetically within each letter
            for entry in sorted(words_by_letter[letter]):
                f.write(entry + "\n")
        print(f"Created {letter}.txt with {len(words_by_letter[letter])} entries")

    print("\nDone! Dictionary files created successfully.")

# Usage
create_dictionary_from_csv("dictionary.csv", "dictionary_by_letter")
