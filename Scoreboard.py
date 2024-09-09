class Scoreboard:
    def __init__(self, capacity=5):
        self._board = [None] * capacity
        self._n = 0

    def __getitem__(self, elem):
        return self._board[elem]

    def __setitem__(self, elem, value):
        pass

    def __str__(self):
        return "\n".join(str(self._board[j]) for j in range(self._n))

    def add(self, entry):

        score = entry.get_score()
        to_add = self._n < len(self._board) or score > self._board[-1].get_score()
        if to_add:
            if self._n < len(self._board):
                self._n += 1
            j = self._n - 1
            while j > 0 and self._board[j - 1].get_score() < score:
                self._board[j] = self._board[j - 1]
                j -= 1
            self._board[j] = entry
