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

def interpret_results(results, query_seq, option):
    """Interprets results with query-centric strength classification."""
    
    # Sort results based on algorithm
    if option == "2":  # Edit Distance (lower = better)
        sorted_results = sorted(results, key=lambda x: x[1])
    else:  # LCS or LCSubstring (higher = better)
        sorted_results = sorted(results, key=lambda x: x[1], reverse=True)
    
    top_3 = sorted_results[:3]
    
    print("\n📊 Interpretation of Top 3 Results (Query-Centric):")
    for i, (name, score, segment) in enumerate(top_3, 1):
        target_len = len(segment) if segment else len(query_seq)  # Fallback
        
        if option == "1":  # Longest Common Substring
            query_coverage = (score / len(query_seq)) * 100
            strength = classify_match_strength(query_coverage)
            print(f"{i}. {name}:")
            print(f"   Substring length: {score} bases")
            print(f"   Query Coverage: {query_coverage:.2f}% → {strength} match")
            if strength == "Low":
                print("Weak alignment")
        
        elif option == "2":  # Edit Distance
            max_len = max(len(query_seq), target_len)
            similarity = (1 - (score / max_len)) * 100
            strength = classify_match_match_strength(similarity)
            print(f"{i}. {name}:")
            print(f"   Edit Distance: {score}")
            print(f"   Similarity: {similarity:.2f}% → {strength} match")
        
        elif option == "3":  # Longest Common Subsequence (LCS)
            query_coverage = (score / len(query_seq)) * 100
            strength = classify_match_strength(query_coverage)
            print(f"{i}. {name}:")
            print(f"   LCS length: {score} bases")
            print(f"   Query Coverage: {query_coverage:.2f}% → {strength} match")
            if strength == "Strong":
                print(" ✅ High confidence: Query is largely conserved in target.")
def classify_match_strength(coverage):
    """Classifies the match strength based on query coverage percentage."""
    if coverage < 60:
        return "Low"
    elif 60 <= coverage < 75:
        return "Medium"
    else:
        return "Strong"
    

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
    best_interpretation = ""
    best_similarity = 0.0
    

    # Compare query to each database sequence
    if option == "1" or option == "3":
        for name, sequence in db_data.items():
            if option == "1":
                score, segment = longest_common_substring(sequence, query_seq)
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
    elif option == "2":
        for name, sequence in db_data.items():
            score = edit_distance(sequence, query_seq)
            similarity = 1 - (score / max(len(sequence), len(query_seq)))

            if similarity > 0.9:
                interpretation = "Highly similar"
            elif similarity > 0.75:
                interpretation = "Moderately similar"
            elif similarity > 0.5:
                interpretation = "Some similarity"
            else:
                interpretation = "Low similarity"

            results.append([name, score, similarity, interpretation])
            print(f"→ Edit distance with '{name}': Score = {score}, Similarity = {similarity:.2f}, Interpretation = {interpretation}")

            if score < best_score:
                best_score = score
                best_name = name
                best_interpretation = interpretation
                best_similarity = similarity

    # Output the best match
    print("\n✅ Most similar sequence found:")
    print(f"🧬 Name: {best_name}")
    print(f"📊 Score: {best_score}")
    if option == "1" or option == "3":
        print(f"🧩 Matching Segment:{best_match_segment if best_match_segment else '[not shown]'}")
    else:
        print(f"🧩 Interpretations: {best_interpretation}")
        print(f"🧩 Similarity: {best_similarity:.2f}")
        print()
        print("Sequences with High or Moderate Similarity:\n")
        found_match = False

        for res in results:
            if res[3] in ["Highly similar", "Moderately similar"]:
                found_match = True
                print(f"Sequence: {res[0]}")
                print(f"Edit Distance: {res[1]}")
                print(f"Similarity: {res[2]:.2f}")
                print(f"Interpretation: {res[3]}")
                print()
    # Interpret the score
    interprate_score = input("Would You like to interprate the score? (yes/no): ").strip().lower()
    if interprate_score == "yes":
        interpret_results(results, query_seq, option)

    # Write results to a file
    with open("results.txt", "w") as out:
        out.write(f"Query: {query_name}\n")
        out.write("Algorithm: Longest Common Substring\n")
        out.write(f"Best Match: {best_name} (Score: {best_score})\n")
        out.write(f"Matching Segment: {best_match_segment if best_match_segment else '[not shown]'}\n\n")
        out.write("All Matches:\n")
        for name, score, segment in sorted(results, key=lambda x: x[1], reverse=True):
            out.write(f"{name}: Score = {score}, Match = {segment if segment else '[not shown]'}\n")

        if not found_match:
            print("❌ None of the sequences are moderately or highly similar to the query sequence.")


    # # Write results to a file
    # with open("results.txt", "w") as out:
    #     out.write(f"Query: {query_name}\n")
    #     out.write("Algorithm: Longest Common Substring\n")
    #     out.write(f"Best Match: {best_name} (Score: {best_score})\n")
    #     out.write(f"Matching Segment: {best_match_segment if best_match_segment else '[not shown]'}\n\n")
    #     out.write("All Matches:\n")
    #     for name, score, segment,  in sorted(results, key=lambda x: x[1], reverse=True):
    #         out.write(f"{name}: Score = {score}, Match = {segment if segment else '[not shown]'}\n")

    # print("\n📝 Results saved to 'results.txt'")


if __name__ == "__main__":
    main()
