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
     a, b = len(seq1), len(seq2)

     # Create a table with (m+1) x (n+1)
     dp = [[0] * (b + 1) for _ in range(a + 1)]

     for i in range(a + 1):
         dp[i][0] = i  # cost of deleting all characters from seq1
     for j in range(b + 1):
         dp[0][j] = j  # cost of inserting all characters to match seq2

     for i in range(1, a + 1):
         for j in range(1, b + 1):
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
     return dp[a][b]




