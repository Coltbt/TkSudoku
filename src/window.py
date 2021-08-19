from grid import Grid, GridRenderer
from vector import *
from tkinter import Tk, Menu, Frame, Button, Label, filedialog, messagebox, Toplevel
from numpad import Numpad
import os
from PIL import Image, ImageTk


class Window(Tk):

    def __init__(self, book, *args, **kwargs):
        """
        Main Window of the Sudoku game
        :param args: args to pass to tkinter.Tk
        :param kwargs: kwargs to pass to tkinter.Tk
        """
        Tk.__init__(self, *args, **kwargs)

        self.numpad = None
        self.book = book
        file = open(book, 'r')
        self.book_length = len(file.readlines())
        file.close()
        self.line = 0

        self.title("Sudoku")
        self.minsize(475, 250)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=1)

        self.sudoku = Grid(GridRenderer(self))
        self.sudoku.renderer.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)

        self.__create_menu_bar()

        frame = Frame(self)

        frame.rowconfigure(2, weight=1)
        frame.rowconfigure(6, weight=1)
        frame.columnconfigure(2, weight=1)

        self.book_label = Label(frame, width=10, font=('Arial', 24, 'bold'),
                                text=os.path.splitext(os.path.basename(self.book))[0])

        level_frame = Frame(frame)
        self.level = Label(level_frame, width=3, font=('Arial', 16))

        left_photo = Image.open("../assets/images/left_arrow.png").resize((32, 32), Image.ANTIALIAS)
        left_arrow = ImageTk.PhotoImage(left_photo)
        left_button = Button(level_frame, image=left_arrow, command=self.__load_previous)
        left_button.image = left_arrow

        right_photo = Image.open("../assets/images/right_arrow.png").resize((32, 32), Image.ANTIALIAS)
        right_arrow = ImageTk.PhotoImage(right_photo)
        right_button = Button(level_frame, image=right_arrow, command=self.__load_next)
        right_button.image = right_arrow

        self.book_label.grid(row=0, column=0, columnspan=2)
        left_button.grid(row=1, column=0)
        self.level.grid(row=1, column=1)
        right_button.grid(row=1, column=2)
        level_frame.grid(row=1, column=0, columnspan=2)

        self.num_button = Button(frame, text='numpad', command=self.create_numpad, bg='#c0c0c0', font=('Arial', 16),
                                 width=10)
        self.num_button.grid(row=3, column=0, pady=2, columnspan=2)
        Button(frame, text='Erase', command=self.delete_value, bg='#f05050', font=('Arial', 16), width=10). \
            grid(row=4,
                 column=0,
                 pady=2,
                 columnspan=2)

        frame.grid(row=1, column=2, padx=5, pady=5, sticky='nsew')

        self.__bind_events()
        self.load_grid(self.book, self.line)

    def __bind_events(self):
        """
        Bind tkinter events for the Window class
        """
        # Bind selections
        self.sudoku.renderer.bind('<Button-1>', self.select)
        self.bind('<Left>', lambda e: self.move_selection(-1, 0))
        self.bind('<Right>', lambda e: self.move_selection(1, 0))
        self.bind('<Down>', lambda e: self.move_selection(0, -1))
        self.bind('<Up>', lambda e: self.move_selection(0, 1))

        # Bind num events
        self.bind('1', lambda e: self.add_value('1'))
        self.bind('2', lambda e: self.add_value('2'))
        self.bind('3', lambda e: self.add_value('3'))
        self.bind('4', lambda e: self.add_value('4'))
        self.bind('5', lambda e: self.add_value('5'))
        self.bind('6', lambda e: self.add_value('6'))
        self.bind('7', lambda e: self.add_value('7'))
        self.bind('8', lambda e: self.add_value('8'))
        self.bind('9', lambda e: self.add_value('9'))

        # Bind delete
        self.bind('<Delete>', lambda e: self.delete_value())

    def __create_menu_bar(self):
        menu_bar = Menu(self, tearoff=0)

        menu_file = Menu(menu_bar, tearoff=0)
        menu_file.add_command(label="Load", command=self.load)
        menu_file.add_separator()
        menu_file.add_command(label="Quit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=menu_file)

        menu_help = Menu(menu_bar, tearoff=0)
        menu_help.add_command(label="Keymap", command=self.keymap)
        menu_help.add_command(label="Rules", command=self.rules)
        menu_help.add_command(label="About", command=self.about)
        menu_bar.add_cascade(label="Help", menu=menu_help)

        self.config(menu=menu_bar)

    def __load_next(self):
        self.line = (self.line + 1) % self.book_length
        self.load_grid(self.book, self.line)

    def __load_previous(self):
        self.line = (self.line - 1) % self.book_length
        self.load_grid(self.book, self.line)

    def create_numpad(self):
        if self.numpad is not None:
            self.numpad.destroy()
            self.num_button.configure(bg='#c0c0c0')
            self.numpad = None
        else:
            self.numpad = Numpad(self)
            self.num_button.configure(bg='#b0f8f8')

    def load(self):
        filename = self.select_file()
        self.load_grid(filename, 0)
        self.line = 0
        self.book = filename
        self.book_label.configure(text=os.path.splitext(os.path.basename(self.book))[0])

    def load_grid(self, fp, line):
        if self.sudoku.load(fp, line % self.book_length):
            self.level.configure(text=str(self.line))

    def select(self, event):
        line = (event.x - self.sudoku.renderer.first_x) // self.sudoku.renderer.cell_size
        column = (event.y - self.sudoku.renderer.first_y) // self.sudoku.renderer.cell_size
        if min(line, column) < 0 or max(line, column) > 8:
            return
        self.sudoku.select(line, column)

    def move_selection(self, dx, dy):
        self.select(Vector(
            ((self.sudoku.selected_coords[0] + dx) % 9) * self.sudoku.renderer.cell_size + self.sudoku.renderer.first_x,
            ((self.sudoku.selected_coords[1] - dy) % 9) * self.sudoku.renderer.cell_size + self.sudoku.renderer.first_y
        ))

    def add_value(self, value):
        self.sudoku.change(*self.sudoku.selected_coords, value)

    def delete_value(self):
        if self.sudoku.sudoku[self.sudoku.selected_coords] == '.':
            self.sudoku.remove(*self.sudoku.selected_coords)

    def keymap(self):
        keymap = Toplevel(self)
        keymap.title("Keymap")
        keymap.resizable(False, False)
        keymap.attributes('-toolwindow', 1)

        Label(keymap,
              text="<1 - 9>\t\tInsert digit\n"
                   "<Left>\t\tMove selection left\n"
                   "<Right>\t\tMove selection right\n"
                   "<Up>\t\tMove selection up\n"
                   "<Down>\t\tMove selection down\n"
                   "<Delete>\tDelete cell content\n"
                   "Left click\t\tSelect cell",
              justify="left").pack(padx=5, pady=5)

    def rules(self):
        rules = Toplevel(self)
        rules.title("Rules")
        rules.resizable(False, False)
        rules.attributes('-toolwindow', 1)

        Label(rules,
              text="Sudoku is a puzzle based on a small number of very simple rules:\n\n"
                   "\t- Every square has to contain a single number\n"
                   "\t- Only the numbers from 1 through to 9 can be used\n"
                   "\t- Each 3×3 box can only contain each number from 1 to 9 once\n"
                   "\t- Each vertical column can only contain each number from 1 to 9 once\n"
                   "\t- Each horizontal row can only contain each number from 1 to 9 once",
              justify='left').pack(padx=5, pady=5)

    def about(self):
        about = Toplevel(self)
        about.title("Rules")
        about.resizable(False, False)
        about.attributes('-toolwindow', 1)

        Label(about,
              text="Sudoku built with tkinter and Python 3.\n"
                   "This is a personnal exercise.").pack(padx=5, pady=5)

    @staticmethod
    def win():
        messagebox.showinfo(title="Game", message="You won !")

    @staticmethod
    def select_file():
        filetypes = (
            ('text files', '*.txt'),
            ('All files', '*.*')
        )

        filename = filedialog.askopenfilename(
            title='Open a file',
            initialdir=os.path.abspath("../assets/books"),
            filetypes=filetypes)

        return filename
