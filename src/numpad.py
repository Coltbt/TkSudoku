from tkinter import Frame, Button, Toplevel


class Numpad(Toplevel):

    def __init__(self, parent=None):
        Toplevel.__init__(self)
        self.parent = parent
        self.title("")
        self.resizable(False, False)
        self.buttons = {}

        self.__construct()
        self.protocol("WM_DELETE_WINDOW", self.__close)
        self.attributes('-toolwindow', 1)

    def __construct(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        frame = Frame(self)

        def create_button(i):
            self.buttons[i] = Button(frame, text=str(i),
                                     command=lambda: self.parent.add_value(str(i)),
                                     width=10,
                                     height=2,
                                     font=('Arial', 16))
            self.buttons[i].grid(row=2 - (i - 1) // 3, column=(i - 1) % 3, padx=2, pady=2, sticky='nsew')

        for j in range(1, 10):
            create_button(j)

        frame.grid(row=1, column=1, sticky='nsew', padx=3, pady=3)

    def __close(self):
        self.parent.create_numpad()

    def __bind_events(self):
        pass
