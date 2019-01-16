'''
TODO:

    * logowanie
    * zarzadzanie datami
    * testowanie
    * zarzadanie folderami
    * plik konfiguracyjny
'''

import unittest
import threading
import os

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter import filedialog

import my_widgets
import linker
import test_detector
import files_creator


def loading_cursor(method):
    def wrapper(master, *args, **kwargs):
        master.configure(cursor='clock')
        master.update()
        ret = method(master, *args, **kwargs)
        master.configure(cursor='arrow')
        return ret
    return wrapper


class Frame_Program_Title(my_widgets.My_Frame):
    def __init__(self, *args, **kwargs):
        my_widgets.My_Frame.__init__(self, *args, **kwargs)

    def _set_parameters(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def _create_widgets(self):
        self.label_title = my_widgets.My_Label(
            master=self, text='PyEasyTesting',
            font=('Consolas', 25, 'bold', 'italic')
        )
        self.label_title.grid(
            row=0, column=0, sticky=tk.NSEW, padx=100, pady=30
        )


class Frame_Main_Menu(my_widgets.My_Label_Frame_Independent):
    def __init__(self, *args, **kwargs):
        my_widgets.My_Label_Frame_Independent.__init__(
            self, *args, text='Main Menu'
        )

    def _set_parameters(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)

    def _create_widgets(self):
        self.button_loading = my_widgets.My_Button(
            master=self, text='Loading'
        )
        self.button_loading.grid(
            row=1, column=0, sticky=tk.NSEW, padx=10, pady=10
        )

        self.button_testing = my_widgets.My_Button(
            master=self, text='Testing'
        )
        self.button_testing.grid(
            row=2, column=0, sticky=tk.NSEW, padx=10, pady=10
        )


class Empty_Frame(my_widgets.My_Frame):
    def __init__(self, *args, **kwargs):
        my_widgets.My_Frame.__init__(self, *args, **kwargs)

    def _set_parameters(self):
        pass

    def _create_widgets(self):
        pass

    def hide_frame(self):
        pass

    def show_frame(self):
        pass


class Frame_Loading(my_widgets.My_Label_Frame_Independent):
    def __init__(self, *args, **kwargs):
        my_widgets.My_Label_Frame_Independent.__init__(
            self, *args, text='LOADING'
        )
        self.directory = None
        self.files_register = dict()
        self.test_detector = test_detector.Test_Detector()

        self.__update = False
        self.__update_frame()

    def _set_parameters(self):
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=0)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

    def _create_widgets(self):
        self.button_get_path = my_widgets.My_Button(
            master=self, text='Tests folder', command=self.__find_directory
        )
        self.button_get_path.grid(row=0, column=0, padx=(10, 5), pady=(10, 5))

        self.button_scan_for_tests = my_widgets.My_Button(
            master=self, text='Scan for tests', state=tk.DISABLED,
            command=self.__scan_for_test_files
        )
        self.button_scan_for_tests.grid(
            row=0, column=1, padx=5, pady=(10, 5)
        )

        self.button_save = my_widgets.My_Button(
            master=self, text='Save test files', state=tk.DISABLED,
            command=self.__save_project
        )
        self.button_save.grid(row=0, column=2, padx=(5, 10), pady=(10, 5))

        self.label_directory = my_widgets.My_Label(
            master=self, text='Directory:\n', relief=tk.GROOVE
        )
        self.label_directory.grid(
            row=1, column=0, columnspan=3, sticky=tk.NSEW, padx=10, pady=5
        )

        self.tree_frame = my_widgets.My_Little_Frame(master=self)
        self.tree_frame.rowconfigure(0, weight=1)
        self.tree_frame.rowconfigure(1, weight=0)
        self.tree_frame.columnconfigure(0, weight=1)
        self.tree_frame.columnconfigure(1, weight=0)
        self.tree_frame.grid(
            row=2, column=0, columnspan=3,
            sticky=tk.NSEW, padx=10, pady=(5, 10)
        )
        self.tree_files = my_widgets.My_Treeview(
            master=self.tree_frame, columns=('Directory', 'Test', 'ID'),
            selectmode='extended'
        )
        self.tree_files.bind('<<TreeviewSelect>>', self.__on_lmb_click)
        self.tree_files.heading('#0', text='Directory', anchor=tk.CENTER)
        self.tree_files.heading('#1', text='Test', anchor=tk.CENTER)
        self.tree_files.column('#0', stretch=tk.YES, minwidth=50)
        self.tree_files.column('#1', stretch=tk.YES, minwidth=50)
        self.tree_files.grid(row=0, column=0, sticky=tk.NSEW)

        self.scrollbar_vert = my_widgets.My_Scrollbar(
            master=self.tree_frame, command=self.tree_files.yview,
            orient=tk.VERTICAL, cursor='sb_v_double_arrow'
        )
        self.scrollbar_vert.grid(row=0, column=1, sticky=tk.NS)

        self.scrollbar_hor = my_widgets.My_Scrollbar(
            master=self.tree_frame, command=self.tree_files.xview,
            orient=tk.HORIZONTAL, cursor='sb_h_double_arrow'
        )
        self.scrollbar_hor.grid(row=1, column=0, sticky=tk.EW)

        self.tree_files.configure(yscrollcommand=self.scrollbar_vert.set)
        self.tree_files.configure(xscrollcommand=self.scrollbar_hor.set)

        self.frame_info = my_widgets.My_Label_Frame(master=self, text='INFO')
        self.frame_info.columnconfigure(0, weight=1)
        self.frame_info.columnconfigure(1, weight=1)
        self.frame_info.columnconfigure(2, weight=1)
        self.frame_info.columnconfigure(3, weight=1)
        self.frame_info.columnconfigure(4, weight=1)
        self.frame_info.columnconfigure(5, weight=1)
        self.frame_info.grid(
            row=3, column=0, columnspan=3, sticky=tk.NSEW, padx=5, pady=5
        )
        self.info1 = my_widgets.My_Label(
            master=self.frame_info, relief=tk.GROOVE, font=('Consolas', 10),
            text='Test found', bg='#005500'
        )
        self.info1.grid(row=0, column=0, sticky=tk.NSEW)
        self.info2 = my_widgets.My_Label(
            master=self.frame_info, relief=tk.GROOVE, font=('Consolas', 10),
            text='Test not found', bg='#770022'
        )
        self.info2.grid(row=0, column=1, sticky=tk.NSEW)
        self.info3 = my_widgets.My_Label(
            master=self.frame_info, relief=tk.GROOVE, font=('Consolas', 10),
            text='Test by user', bg='#008800'
        )
        self.info3.grid(row=0, column=2, sticky=tk.NSEW)
        self.info4 = my_widgets.My_Label(
            master=self.frame_info, relief=tk.GROOVE, font=('Consolas', 10),
            text='Not test by user', bg='#DD0044'
        )
        self.info4.grid(row=0, column=3, sticky=tk.NSEW)
        self.info5 = my_widgets.My_Label(
            master=self.frame_info, relief=tk.GROOVE, font=('Consolas', 10),
            text='Cannot scan', bg='#0000AA'
        )
        self.info5.grid(row=0, column=4, sticky=tk.NSEW)
        self.info6 = my_widgets.My_Label(
            master=self.frame_info, relief=tk.GROOVE, font=('Consolas', 10),
            text='Not \'Python\' file', bg='#000000'
        )
        self.info6.grid(row=0, column=5, sticky=tk.NSEW)

    def __update_frame(self):
        if(self.directory is None):
            self.button_scan_for_tests.configure(state=tk.DISABLED)
            self.button_save.configure(state=tk.DISABLED)
        else:
            self.button_scan_for_tests.configure(state=tk.NORMAL)
            self.button_save.configure(state=tk.NORMAL)
        if(self.__update is True):
            self.after(40, self.__update_frame)

    def __find_directory(self):
        self.directory = filedialog.askdirectory()
        if(self.directory == ''):
            self.directory = None
        else:
            self.label_directory.configure(
                text='Directory:\n{:s}'.format(self.directory)
            )
            self.__start_filling_process()

    @loading_cursor
    def __start_filling_process(self):
        last_folder = files_creator.get_file_from_path(path=self.directory)
        self.tree_files.insert(
            parent='', index=tk.END, iid=last_folder,
            text=last_folder, values=('', ), tags=(last_folder, )
        )
        self.files_register[last_folder] = self.directory
        self.__fill_tree(path=self.directory, root=last_folder)

    def __fill_tree(self, path, root):
        files = os.listdir(path)
        for _file in files:
            new_path = os.path.join(path, _file)
            new_root = root + '-' + _file
            self.files_register[new_root] = new_path
            if(os.path.isfile(new_path)):
                self.tree_files.insert(
                    parent=root, index=tk.END, iid=new_root,
                    text=_file, values=('', ), tags=(new_root, )
                )
            elif(os.path.isdir(new_path)):
                self.tree_files.insert(
                    parent=root, index=tk.END, iid=new_root,
                    text=_file, values=('', ), tags=(new_root, )
                )
                self.__fill_tree(path=new_path, root=new_root)

    @loading_cursor
    def __scan_for_test_files(self):
        tests_counter = 0
        none_tests_counter = 0
        failed_tests_counter = 0
        other_counter = 0
        for key, file_path in self.files_register.items():
            result = self.test_detector.is_test_file(module_path=file_path)
            if(result is True):
                self.tree_files.tag_configure(
                    tagname=key, background='#005500'
                )
                self.tree_files.item(item=key, values=(True, ))
                tests_counter += 1
            elif(result is False):
                self.tree_files.tag_configure(
                    tagname=key, background='#770022'
                )
                self.tree_files.item(item=key, values=(False, ))
                none_tests_counter += 1
            elif(result is None):
                self.tree_files.item(item=key, values=('', ))
                other_counter += 1
            elif(type(result) == str and result == 'FAILED'):
                self.tree_files.tag_configure(
                    tagname=key, background='#0000AA'
                )
                failed_tests_counter += 1
            else:
                messagebox.showwarning('WARNING', 'Directory scan failed.')
        else:
            m = 'Scan completed.'
            m += '\nFound {:n} proper test files.'.format(tests_counter)
            m += '\nFound {:n} \'Python\' files without tests.'.format(
                none_tests_counter
            )
            m += '\nFound {:n} files, that failed to load.'.format(
                failed_tests_counter
            )
            m += '\nFound {:n} other files and directories.'.format(
                other_counter
            )
            messagebox.showinfo('SUCCES', m)

    def __on_lmb_click(self, event):
        item = self.tree_files.selection()[0]
        item_children = self.tree_files.get_children(item=item)
        if(
            len(item_children) == 0 and
            self.test_detector.is_python_module(module_name=item)
           ):
            is_test = self.tree_files.item(item)['values'][0]
            if(is_test == 'True'):
                self.tree_files.tag_configure(
                    tagname=item, background='#DD0044'
                )
                self.tree_files.item(item=item, values=(False, ))
            elif(is_test == 'False' or is_test == ''):
                self.tree_files.tag_configure(
                    tagname=item, background='#008800'
                )
                self.tree_files.item(item=item, values=(True, ))

    def __get_only_tests(self, parent, register):
        children = self.tree_files.get_children(item=parent)
        for child in children:
            grand_children = self.tree_files.get_children(item=child)
            if(len(grand_children) == 0):
                is_test = self.tree_files.item(child)['values'][0]
                if(is_test == 'True'):
                    register[child] = self.files_register[child]
            else:
                self.__get_only_tests(parent=child, register=register)

    def __save_project(self):
        last_folder = files_creator.get_file_from_path(path=self.directory)
        register = dict()
        self.__get_only_tests(parent=last_folder, register=register)
        files_creator.save_project(
            project_name=last_folder, tests_paths=register
        )

    def hide_frame(self):
        self.__update = False

    def show_frame(self):
        self.__update = True
        self.__update_frame()


