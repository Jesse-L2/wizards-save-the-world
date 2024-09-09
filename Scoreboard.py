class Score:
    def __init__(self, name, score):
        self._name = name
        self._score = score
    def get_name(self):
        return self._name
    def get_score(self):
        return self._score
    def __str__(self):
        return f'{self._name}: {self._score}'

class Scoreboard:
    def __init__(self, capacity=5):
        self._scoreboard = [None] * capacity
        self._n = 0

    def __getitem__(self, elem):
        return self._scoreboard[elem]

    def __setitem__(self, elem, value):
        pass

    def __str__(self):
        return "\n".join(str(self._scoreboard[j]) for j in range(self._n))

    def add(self, entry):
        score = entry.get_score()
        to_add = self._n < len(self._scoreboard) or score > self._scoreboard[-1].get_score()
        if to_add:
            if self._n < len(self._scoreboard):
                self._n += 1
            j = self._n - 1
            while j > 0 and self._scoreboard[j - 1].get_score() < score:
                self._scoreboard[j] = self._scoreboard[j - 1]
                j -= 1
            self._scoreboard[j] = entry
