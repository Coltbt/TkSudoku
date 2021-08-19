from gridRenderer import GridRenderer


class Grid:

    def __init__(self, renderer: GridRenderer):
        """
        This object represents a sudoku sudoku. This is basically both the model (a container for data) and the controller.
        """
        self.grid = dict()
        self.renderer = renderer
        self.renderer.sudoku = self
        self.loaded = False
        self.selected_coords = (0, 0)

        for i in range(9):
            for j in range(9):
                self.grid[(i, j)] = '.'

        self.sudoku = self.grid.copy()

    def load(self, fp, line=0):
        """
        Load a sudoku from a txt file.

        A sudoku is represented in line as follows :
        ...61......3.57....578.........6..7..76134..2.....5...6.5.7..18..24...6..3..8..4.
        for the following sudoku (a point is an empty cell) :

         . . . | 6 1 . | . . .\n
         . . 3 | . 5 7 | . . .\n
         . 5 7 | 8 . . | . . .\n
        -----------------------.\n
         . . . | . 6 . | . 7 .\n
         . 7 5 | 1 3 4 | . . 2\n
         . . . | . . 5 | . . .\n
        -----------------------.\n
         6 . 5 | . 7 . | . 1 8\n
         . . 2 | 4 . . | . 6 .\n
         . 3 . | . 8 . | . 4 .\n

        :param fp: filepath
        :param line: line where the sudoku data is
        :return: True if successfully loaded, else False
        """
        loaded = False
        try:
            file = open(fp, 'r')
            data = file.readlines()[line]
            self.__reset()
            for i in range(9):
                for j in range(9):
                    cell = data[i * 9 + j]
                    self.change(i, j, cell, True)

            self.loaded = True
            loaded = True

        except FileNotFoundError:
            print(f"File {fp} not found.\n\t")

        return loaded

    def change(self, line, column, value, original=False):
        """
        Change the digit of a cell
        """
        if original:
            self.sudoku[(line, column)] = value

        if not original and self.sudoku[(line, column)] != '.':
            return

        if not self.__is_valid(line, column, value):
            return
        self.grid[(line, column)] = value

        if value == '.':
            self.renderer.change(line, column, ' ', original)
        else:
            self.renderer.change(line, column, value, original)

        if self.__is_full():
            self.win()

    def remove(self, line, column):
        """
        Make a cell empty
        """
        if self.grid[(line, column)] == '.':
            return
        self.grid[(line, column)] = '.'
        self.renderer.change(line, column, ' ')

    def get(self, line, column):
        """
        Get the digit in a cell
        """
        return self.grid[(line, column)] if self.grid[(line, column)] != '.' else ' '

    def select(self, line, column):
        self.selected_coords = (line, column)
        self.renderer.change_select(self.selected_coords)

    def win(self):
        self.renderer.parent.win()

    def __is_full(self):
        """
        Check if the sudoku is full (→ WIN)

        :return: True if full, otherwise False
        """
        full = True
        for i in range(9):
            for j in range(9):
                if self.grid[(i, j)] == '.':
                    full = False
                    break
            if not full:
                break

        return full

    def __is_valid(self, line, column, value):
        """
        Check if the emplacement of a digit in a cell is possible

        :return: True if valid, otherwise False
        """
        # Check in lines
        for i in range(9):
            if i != line:
                if self.grid[(i, column)] == value:
                    return False

        # Check in columns
        for i in range(9):
            if i != column:
                if self.grid[(line, i)] == value:
                    return False

        # Check in cases
        # First find the case
        # Then go iter through it as for lines and columns
        case = (
            line // 3,
            column // 3
        )

        for i in range(9):
            x, y = case[0] * 3 + i // 3, case[1] * 3 + i % 3
            if x != line or y != column:
                if self.grid[(x, y)] == value:
                    return False

        return True

    def __reset(self):
        """
        Empty all the cells
        """
        for i in range(9):
            for j in range(9):
                self.remove(i, j)
