import tkinter as tk
import tkinter.ttk as ttk


class My_Frame(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        self.configure(bg='#444444')

        for key, value in kwargs.items():
            if(key != 'master'):
                self[key] = value

        self.active = False
        self._set_parameters()
        self._create_widgets()

    def _set_parameters(self):
        raise NotImplementedError

    def _create_widgets(self):
        raise NotImplementedError

    def hide_frame(self):
        raise NotImplementedError

    def show_frame(self):
        raise NotImplementedError


class My_Little_Frame(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        self.configure(bg='#444444')

        for key, value in kwargs.items():
            if(key != 'master'):
                self[key] = value


class My_Label_Frame(tk.LabelFrame):
    def __init__(self, *args, **kwargs):
        tk.LabelFrame.__init__(self, *args, **kwargs)

        self.configure(
            bg='#444444', fg='#FF7000',
            font=('Consolas', 15, 'bold')
        )

        for key, value in kwargs.items():
            if(key != 'master'):
                self[key] = value


class My_Label_Frame_Independent(tk.LabelFrame):
    def __init__(self, *args, **kwargs):
        tk.LabelFrame.__init__(self, *args, **kwargs)

        self.configure(
            bg='#444444', fg='#FF7000',
            font=('Consolas', 15, 'bold')
        )

        for key, value in kwargs.items():
            if(key != 'master'):
                self[key] = value

        self.active = False
        self._set_parameters()
        self._create_widgets()

    def _set_parameters(self):
        raise NotImplementedError

    def _create_widgets(self):
        raise NotImplementedError

    def hide_frame(self):
        raise NotImplementedError

    def show_frame(self):
        raise NotImplementedError


class My_Label(tk.Label):
    def __init__(self, *args, **kwargs):
        tk.Label.__init__(self, *args, **kwargs)

        self.configure(
            bg='#444444', fg='#FF8000',
            font=('Consolas', 15, 'bold')
        )

        for key, value in kwargs.items():
            if(key != 'master'):
                self[key] = value


class My_Button(tk.Button):
    def __init__(self, *args, **kwargs):
        tk.Button.__init__(self, *args, **kwargs)

        self.configure(
            bg='#555555', fg='#FF8000', bd=2,
            activebackground='#FF8000', activeforeground='#555555',
            disabledforeground='#222222', font=('Consolas', 15, 'bold'),
            highlightcolor='#DDDDDD', highlightthickness=2,
            justify=tk.CENTER, relief=tk.RIDGE, overrelief=tk.GROOVE,
            cursor='hand2'
        )

        for key, value in kwargs.items():
            if(key != 'master'):
                self[key] = value

    def enable(self):
        self.configure(state=tk.NORMAL, bg='#555555')

    def disable(self):
        self.configure(state=tk.DISABLED, bg='#000000')


class My_Text(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

        self.configure(
            bg='#443344', fg='#FF8000', bd=2,
            font=('Consolas', 15), highlightcolor='#DDDDDD',
            highlightthickness=2, wrap=tk.WORD
        )

        for key, value in kwargs.items():
            if(key != 'master'):
                self[key] = value

    def enable(self):
        self.configure(state=tk.NORMAL)

    def disable(self):
        self.configure(state=tk.DISABLED)


class My_Checkbutton(tk.Checkbutton):
    def __init__(self, *args, **kwargs):
        tk.Checkbutton.__init__(self, *args, **kwargs)

        self.configure(
            bg='#555555', fg='#FF8000', bd=2,
            activebackground='#FF8000', activeforeground='#555555',
            disabledforeground='#222222', font=('Consolas', 15, 'bold'),
            highlightcolor='#DDDDDD', highlightthickness=2,
            justify=tk.CENTER, relief=tk.SUNKEN, cursor='hand2'
        )

        for key, value in kwargs.items():
            if(key != 'master'):
                self[key] = value

    def enable(self):
        self.configure(state=tk.NORMAL, bg='#555555')

    def disable(self):
        self.configure(state=tk.DISABLED, bg='#000000')

    def check(self):
        self.configure(
            bg='#FF8000', fg='#555555',
            activebackground='#555555', activeforeground='#FF8000'
        )

    def uncheck(self):
        self.configure(
            bg='#555555', fg='#FF8000',
            activebackground='#FF8000', activeforeground='#555555'
        )


class My_Treeview(ttk.Treeview):
    def __init__(self, *args, **kwargs):
        ttk.Treeview.__init__(self, *args, **kwargs)

        style = ttk.Style(master=self)
        style.theme_use(themename='clam')
        style.configure(
            style='Treeview', background='#000000', fieldbackground='#000000',
            foreground='#FF8000'
        )
        style.configure(
            style='Treeview.Heading', background='#FF8000',
            foreground='#222222', relief=tk.GROOVE
        )

        for key, value in kwargs.items():
            if(key != 'master'):
                self[key] = value


class My_Progressbar(ttk.Progressbar):
    pass


class My_Scrollbar(tk.Scrollbar):
    def __init__(self, *args, **kwargs):
        tk.Scrollbar.__init__(self, *args, **kwargs)

        self.configure(
            bg='#555555', bd=2, troughcolor='#FF0000', orient=tk.VERTICAL,
            activebackground='#FF8000', elementborderwidth=2,
            highlightcolor='#DDDDDD', highlightthickness=2
        )

        for key, value in kwargs.items():
            if(key != 'master'):
                self[key] = value


if(__name__ == '__main__'):
    root = tk.Tk()
    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)

    # frame = My_Frame(master=root)
    # frame.grid(row=0, column=0, sticky='ENWS')

    label_frame = My_Label_Frame(master=root, text='New Label')
    label_frame.grid(row=0, column=1, sticky='ENWS')

    button = My_Button(master=root, text='Click Me')
    button.grid(row=0, column=0)

    text = My_Text(master=root)
    text.grid(row=1, column=0)

    checkbutton = My_Checkbutton(master=label_frame, text='Checkbutton')
    checkbutton.grid(row=0, column=0)

    scrollbar = My_Scrollbar(master=root)
    scrollbar.grid(row=1, column=1, sticky=tk.NS)

    root.mainloop()