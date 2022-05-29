class FileMatcher:
    def __init__(self) -> None:
        pass
    
    def _levenshteinDistcance(self, str1: str, str2: str):
        len1 = len(str1)
        len2 = len(str2)
        d = [[0 for j in range(len2 + 1)] for i in range(len1 + 1)]
        for i in range(len1 + 1):
            d[i][0] = i
        for j in range(len2 + 1):
            d[0][j] = j
        for i in range(1, len1 + 1):
            for j in range(1, len2 + 1):
                if str1[i-1] != str2[j-1]:
                    cost = 1
                else:
                    cost = 0
                d[i][j] = min(d[i-1][j]+1, d[i][j-1]+1, d[i-1][j-1]+cost)
        return d[len1][len2]

    def distance(self, filename: str, pattern: str, margin=2):
        len_filename = len(filename)
        len_pattern = len(pattern)
        min_dist = len_filename
        for i in range(len_filename):
            for j in range(len_pattern + margin + 1):
                start = i
                end = i + j if i + j < len_filename else len_filename
                min_dist = min(self._levenshteinDistcance(filename[start:end], pattern), min_dist)
        return min_dist
        

if __name__ == '__main__':
    matcher = FileMatcher()
    print(matcher.distance("batterfly.jpg", "baat"))