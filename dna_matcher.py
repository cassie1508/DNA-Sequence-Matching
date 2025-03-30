# dna_matcher.py
from L_C_Sequence import *

def read_fasta_file(filename):
    sequences = {}
    with open(filename, 'r') as f:
        name = None
        seq_lines = []
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith('>'):
                if name:
                    sequences[name] = ''.join(seq_lines).upper()
                name = line[1:]  # remove '>'
                seq_lines = []
            else:
                seq_lines.append(line)
        if name:
            sequences[name] = ''.join(seq_lines).upper()
    return sequences


def longest_common_substring(s, t):
    #can you let it print the string of characters itself?
    
    n = len(s)
    m = len(t)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    max_len = 0
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s[i - 1] == t[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                max_len = max(max_len, dp[i][j])
            else:
                dp[i][j] = 0
    return max_len


def compute_similarity(algorithm, s, t):
    # while True:
    #     try:
    if algorithm == "1":
        print("\nComparing using Longest Common Substring...\n")
        return longest_common_substring(s,t)
    elif algorithm == "2":
        print("\nComparing using Longest Common Sequence...\n")
        return longest_common_sequence(s,t)
                
    # elif algorithm == "3":
        # except ValueError:
    else:
        print("Invalid option. Please select a valid algorithm.")
    


def main():
    print("🧬 DNA Sequence Matcher🧬\n")
    query_file = input("Enter the query file name (e.g. DNA_query.txt): ").strip()
    db_file = input("Enter the database file name (e.g. DNA_sequences.txt): ").strip()

    try:
        query_data = read_fasta_file(query_file)
        db_data = read_fasta_file(db_file)
    except FileNotFoundError:
        print("File not found. Please check the filenames.")
        return

    if len(query_data) != 1:
        print("Query file must contain exactly one sequence.")
        return

    query_name, query_seq = list(query_data.items())[0]

    algorithm = input("Select matching algorithm (1 for Longest Common Substring\n, 2 for Longest Common Subsequence \n and 3 for ...): ")
    

    best_score = float('-inf')
    best_name = ""
    for name, sequence in db_data.items():
        score = compute_similarity(algorithm, sequence, query_seq)
        print(f"→ Similarity with '{name}': {score}")
        if score > best_score:
            best_score = score
            best_name = name

    print("\n✅ Most similar sequence found:")
    print(f"🧬 Name: {best_name}")
    print(f"📊 Score: {best_score}")
    return 


if __name__ == "__main__":
    main()
