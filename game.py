class Case:
    MAX_ABCISS = 10
    MAX_ORDINATE = 10

    def __init__(self, down_left_corner_absciss, down_left_corner_ordinate) -> None:
        self.down_left_corner_absciss = down_left_corner_absciss
        self.down_left_corner_ordinate = down_left_corner_ordinate

    @classmethod
    def create_grid(self):
        for abciss in range(self.MAX_ABCISS):
            for ordinate in range(self.MAX_ORDINATE):
                case = Case(abciss, ordinate)

