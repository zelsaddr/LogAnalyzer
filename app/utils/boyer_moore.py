class BoyerMoore:

    def compute_bad_character_table(self, pattern):
        m = len(pattern)
        bad_character = {}

        for i in range(m - 1):
            bad_character[pattern[i]] = i

        return bad_character

    def boyer_moore_search(self, text, pattern):
        n = len(text)
        m = len(pattern)
        bad_character = self.compute_bad_character_table(pattern)
        i = 0

        while i <= n - m:
            j = m - 1

            while j >= 0 and text[i + j].lower() == pattern[j].lower():
                j -= 1

            if j == -1:
                return True  # Pola ditemukan
            else:
                bad_character_shift = j - \
                    bad_character.get(text[i + j].lower(), -1)
                i += max(1, bad_character_shift)

        return False  # Pola tidak ditemukan

