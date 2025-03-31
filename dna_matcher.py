# dna_matcher.py

# This script compares a DNA query sequence to a database of DNA sequences.
# Algorithm used: Longest Common Substring (LCS)
# - Finds the longest continuous substring shared by two sequences.
# - Runtime: O(n * m), Space: O(n * m)
# It outputs both the similarity score and the matching segment,
# and writes all results to a file. Users get 3 attempts to enter valid filenames.

def read_fasta_file(filename):
    """Reads a FASTA-format file and returns a dictionary of {sequence_name: sequence}"""
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
                name = line[1:]
                seq_lines = []
            else:
                seq_lines.append(line)
        if name:
            sequences[name] = ''.join(seq_lines).upper()
    return sequences


def longest_common_substring(s, t):
    """Returns the length and sequence of the longest common substring between s and t"""
    n, m = len(s), len(t)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    max_len = 0
    end_pos = 0
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s[i - 1] == t[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                if dp[i][j] > max_len:
                    max_len = dp[i][j]
                    end_pos = i
            else:
                dp[i][j] = 0
    return max_len, s[end_pos - max_len:end_pos]


def main():
    print("🧬 DNA Sequence Matcher - Longest Common Substring Only 🧬\n")

    # Try up to 3 times to get a valid query file
    for attempt in range(3):
        query_file = input("Enter the query file name (e.g. DNA_query.txt): ").strip()
        try:
            query_data = read_fasta_file(query_file)
            if len(query_data) != 1:
                print("❌ Query file must contain exactly one sequence.")
                continue
            break
        except FileNotFoundError:
            print("❌ File not found. Please check the filename.")
    else:
        print("❌ Sorry, the query file is incorrect. Your three attempts are over.")
        return

    # Try up to 3 times to get a valid database file
    for attempt in range(3):
        db_file = input("Enter the database file name (e.g. DNA_sequences.txt): ").strip()
        try:
            db_data = read_fasta_file(db_file)
            break
        except FileNotFoundError:
            print("❌ File not found. Please check the filename.")
    else:
        print("❌ Sorry, the database file is incorrect. Your three attempts are over.")
        return

    query_name, query_seq = list(query_data.items())[0]

    print("\n🔍 Comparing using Longest Common Substring...\n")

    # Initialize best match tracking
    best_score = float('-inf')
    best_name = ""
    best_match_segment = ""
    results = []

    # Compare query to each database sequence
    for name, sequence in db_data.items():
        score, segment = longest_common_substring(sequence, query_seq)
        results.append((name, score, segment))
        print(f"→ Similarity with '{name}': Score = {score}, Match = {segment if segment else '[not shown]'}")
        if score > best_score:
            best_score = score
            best_name = name
            best_match_segment = segment

    # Output the best match
    print("\n✅ Most similar sequence found:")
    print(f"🧬 Name: {best_name}")
    print(f"📊 Score: {best_score}")
    print(f"🧩 Matching Segment: {best_match_segment if best_match_segment else '[not shown]'}")

    # Write results to a file
    with open("results.txt", "w") as out:
        out.write(f"Query: {query_name}\n")
        out.write("Algorithm: Longest Common Substring\n")
        out.write(f"Best Match: {best_name} (Score: {best_score})\n")
        out.write(f"Matching Segment: {best_match_segment if best_match_segment else '[not shown]'}\n\n")
        out.write("All Matches:\n")
        for name, score, segment in sorted(results, key=lambda x: x[1], reverse=True):
            out.write(f"{name}: Score = {score}, Match = {segment if segment else '[not shown]'}\n")

    print("\n📝 Results saved to 'results.txt'")


if __name__ == "__main__":
    main()
