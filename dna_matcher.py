# dna_matcher.py

# This script compares a DNA query sequence to a database of DNA sequences.
# Algorithm used: Longest Common Substring (LCS)
# - Finds the longest continuous substring shared by two sequences.
# - Runtime: O(n * m), Space: O(n * m)
# It outputs both the similarity score and the matching segment,
# and writes all results to a file. Users get 3 attempts to enter valid filenames.

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
