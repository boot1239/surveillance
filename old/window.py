import re

from tkinter import BOTH, DISABLED, END, Entry, NORMAL, TclError, Tk
from tkinter.scrolledtext import ScrolledText

from commands import process_command
from constants import *
from helpers import HyperlinkManager


class Screen:
    def __init__(self, args):
        for key, value in vars(args).items():
            setattr(self, key, value)
        self.window = Tk()
        self.__set_fullscreen()
        self.window.title(f'Hacker Console version {CONSOLE_VERSION}')
        self.window.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)

        self.canvas = ScrolledText(self.window, bg=BG_BLACK, fg=FG_GREEN)
        self.canvas.pack(fill=BOTH, expand=True)
        self.hyperlink = HyperlinkManager(self.canvas)
        self.canvas.config(state=DISABLED, font=FONT)

        self.input = Entry(
            self.window, bg=BG_BLACK, fg=FG_GREEN, insertbackground=FG_GREEN
        )
        self.input.pack(fill=BOTH)
        self.input.config(font=FONT)
        self.input.insert(END, 'Enter command..')

        self.on_press_return_id = False
        self.on_press_up_id = False
        self.on_click_placeholder_id = False
        self.input.bind('<FocusIn>', self.__detect_enter_text)
        self.input.bind('<FocusOut>', self.__detect_leave_text)
        self.window.bind('<Escape>', self.__close)

        self.last_inputs = []
        self.last_inputs_pointer = 0

        self.window.mainloop()

    def __close(self, event):
        self.window.destroy()

    def __set_fullscreen(self):
        self.window.attributes('-fullscreen', getattr(self, 'fullscreen'))

    def __on_press_return(self, event):
        if self.on_press_return_id:
            input_text = self.input.get()
            self.last_inputs.append(input_text)
            self.input.delete(0, END)
            self.__process_command(input_text)
            self.last_inputs_pointer = 0

    def __on_press_up(self, event):
        if self.on_press_up_id:
            if self.last_inputs_pointer < len(self.last_inputs):
                self.last_inputs_pointer += 1
                self.input.delete(0, END)
                self.input.insert(
                    END, self.last_inputs[-self.last_inputs_pointer]
                )

    def __on_press_down(self, event):
        if self.on_press_down_id:
            if self.last_inputs_pointer > 1:
                self.last_inputs_pointer -= 1
                self.input.delete(0, END)
                self.input.insert(
                    END, self.last_inputs[-self.last_inputs_pointer]
                )

    def __detect_enter_text(self, event):
        self.input.delete(0, END)
        self.on_press_return_id = self.input.bind(
            '<Return>', self.__on_press_return
        )
        self.on_press_up_id = self.input.bind('<Up>', self.__on_press_up)
        self.on_press_down_id = self.input.bind('<Down>', self.__on_press_down)

    def __detect_leave_text(self, event):
        if self.on_press_return_id:
            try:
                self.input.unbind('<Return>', self.on_press_return_id)
                self.input.unbind('<Up>', self.on_press_up_id)
                self.input.unbind('<Down>', self.on_press_down_id)
                if not self.input.get():
                    self.input.insert(END, 'Enter command..')
                self.on_press_return_id = False
            except TclError:
                pass

    def __process_command(self, command, clicked=False):
        response = process_command(command, clicked=clicked)
        self.__write_to_canvas(**response.__dict__)

    def __write_to_canvas(self, message, clickable=False):
        self.canvas.configure(state=NORMAL)
        words = re.split(r'(\w+)', message)
        for part in words:
            if re.match(r'\w', part) and clickable:
                self.canvas.insert(
                    END, part, self.hyperlink.add(self.__process_command, part)
                )
            else:
                self.canvas.insert(END, part)
        self.canvas.insert(END, f'\n\n')
        self.canvas.yview_moveto(1)
        self.canvas.configure(state=DISABLED)
        self.canvas.update()