class Frame_Testing(my_widgets.My_Label_Frame_Independent):
    def __init__(self, *args, **kwargs):
        my_widgets.My_Label_Frame_Independent.__init__(
            self, *args, text='TESTING'
        )

    def _set_parameters(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def _create_widgets(self):
        self.btn = my_widgets.My_Button(
            master=self, text='TESTTING'
        )
        self.btn.grid(row=0, column=0)

    def hide_frame(self):
        pass

    def show_frame(self):
        pass


class PyEasyTesting_Window(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.__frames = {
            'EMPTY': Empty_Frame(),
            'LOADING': Frame_Loading(),
            'TESTING': Frame_Testing(),
        }

        self._set_parameters()
        self.__create_static_frames()
        self.__program_buttons()
        self.__add_events()
        self.__frame_changer()
        self.mainloop()

    def _set_parameters(self):
        self.configure(bg='#222222')
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=5)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=5)

    def __create_static_frames(self):
        self.frame_title = Frame_Program_Title()
        self.frame_title.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW)

        self.frame_main_menu = Frame_Main_Menu()
        self.frame_main_menu.grid(row=1, column=0, sticky=tk.NSEW)

        self.__frames['EMPTY'].active = True

    def __change_frame(self, frame_name):
        for key in self.__frames:
            if(key == frame_name):
                self.__frames[key].active = True
            else:
                self.__frames[key].active = False
        self.__frame_changer()

    def __frame_changer(self):
        for frame_name, frame in self.__frames.items():
            if(frame.active):
                self.__frames[frame_name].grid(row=1, column=1, sticky=tk.NSEW)
                self.__frames[frame_name].show_frame()
            else:
                self.__frames[frame_name].hide_frame()
                self.__frames[frame_name].grid_remove()

    def __program_buttons(self):
        self.frame_main_menu.button_loading.configure(
            command=lambda: self.__change_frame(frame_name='LOADING')
        )
        self.frame_main_menu.button_testing.configure(
            command=lambda: self.__change_frame(frame_name='TESTING')
        )

    def __add_events(self):
        self.protocol('WM_DELETE_WINDOW', self._on_exit)

    def _on_exit(self):
        result = messagebox.askyesno('EXIT', 'Are You sure?')
        if(result is True):
            # Save protocol
            self.quit()
            self.destroy()


