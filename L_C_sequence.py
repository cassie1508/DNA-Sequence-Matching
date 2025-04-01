def longest_common_sequence(X, Y):
    m = len(X)
    n = len(Y)

    LCS = [[0 for i in range(n + 1)] for j in range(m + 1)]
    for i in range(m+1): 
        for j in range(n+1):  
            if i== 0 or  j == 0:
                LCS[i][j] = 0
            elif X[i-1] == Y[j-1]:
                LCS[i][j] = 1 + LCS[i-1][j-1]
            else: 
                LCS[i][j] = max(LCS[i-1][j], LCS[i][j-1])
    i, j = m, n
    lcs_items = []
    while i > 0 and j > 0:
        if X[i-1] == Y[j-1]:
            lcs_items.append(X[i-1])
            i -= 1
            j -= 1
        elif LCS[i-1][j] > LCS[i][j-1]:
            i -= 1
        else:
            j -= 1
    lcs_items.reverse()
    lcs_string = ''.join(lcs_items)
 
    
    return lcs_string

print(longest_common_sequence("ACADB", "CBDA"))
