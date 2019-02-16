import tkinter as tk

import my_widgets


class Test_Info(tk.Toplevel):
    def __init__(self, master, method_info, *args, **kwargs):
        tk.Toplevel.__init__(self, master=master, *args, **kwargs)
        self.grab_set()
        self.method_info = method_info

        self._set_parameters()
        self._create_widgets()

    def _set_parameters(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.configure(bg='#444444')
        if(self.method_info['result'] is True):
            self.title(self.method_info['method'] + '    ~    PASS')
        else:
            error_info = str()
            if(self.method_info['failure_text'] is not None):
                error_info = self.method_info['failure_text'].split('\n')
            elif(self.method_info['error_text'] is not None):
                error_info = self.method_info['error_text'].split('\n')
            self.title(
                self.method_info['method'] + '    ~    ' + error_info[-2]
            )

    def _create_widgets(self):
        self.text = my_widgets.My_Text(master=self)
        self.text.grid(row=0, column=0, sticky=tk.NSEW)

        self.scrollbar_vert = my_widgets.My_Scrollbar(
            master=self, command=self.text.yview,
            orient=tk.VERTICAL, cursor='sb_v_double_arrow'
        )
        self.scrollbar_vert.grid(row=0, column=1, sticky=tk.NS, pady=1)

        info = 'Module: {:s}\n'.format(
            self.method_info['module'].split('*')[-1]
        )
        info += 'Class: {:s}\n'.format(self.method_info['class'])
        info += 'Method: {:s}\n'.format(self.method_info['method'])
        if(self.method_info['result'] is True):
            info += 'Execution time: {:.3f}\n'.format(self.method_info['time'])
            info += '\nDocumentation:\n{:s}'.format(self.method_info['doc'])
            self.text.insert('0.0', info, tk.END)
            self.text.set_bg_pass()
        else:
            if(self.method_info['failure_text'] is not None):
                info += self.method_info['failure_text']
                self.text.set_bg_failure()
            elif(self.method_info['error_text'] is not None):
                info += self.method_info['error_text']
                self.text.set_bg_error()
            self.text.insert('0.0', info, tk.END)

        self.text.disable()
        self.text.configure(yscrollcommand=self.scrollbar_vert.set)
