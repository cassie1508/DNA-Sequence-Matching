def edit_distance(seq1, seq2):
     """
     Computes the edit distance (Levenshtein distance) between two sequences.
     The cost for insertion, deletion, or substitution is set to 1.

     Parameters:
         seq1 (str): First DNA sequence.
         seq2 (str): Second DNA sequence.

     Returns:
         int: The edit distance between seq1 and seq2.
     """
     m, n = len(seq1), len(seq2)

     # Create a table with (m+1) x (n+1)
     dp = [[0] * (n + 1) for _ in range(m + 1)]

     for i in range(m + 1):
         dp[i][0] = i  # cost of deleting all characters from seq1
     for j in range(n + 1):
         dp[0][j] = j  # cost of inserting all characters to match seq2

     for i in range(1, m + 1):
         for j in range(1, n + 1):
             # If characters are the same, no substitution cost; otherwise, cost is 1.
             if seq1[i - 1] == seq2[j - 1]:
                 cost = 0
             else:
                 cost = 1

             dp[i][j] = min(
                 dp[i - 1][j] + 1,      # deletion
                 dp[i][j - 1] + 1,      # insertion
                 dp[i - 1][j - 1] + cost  # substitution
             )
     return dp[m][n]

def find_best_alignment(database, target):
    """
    Parameters:
        database (list of str): List of DNA sequences.
        target (str): The target DNA sequence to compare against.

    Returns:
        tuple: (best_sequence, best_distance)
    """
    best_distance = float('inf')
    best_sequence = None

    for seq in database:
        distance = edit_distance(seq, target)
        # Debug: Uncomment the next line to print each sequence's distance.
        # print(f"Comparing: {seq} | Distance: {distance}")
        if distance < best_distance:
            best_distance = distance
            best_sequence = seq

    return best_sequence, best_distance


if __name__ == "__main__":
    dna_database = [
        "ATGCGTAC",
        "ATCCGTAG",
        "ATGCGTAA",
        "ATGCGTGC"
    ]
    target_dna = "ATGCGTAT"

    best_seq, best_dist = find_best_alignment(dna_database, target_dna)
    print(f"Best matching sequence: {best_seq} with edit distance: {best_dist}")
