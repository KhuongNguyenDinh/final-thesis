import numpy as np
import string
import fingerprint

def levenshtein_distance(seq1, seq2):
    seq1 = seq1.lower()
    seq2 = seq2.lower()
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in range(size_x):
        matrix [x, 0] = x
    for y in range(size_y):
        matrix [0, y] = y
    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1)
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + 1,
                    matrix[x-1,y-1] + 1,
                    matrix[x,y-1] + 1)
    return (matrix[size_x - 1, size_y - 1])

class detect_cluster():
        def __init__(self,group):
            self.group = group
          
class knn(detect_cluster):
    def __init__(self, radius, group):
        self.group = group
        self.radius = radius

    def levenshtein(self):
        self.cluster = []
        for i in range(0,len(self.group)-2):
            for j in range(i+1, len(self.group)-2):
                if self.radius >= levenshtein_distance(self.group[i],self.group[j]):
                    self.cluster.append([self.group[i],self.group[j]])
        return self.cluster

    def partial_match(self):
        return "partial match"

class key_collision(detect_cluster):
    def __init__(self, group):
        self.group = group

    def fingerprint(self):
        return fingerprint()

    def ngram_fingerprint(self):
        return "n-gram fingerprint"