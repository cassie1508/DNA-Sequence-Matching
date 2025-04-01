from dna_matcher import longest_common_substring
from edit_distance import edit_distance
from L_C_sequence import longest_common_sequence

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

# def validate_fasta_file(filename):

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
    for _ in range(3):
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

    option = input("Choose the algorithm for comparison (1: Longest Common Substring, 2: Edit Distance: , 3: Longest Common Sequence ").strip()
    if option == "1":
      print("\n🔍 Comparing using Longest Common Substring...\n")
    elif option == "2":
      print("\n🔍 Comparing using Edit Distance...\n")
    elif option == "3":
      print("\n🔍 Comparing using Longest Common Sequence...\n")
    else:
      print("❌ Invalid option. Please enter 1, 2, or 3.")
      return

    # Initialize best match tracking
    best_score = float('-inf') if option != "2" else float('inf')
    best_name = ""
    best_match_segment = ""
    results = []

    # Compare query to each database sequence
    for name, sequence in db_data.items():
        if option == "1":
          score, segment = longest_common_substring(sequence, query_seq)
        elif option == "2":
          score = edit_distance(sequence, query_seq)
          segment = ""
        else:
          score, segment = longest_common_sequence(sequence, query_seq)
        results.append((name, score, segment))
        print(f"→ Similarity with '{name}': Score = {score}, Match = {segment if segment else '[not shown]'}")

        if score > best_score and (option == "1" or option == "3"):
            best_score = score
            best_name = name
            best_match_segment = segment
        elif option == "2" and score < best_score:
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
