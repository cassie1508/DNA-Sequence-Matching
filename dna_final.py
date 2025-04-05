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

def classify_match_strength(similarity):
    if similarity > 0.9:
        return "Highly similar"
    elif similarity > 0.75:
        return "Moderately similar"
    elif similarity > 0.5:
        return "Some similarity"
    else:
        return "Low similarity"


def interpret_results(results, query_seq, option):
    if option not in ["1", "3"]:
        return  # Only interpret LCS and LCSubstring

    print("\n📊 Interpretation of Top 3 Results:")
    results = sorted(results, key=lambda x: x[1], reverse=True)[:3]

    for i, (name, score, segment) in enumerate(results, 1):
        similarity = score / len(query_seq)
        interpretation = classify_match_strength(similarity)
        label = "LCS" if option == "3" else "LCSubstring"

        print(f"\n{i}. 🧬 {name}")
        print(f" {label} Length: {score}")
        print(f" Query percentage: {similarity * 100:.2f}% : {interpretation} match")


    

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

    for name, sequence in db_data.items():
        if option == "1":
            score, segment = longest_common_substring(sequence, query_seq)
        elif option == "2":
            score = edit_distance(sequence, query_seq)
            similarity = 1 - (score / max(len(sequence), len(query_seq)))
            interpretation = classify_match_strength(similarity)
            results.append([name, score, similarity, interpretation])
            print(f"→ Edit distance with '{name}': Score = {score}, Similarity = {similarity:.2f}, Interpretation = {interpretation}")
            if score < best_score:
                best_score = score
                best_name = name
                best_interpretation = interpretation
                best_similarity= similarity
            continue
        else:
            score, segment = longest_common_sequence(sequence, query_seq)

        results.append((name, score, segment))
        print(f"→ Match with '{name}': Score = {score}, Match = {segment if segment else '[not shown]'}")
        if score > best_score:
            best_score, best_name, best_segment = score, name, segment
    
    print("\n✅ Most similar sequence found:")
    print(f"🧬 Name: {best_name}")
    print(f"📊 Score: {best_score}")
    if option == "1" or option == "3":
        print(f"🧩 Segment: {best_segment if best_segment else '[not shown]'}")
    else:
        print(f"💭Interpretation: {best_interpretation}")
        print(f"✨ Similarity: {best_similarity:.2f}")
        print("\nSequences with High or Moderate Similarity:")
        interpret_score = input("\n Would you like to interpret the top 3 results? (yes/no): ").strip().lower()
        if interpret_score == "yes":
            print("\n📊 Interpretation of Top 3 Results (Edit Distance):")
            top3 = sorted(results, key=lambda x: x[1])[:3]
            for i, (name, score, similarity, interpretation) in enumerate(top3, 1):
                print(f"\n{i}. 🧬 {name}")
                print(f" Score: {score}")
                print(f"✨ Similarity: {similarity * 100:.2f}% : {interpretation} match")

    if option != "2" and input("\nInterpret top 3 matches? (yes/no): ").strip().lower() == "yes":
        interpret_results(results, query_seq, option)


    # Write results to a file
    with open("results.txt", "w") as out:
        out.write(f"Query: {query_name}\n")
        out.write(f"Algorithm: {'LCSubstring' if option == '1' else 'Edit Distance' if option == '2' else 'LCS'}\n")
        out.write(f"Best Match: {best_name} (Score: {best_score})\n")
        if option in ["1", "3"]:
            out.write(f"Matching Segment: {best_segment if best_segment else '[not shown]'}\n")
        else:
            out.write(f"Similarity: {best_similarity:.2f}, Interpretation: {best_interpretation}\n")

        out.write("\nAll Matches:\n")
        if option == "2":
            for name, score, similarity, interpretation in sorted(results, key=lambda x: x[1]):
                out.write(f"{name}: Edit Distance = {score}, Similarity = {similarity:.2f}, Interpretation = {interpretation}\n")
        else:
            for name, score, segment in sorted(results, key=lambda x: x[1], reverse=True):
                out.write(f"{name}: Score = {score}, Segment = {segment if segment else '[not shown]'}\n")

    print("\n📝 Results saved to 'results.txt'")

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
