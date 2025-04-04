# DNA Sequence Matcher

This is a Python project that compares a DNA query sequence against a database of sequences using different algorithms. It's designed for students or anyone learning about string matching in bioinformatics, and it works entirely in the command line for simplicity.

## Project Structure

- `dna_matcher_main.py`: Main script that handles user input, file reading, and calls the selected comparison algorithm.
- `dna_matcher.py`: Contains the function for Longest Common Substring.
- `edit_distance.py`: Contains the Edit Distance (Levenshtein Distance) function.
- `L_C_sequence.py`: Contains the Longest Common Subsequence function.
- `DNA_query.txt`: Sample FASTA file containing one query sequence.
- `DNA_sequences.txt`: Sample FASTA file containing multiple database sequences.
- `results.txt`: Automatically generated file with comparison results after the program runs.

## How to Run

1. Make sure Python 3 is installed on your system.
2. Open a terminal or command prompt in the project directory.
3. Run the program with: `python dna_matcher_main.py`
4. When prompted, provide the filename of your query file (e.g., `DNA_query.txt`). This file should contain exactly one sequence.
5. Provide the database filename (e.g., `DNA_sequences.txt`). This file can contain multiple sequences.
6. Choose the algorithm to use:
   - Type `1` for Longest Common Substring
   - Type `2` for Edit Distance
   - Type `3` for Longest Common Subsequence
7. The program will compare the query sequence with each database sequence, display the results in the terminal, and save everything in `results.txt`.

## FASTA File Format

Both the query and database files must follow the FASTA format. This means each sequence starts with a line that begins with a greater-than sign (`>`), followed by the sequence name. The next line(s) should contain the actual DNA sequence. Example:
sequence1 ACTGACTGACTG


- The query file must contain exactly one sequence.
- The database file can contain as many sequences as needed, each with a unique header.

## Sample Output

Console output will look something like this:
Similarity with 'sequence1': Score = 12, Match = ACTGACTGACTG Similarity with 'sequence2': Score = 9, Match = CTGACTGAC Most similar sequence found: Name: sequence1 Score: 12 Matching Segment: ACTGACTGACTG

In `results.txt`, the output includes the query name, algorithm used, best match, and all individual results sorted by score.

## Algorithm Descriptions

- Longest Common Substring: Finds the longest uninterrupted sequence of characters shared between the query and a database sequence.
- Edit Distance: Calculates how many insertions, deletions, or substitutions are needed to transform one sequence into another. A lower score means a closer match.
- Longest Common Subsequence: Finds the longest sequence of characters that appear in the same relative order in both sequences, not necessarily contiguous.

## Purpose

This project was created as a way to learn how different string comparison algorithms work in the context of biological data. It's useful for understanding algorithm efficiency, data parsing, and simple applications of bioinformatics in Python. It also helped reinforce how to work with user input, file hand