# class MainWindow(tk.Tk):
#     def __init__(self, *args, **kwargs):
#         tk.Tk.__init__(self, *args, **kwargs)

#         self.tests_count = None
#         self.counter = 0

#         self.__set_parameters()
#         self.__create_widgets()
#         self.mainloop()

#     def __listen(self):
#         if(not linker.queue_empty()):
#             text = linker.queue_get()
#             # for key, value in text.items():
#             #     self.__add_text(new_text=key + ": " + str(value))
#             # self.__add_text(new_text="="*100)
#             self.counter += 1
#             self.after(ms=20, func=self.__listen)
#         else:
#             if(self.counter < self.tests_count):
#                 self.after(ms=20, func=self.__listen)
#             else:
#                 self.counter = 0

#     def __set_parameters(self):
#         self.title('PyEasyTesting')
#         self.rowconfigure(index=0, weight=1)
#         self.rowconfigure(index=1, weight=0)
#         self.columnconfigure(index=0, weight=1)

#     def __create_widgets(self):
#         pass

#     def start_test(self):
#         self.text['state'] = tk.NORMAL
#         self.text.delete(0.0, tk.END)
#         self.text['state'] = tk.DISABLED
#         modules = [
#             # 'tests.tempTest',
#             'tests.tempTest2',
#             # 'tests.tempTest3',
#         ]
#         # tm = test_manager.TestManager()
#         # tm.build_tests(modules=modules)
#         # self.tests_count = tm.tests_count
#         # tm.start_tests()
#         # self.__listen()


if(__name__ == "__main__"):
    PyEasyTesting_Window()
