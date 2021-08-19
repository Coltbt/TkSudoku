from tkinter import Canvas, Tk
import tkinter.font as tk_font


class GridRenderer(Canvas):

    def __init__(self, parent=None, *args, **kwargs):
        """
        This object is a Canvas that renders a sudoku Grid
        """
        Canvas.__init__(self, parent, *args, **kwargs)

        self.first_x, self.first_y = 0, 0
        self.cell_size = 0
        self.font = tk_font.Font(family="Arial", size=16)
        self.sudoku = None
        self.elements = {}
        self.selected_coords = [0, 0]
        self.selected_id = None

        self.bind('<Configure>', self.update)
        for i in range(9):
            for j in range(9):
                self.elements[(i, j)] = None

    def _draw_grid(self):
        """
        Draw sudoku lines
        """
        end_x, end_y = self.first_x + 9 * self.cell_size, self.first_y + 9 * self.cell_size

        # Draw horizontal lines
        for i in range(10):
            if i % 3 == 0:
                horizontal_width = 3
            else:
                horizontal_width = 1

            self.create_line(self.first_x, self.first_y + i * self.cell_size,
                             end_x, self.first_y + i * self.cell_size,
                             width=horizontal_width, capstyle='round')

        # Draw vertical lines
        for i in range(10):
            if i % 3 == 0:
                vertical_width = 3
            else:
                vertical_width = 1

            self.create_line(self.first_x + i * self.cell_size, self.first_y,
                             self.first_x + i * self.cell_size, end_y,
                             width=vertical_width, capstyle='round', tag='grid')

    def _load_grid(self):
        """
        Redraw the sudoku numbers
        """
        if self.sudoku is None:
            return

        for i in range(9):
            for j in range(9):
                cell = self.sudoku.grid[(i, j)]
                if cell != '.':
                    original = self.sudoku.sudoku[(i, j)] != '.'
                    self.change(i, j, cell, original)

    def _draw_selected(self):
        borderwidth = self.cell_size // 40 if self.cell_size > 40 else 1

        x = self.first_x + self.cell_size * self.selected_coords[0]
        y = self.first_y + self.cell_size * self.selected_coords[1]

        if self.selected_id is not None:
            self.delete(self.selected_id)

        self.selected_id = self.create_rectangle(x + borderwidth / 2, y + borderwidth / 2,
                                                 x + self.cell_size - borderwidth/2, y + self.cell_size - borderwidth/2,
                                                 fill='#b0f8f8', width=borderwidth, outline='#88c0ff')
        self.tag_lower(self.selected_id, 'text')
        self.tag_lower(self.selected_id, 'grid')

    def update(self, event):
        """
        Update draw and variables when Canvas is resized or placed for the first time
        """
        # We don't want a too small grid
        if event.width < 100 or event.height < 100:
            return

        # Make tkinter.Canvas update
        Canvas.update(self)

        # Update variables
        width, height = self.winfo_width() - 4, self.winfo_height() - 4
        self.cell_size = min(width, height) // 9
        self.first_x = width / 2 - 4.5 * self.cell_size
        self.first_y = 2 + height / 2 - 4.5 * self.cell_size
        self.font.config(size=int(self.cell_size / 1.5))

        # Reset and redraw all
        self.reset()
        self._draw_grid()
        self._load_grid()
        self._draw_selected()

    def change(self, line, column, value, original=False):
        """
        Write a digit
        """

        if value == '.':
            return self.remove(line, column)

        if original:
            color = 'black'
        else:
            color = "#606060"

        if self.elements[line, column] is not None:
            self.remove(line, column)

        x = self.first_x + self.cell_size * (0.5 + line)
        y = self.first_y + self.cell_size * (0.5 + column)
        self.elements[(line, column)] = self.create_text(x, y, text=value, font=self.font, tag='text', fill=color)

    def remove(self, line, column):
        """
        Empty a cell
        """
        self.delete(self.elements[(line, column)])

    def reset(self):
        """
        Empty all cells
        """
        self.delete("all")
        self._draw_grid()

    def change_select(self, selected_coords):
        self.selected_coords = selected_coords
        self._draw_selected()


if __name__ == '__main__':
    root = Tk()
    GridRenderer().pack(fill='both', expand=True)
    root.mainloop()
