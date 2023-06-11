class BoyerMoore:

    def compute_bad_character_table(self, pattern):
        m = len(pattern)
        bad_character = {}

        for i in range(m - 1):
            bad_character[pattern[i]] = i

        return bad_character

    def compute_good_suffix_table(self, pattern):
        m = len(pattern)
        good_suffix = [0] * (m + 1)
        border = [0] * (m + 1)
        j = m

        for i in range(m, -1, -1):
            if j == m:
                border[i] = j
            else:
                if pattern[i] != pattern[j]:
                    border[i] = j
                else:
                    border[i] = border[j]

            j = border[i]

        for i in range(m):
            good_suffix[i] = m - border[i]

        return good_suffix

    def boyer_moore_search(self, text, pattern):
        n = len(text)
        m = len(pattern)
        bad_character = self.compute_bad_character_table(pattern)
        good_suffix = self.compute_good_suffix_table(pattern)
        i = j = 0

        while i <= n - m:
            j = m - 1

            while j >= 0 and text[i + j] == pattern[j]:
                j -= 1

            if j == -1:
                return True  # Pola ditemukan
            else:
                bad_character_shift = j - bad_character.get(text[i + j], -1)
                good_suffix_shift = good_suffix[j + 1]
                i += max(bad_character_shift, good_suffix_shift)

        return False  # Pola tidak ditemukan

    def detect_patterns(self, text, pattern_list):
        detected_patterns = []

        for pattern_data in pattern_list:
            pattern_syntax = pattern_data['pattern_syntax']
            pattern_name = pattern_data['pattern_name']

            patterns = pattern_syntax.split('|')

            for pattern in patterns:
                if self.boyer_moore_search(text, pattern):
                    detected_patterns.append(pattern_name)
                    break

        return detected_patterns


BM = BoyerMoore()

# Contoh penggunaan
text = "select * FROM users; drop TABLE users;"
pattern_list = [{'pattern_syntax': 'select|insert|update|delete|drop|create|alter', 'pattern_name': 'sqli'},
                {'pattern_syntax': 'drop', 'pattern_name': 'ddos'}]


detected_patterns = BM.detect_patterns(text, pattern_list)

if detected_patterns:
    print("Pola-pola yang terdeteksi:", detected_patterns)
else:
    print("Tidak ada pola yang terdeteksi")
