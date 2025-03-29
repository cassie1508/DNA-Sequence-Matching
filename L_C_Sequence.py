def longest_common_sequence(X, Y):
    m = len(X)
    n = len(Y)
    LCS = [[0 for i in range(m + 1)] for j in range(n + 1)]
    print(LCS)
    
    for i in range(1, m+1):  
        # print("i-1", i-1)
        for j in range(1, n+1):  
            #print("j-1", j-1)
            # print (X[i-1], Y[j-1])
            if X[i-1] == Y[j-1]:
                print("i", i, "j", j)
                print (LCS[j][i])
                LCS[i][j] = 1 + LCS[i-1][j-1]

        #         #if the characters are the same, add 1 to the previous diagonal value
            else:
                print("i-1", i-1 , "j", j)
                LCS[i][j] = max(LCS[i-1][j], LCS[i][j-1])

    print(LCS)
    return LCS

longest_common_sequence("AGGTAB", "GXTXAYB")