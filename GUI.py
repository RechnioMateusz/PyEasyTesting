import os
import sys
import traceback
import logging
import logging.config
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter.simpledialog import askstring

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import matplotlib.pyplot as plt

import _loader
from gui_elements import my_widgets
from gui_elements import my_windows
from _logic import logic


def loading_cursor(method):
    def wrapper(master, *args, **kwargs):
        if(sys.platform.lower() == 'linux'):
            master.configure(cursor='watch')
        else:
            master.configure(cursor='wait')
        master.update()
        ret = method(master, *args, **kwargs)
        master.configure(cursor='arrow')
        return ret
    return wrapper


class Frame_Program_Title(my_widgets.My_Frame):
    def __init__(self, *args, **kwargs):
        my_widgets.My_Frame.__init__(self, *args, **kwargs)
        self.master.logger.info(
            'Creating {:s}...'.format(self.__class__.__name__)
        )

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
            self, *args, text='Main Menu', **kwargs
        )
        self.master.logger.info(
            'Creating {:s}...'.format(self.__class__.__name__)
        )

    def _set_parameters(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=0)
        self.rowconfigure(4, weight=0)

    def _create_widgets(self):
        self.master.logger.info('Programming buttons...')
        self.button_loading = my_widgets.My_Button(
            master=self, text='Loading', command=self.change_frame_loading
        )
        self.button_loading.grid(
            row=1, column=0, sticky=tk.NSEW, padx=10, pady=10
        )

        self.button_testing = my_widgets.My_Button(
            master=self, text='Testing', command=self.change_frame_testing
        )
        self.button_testing.grid(
            row=2, column=0, sticky=tk.NSEW, padx=10, pady=10
        )

        self.button_results = my_widgets.My_Button(
            master=self, text='Results', command=self.change_frame_results
        )
        self.button_results.grid(
            row=3, column=0, sticky=tk.NSEW, padx=10, pady=10
        )

        self.button_analysis = my_widgets.My_Button(
            master=self, text='Analysis', command=self.change_frame_analysis
        )
        self.button_analysis.grid(
            row=4, column=0, sticky=tk.NSEW, padx=10, pady=10
        )

    def change_frame_loading(self):
        self.master.change_frame(frame_name='LOADING')
        self.button_loading.configure(state=tk.DISABLED)
        self.button_testing.configure(state=tk.NORMAL)
        self.button_results.configure(state=tk.NORMAL)
        self.button_analysis.configure(state=tk.NORMAL)

    def change_frame_testing(self):
        self.master.change_frame(frame_name='TESTING')
        self.button_loading.configure(state=tk.NORMAL)
        self.button_testing.configure(state=tk.DISABLED)
        self.button_results.configure(state=tk.NORMAL)
        self.button_analysis.configure(state=tk.NORMAL)

    def change_frame_results(self):
        self.master.change_frame(frame_name='RESULTS')
        self.button_loading.configure(state=tk.NORMAL)
        self.button_testing.configure(state=tk.NORMAL)
        self.button_results.configure(state=tk.DISABLED)
        self.button_analysis.configure(state=tk.NORMAL)

    def change_frame_analysis(self):
        self.master.change_frame(frame_name='ANALYSIS')
        self.button_loading.configure(state=tk.NORMAL)
        self.button_testing.configure(state=tk.NORMAL)
        self.button_results.configure(state=tk.NORMAL)
        self.button_analysis.configure(state=tk.DISABLED)


class Empty_Frame(my_widgets.My_Frame):
    def __init__(self, *args, **kwargs):
        my_widgets.My_Frame.__init__(self, *args, **kwargs)
        self.master.logger.info(
            'Creating {:s}...'.format(self.__class__.__name__)
        )

    def _set_parameters(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def _create_widgets(self):
        self.label_info = my_widgets.My_Label(master=self, text='Some info')
        self.label_info.grid(row=0, column=0, sticky=tk.NSEW, padx=10, pady=10)

    def hide_frame(self):
        pass

    def show_frame(self):
        pass


class Frame_Loading(my_widgets.My_Label_Frame_Independent):
    def __init__(self, *args, **kwargs):
        my_widgets.My_Label_Frame_Independent.__init__(
            self, *args, text='LOADING'
        )
        self.master.logger.info(
            'Creating {:s}...'.format(self.__class__.__name__)
        )

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
        self.tree_files.bind('<Double-Button-1>', self.__on_lmb_double_click)
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
            master=self.frame_info, relief=tk.GROOVE,
            font=('Consolas', 10), text='Test found'
        )
        self.info1.set_positive_scan()
        self.info1.grid(row=0, column=0, sticky=tk.NSEW)
        self.info2 = my_widgets.My_Label(
            master=self.frame_info, relief=tk.GROOVE,
            font=('Consolas', 10), text='Test not found'
        )
        self.info2.set_negative_scan()
        self.info2.grid(row=0, column=1, sticky=tk.NSEW)
        self.info3 = my_widgets.My_Label(
            master=self.frame_info, relief=tk.GROOVE,
            font=('Consolas', 10), text='Is test [by user]'
        )
        self.info3.set_positive_user()
        self.info3.grid(row=0, column=2, sticky=tk.NSEW)
        self.info4 = my_widgets.My_Label(
            master=self.frame_info, relief=tk.GROOVE,
            font=('Consolas', 10), text='Is not test [by user]'
        )
        self.info4.set_negative_user()
        self.info4.grid(row=0, column=3, sticky=tk.NSEW)
        self.info5 = my_widgets.My_Label(
            master=self.frame_info, relief=tk.GROOVE,
            font=('Consolas', 10), text='Cannot scan'
        )
        self.info5.set_cannot_scan()
        self.info5.grid(row=0, column=4, sticky=tk.NSEW)
        self.info6 = my_widgets.My_Label(
            master=self.frame_info, relief=tk.GROOVE,
            font=('Consolas', 10), text='Not \'Python\' file'
        )
        self.info6.set_normal_background()
        self.info6.grid(row=0, column=5, sticky=tk.NSEW)

    def __update_frame(self):
        if(self.master.logic.loading_directory is None):
            self.button_scan_for_tests.configure(state=tk.DISABLED)
            self.button_save.configure(state=tk.DISABLED)
        else:
            self.button_scan_for_tests.configure(state=tk.NORMAL)
            self.button_save.configure(state=tk.NORMAL)
        if(self.__update is True):
            self.after(40, self.__update_frame)

    def __find_directory(self):
        temp_directory = filedialog.askdirectory()
        if(temp_directory != ''):
            self.__clear_tree()
            self.master.logic.clear_loading_logic()

            self.master.logic.loading_directory = temp_directory
            self.label_directory.configure(
                text='Directory:\n{:s}'.format(
                    self.master.logic.loading_directory
                )
            )
            self.master.logger.info('Starting recursive search in {:s}'.format(
                self.master.logic.loading_directory
            ))
            self.__start_filling_process()

    def __clear_tree(self):
        self.tree_files.delete(*self.tree_files.get_children())

    @loading_cursor
    def __start_filling_process(self):
        last_folder = self.master.logic.files_creator.get_file_from_path(
            path=self.master.logic.loading_directory
        )
        self.tree_files.insert(
            parent='', index=tk.END, iid=last_folder,
            text=last_folder, values=('', ), tags=(last_folder, )
        )
        self.master.logic.loading_files_register[last_folder] = \
            self.master.logic.loading_directory
        self.__fill_tree(
            path=self.master.logic.loading_directory, root=last_folder
        )

    def __fill_tree(self, path, root):
        files = os.listdir(path)
        for _file in files:
            new_path = os.path.join(path, _file)
            new_root = root + '-' + _file
            self.master.logic.loading_files_register[new_root] = new_path
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
        for key, file_path in self.master.logic.loading_files_register.items():
            result = self.master.logic.detector.is_test_file(
                module_path=file_path
            )
            if(result is True):
                self.tree_files.set_bg_positive_scan(key=key)
                self.tree_files.item(item=key, values=(True, ))
                tests_counter += 1
            elif(result is False):
                self.tree_files.set_bg_negative_scan(key=key)
                self.tree_files.item(item=key, values=(False, ))
                none_tests_counter += 1
            elif(result is None):
                self.tree_files.item(item=key, values=('', ))
                other_counter += 1
            elif(type(result) == str and result == 'FAILED'):
                self.tree_files.set_bg_cannot_scan(key=key)
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
            self.master.logger.info(m)
            messagebox.showinfo('SUCCES', m)

    def __on_lmb_double_click(self, event):
        try:
            item = self.tree_files.selection()[0]
            self.tree_files.selection_remove(item)
        except IndexError as ex:
            self.master.logger.debug(
                'Cannot select this item. {:s}'.format(str(ex))
            )
        else:
            item_children = self.tree_files.get_children(item=item)
            if(
                len(item_children) == 0 and
                self.master.logic.detector.is_python_module(module_name=item)
            ):
                is_test = self.tree_files.item(item)['values'][0]
                if(is_test == 'True'):
                    self.tree_files.set_bg_negative_user(key=item)
                    self.tree_files.item(item=item, values=(False, ))
                elif(is_test == 'False' or is_test == ''):
                    self.tree_files.set_bg_positive_user(key=item)
                    self.tree_files.item(item=item, values=(True, ))

    def __get_only_tests(self, parent, register):
        children = self.tree_files.get_children(item=parent)
        for child in children:
            grand_children = self.tree_files.get_children(item=child)
            if(len(grand_children) == 0):
                is_test = self.tree_files.item(child)['values'][0]
                if(is_test == 'True'):
                    register[child] = \
                        self.master.logic.loading_files_register[child]
            else:
                self.__get_only_tests(parent=child, register=register)

    def __ask_project_name(self):
        result = messagebox.askyesno(
            'Choose project name',
            'Do you want to use folder name as project name?'
        )
        if(result is False):
            project_name = askstring('Project name', 'Enter project name')
            return project_name
        else:
            return str()

    def __save_project(self):
        last_folder = self.master.logic.files_creator.get_file_from_path(
            path=self.master.logic.loading_directory
        )
        register = dict()
        self.__get_only_tests(parent=last_folder, register=register)
        elements = self.__fetch_elements(register=register)

        project_name = self.__ask_project_name()
        if(project_name is None):
            return
        elif(len(project_name) == 0):
            project_name = last_folder

        try:
            self.master.logic.files_creator.save_project(
                project_name=project_name, tests_paths=register,
                elements=elements,
                folder=self.master.logic.settings.projects_folder
            )
        except Exception as ex:
            messagebox.showerror(
                'ERROR',
                'Unexpected error has occured while saving.\n{:s}'.format(
                    str(ex)
                )
            )
        else:
            m = 'Project succesfully saved as \'{:s}.json\'.'.format(
                    project_name
                )
            self.master.logger.info(m)
            messagebox.showinfo('SUCCESS', m)

    def __fetch_elements(self, register):
        elements = list()
        for key in register:
            _test_module = {
                'path': register[key]
            }
            _module = self.master.logic.detector.load_module(
                module_path=register[key]
            )
            test_cases = self.__fetch_test_cases(_module=_module)
            _test_module[_module.__name__] = test_cases
            elements.append(_test_module)
        return elements

    def __fetch_test_cases(self, _module):
        _classes = self.master.logic.detector.get_module_classes(
            _module=_module
        )
        _test_cases = dict()
        for _class in _classes:
            if(self.master.logic.detector.is_test_class(_class=_class)):
                _tests = self.__fetch_tests(_class=_class)
                _test_cases[_class.__name__] = _tests
        return _test_cases

    def __fetch_tests(self, _class):
        _methods = self.master.logic.detector.get_class_methods(
            _class=_class
        )
        _tests = list()
        for _method in _methods:
            if(self.master.logic.detector.is_test_method(_method=_method)):
                _tests.append(_method.__name__)
        return _tests

    def hide_frame(self):
        self.__update = False
        self.__clear_tree()
        self.master.logic.clear_loading_logic()

    def show_frame(self):
        self.__update = True
        self.__update_frame()


class Frame_Testing(my_widgets.My_Label_Frame_Independent):
    def __init__(self, *args, **kwargs):
        my_widgets.My_Label_Frame_Independent.__init__(
            self, *args, text='TESTING', **kwargs
        )
        self.__update = False
        self.master.logger.info(
            'Creating {:s}...'.format(self.__class__.__name__)
        )

    def __listen_to_checkbuttons(self):
        if(self.multithreading_var.get() is True):
            self.checkbutton_multithreading_testing.check()
        else:
            self.checkbutton_multithreading_testing.uncheck()

        if(self.__update):
            self.after(50, self.__listen_to_checkbuttons)

    def __update_parent(self, register):
        for item in register:
            children = self.tree_files.get_children(item)
            counter = 0
            for child in children:
                if(self.tree_files.item(child)['values'][0] == 'True'):
                    counter += 1
            ignore, _type = self.tree_files.item(item)['values']
            if(counter == len(children)):
                ignore = True
                self.tree_files.set_fg_ignore(key=item)
                self.tree_files.item(
                    item=item, values=(ignore, _type)
                )
            else:
                ignore = False
                self.tree_files.set_fg_not_ignore(key=item)
                self.tree_files.item(
                    item=item, values=(ignore, _type)
                )

    def __check_items_ignore(self, register):
        counter = 0
        for key in register:
            if(self.tree_files.item(key)['values'][0] == 'True'):
                counter += 1
        if(counter == len(register)):
            return True
        else:
            return False

    def __update_start_button(self):
        if(len(self.tree_files.get_children()) == 0):
            self.button_start_test.configure(state=tk.DISABLED)
            return

        modules_ignore = self.__check_items_ignore(
            register=self.master.logic.testing_modules_register
        )
        classes_ignore = self.__check_items_ignore(
            register=self.master.logic.testing_classes_register
        )
        methods_ignore = self.__check_items_ignore(
            register=self.master.logic.testing_methods_register
        )
        if(modules_ignore and classes_ignore and methods_ignore):
            self.button_start_test.configure(state=tk.DISABLED)
        else:
            self.button_start_test.configure(state=tk.NORMAL)

    def __update_tree(self):
        self.__update_start_button()
        self.__update_parent(
            register=self.master.logic.testing_classes_register
        )
        self.__update_parent(
            register=self.master.logic.testing_modules_register
        )

    def _set_parameters(self):
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

    def _create_widgets(self):
        self.tree_frame = my_widgets.My_Little_Frame(master=self)
        self.tree_frame.rowconfigure(0, weight=1)
        self.tree_frame.rowconfigure(1, weight=0)
        self.tree_frame.columnconfigure(0, weight=1)
        self.tree_frame.columnconfigure(1, weight=0)
        self.tree_frame.grid(
            row=1, column=0, sticky=tk.NSEW, padx=(10, 5), pady=10
        )
        self.tree_files = my_widgets.My_Treeview(
            master=self.tree_frame, columns=('Test', 'Ignore', 'Type', 'ID'),
            selectmode='extended'
        )
        self.tree_files.bind('<Double-Button-1>', self.__ignore_handler)
        self.tree_files.heading('#0', text='Test', anchor=tk.CENTER)
        self.tree_files.heading('#1', text='Ignore', anchor=tk.CENTER)
        self.tree_files.heading('#2', text='Type', anchor=tk.CENTER)
        self.tree_files.column('#0', stretch=tk.YES, minwidth=50)
        self.tree_files.column('#1', stretch=tk.YES, minwidth=50)
        self.tree_files.column('#2', stretch=tk.YES, minwidth=50)
        self.tree_files.grid(row=0, column=0, sticky=tk.NSEW)

        self.scrollbar_vert = my_widgets.My_Scrollbar(
            master=self.tree_frame, command=self.tree_files.yview,
            orient=tk.VERTICAL, cursor='sb_v_double_arrow'
        )
        self.scrollbar_vert.grid(row=0, column=1, sticky=tk.NS, pady=1)

        self.scrollbar_hor = my_widgets.My_Scrollbar(
            master=self.tree_frame, command=self.tree_files.xview,
            orient=tk.HORIZONTAL, cursor='sb_h_double_arrow'
        )
        self.scrollbar_hor.grid(row=1, column=0, sticky=tk.EW, padx=1)

        self.tree_files.configure(yscrollcommand=self.scrollbar_vert.set)
        self.tree_files.configure(xscrollcommand=self.scrollbar_hor.set)

        self.buttons_frame = my_widgets.My_Little_Frame(master=self)
        self.buttons_frame.rowconfigure(0, weight=1)
        self.buttons_frame.columnconfigure(0, weight=0)
        self.buttons_frame.columnconfigure(1, weight=0)
        self.buttons_frame.columnconfigure(2, weight=0)
        self.buttons_frame.columnconfigure(3, weight=0)
        self.buttons_frame.columnconfigure(4, weight=0)
        self.buttons_frame.grid(row=0, column=0, sticky=tk.EW)

        self.label_projects_selector = my_widgets.My_Label(
            master=self.buttons_frame, text='Choose project: '
        )
        self.label_projects_selector.grid(
            row=0, column=0, sticky=tk.NSEW, padx=10
        )

        self.combobox_projects = my_widgets.My_Combobox(
            master=self.buttons_frame
        )
        self.combobox_projects.bind(
            '<<ComboboxSelected>>', self.__on_combobox_selected
        )
        self.combobox_projects.grid(
            row=0, column=1, sticky=tk.EW, padx=10, pady=(10, 5)
        )

        self.multithreading_var = tk.BooleanVar(master=self)
        self.checkbutton_multithreading_testing = my_widgets.My_Checkbutton(
            master=self.buttons_frame, text='Multithreading tests',
            variable=self.multithreading_var
        )
        self.checkbutton_multithreading_testing.grid(
            row=0, column=2, sticky=tk.NSEW, padx=(5, 10), pady=(5, 10)
        )

        self.separator = my_widgets.My_Separator(master=self.buttons_frame)
        self.separator.grid(row=0, column=3, sticky=tk.NSEW)

        self.button_start_test = my_widgets.My_Button(
            master=self.buttons_frame, text='Start tests',
            command=self.__start_testing
        )
        self.button_start_test.grid(
            row=0, column=4, sticky=tk.NSEW, padx=(5, 10), pady=5
        )

    def __ignore_handler(self, event):
        try:
            item = self.tree_files.selection()[0]
            self.tree_files.selection_remove(item)
        except IndexError as ex:
            self.master.logger.debug(
                'Cannot select this item. {:s}'.format(str(ex))
            )
        else:
            ignore = self.tree_files.item(item)['values'][0]
            if(ignore == 'True'):
                ignore = False
            else:
                ignore = True
            self.__ignore_recursively(item=item, ignore=ignore)
            self.__update_tree()

    def __ignore_recursively(self, item, ignore):
        _type = self.tree_files.item(item)['values'][1]
        if(ignore is False):
            self.tree_files.set_fg_not_ignore(key=item)
            self.tree_files.item(item=item, values=(ignore, _type))
        else:
            self.tree_files.set_fg_ignore(key=item)
            self.tree_files.item(item=item, values=(ignore, _type))
        self.tree_files.item(item=item, values=(ignore, _type))
        grand_items = self.tree_files.get_children(item=item)

        for grand_item in grand_items:
            self.__ignore_recursively(item=grand_item, ignore=ignore)

    def __clear_tree(self):
        self.tree_files.delete(*self.tree_files.get_children())

    @loading_cursor
    def __on_combobox_selected(self, event):
        self.__clear_tree()
        self.master.logic.clear_testing_logic()
        project = self.master.logic.files_creator.load_project(
            project_name=self.combobox_projects.get()
        )
        self.master.logger.info('Loading project {:s}'.format(project['name']))
        self.__fill_tree(project=project)
        self.__update_tree()

    def __fill_tree(self, project):
        self.master.logger.info('Files and tests in project:')
        self.__add_modules(project=project, root=project['name'])

    def __add_modules(self, project, root):
        for test in project['tests']:
            _module = self.master.logic.detector.load_module(
                module_path=test['path']
            )
            self.master.logger.info('-{:s}'.format(_module.__name__))

            new_root = '{:s}*{:s}*{:s}'.format(
                root, test['path'], _module.__name__
            )
            self.master.logic.testing_modules_register[new_root] = _module
            self.tree_files.insert(
                parent='', index=tk.END, iid=new_root, text=_module.__name__,
                values=(False, 'Module'), tags=(new_root, )
            )

            self.__add_classes(_module=_module, root=new_root)

    def __add_classes(self, _module, root):
        _classes = self.master.logic.detector.get_module_classes(
            _module=_module
        )
        for _class in _classes:
            if(self.master.logic.detector.is_test_class(_class=_class)):
                self.master.logger.info('--{:s}'.format(_class.__name__))

                new_root = '{:s}*{:s}'.format(root, _class.__name__)
                self.master.logic.testing_classes_register[new_root] = _class
                self.tree_files.insert(
                    parent=root, index=tk.END, iid=new_root,
                    text=_class.__name__, values=(False, 'Class'),
                    tags=(new_root, )
                )

                self.__add_methods(_class=_class, root=new_root)

    def __add_methods(self, _class, root):
        _methods = self.master.logic.detector.get_class_methods(_class=_class)
        for _method in _methods:
            if(self.master.logic.detector.is_test_method(_method=_method)):
                self.master.logger.info('---{:s}'.format(_method.__name__))

                new_root = '{:s}*{:s}'.format(root, _method.__name__)
                self.master.logic.testing_methods_register[new_root] = _method
                self.tree_files.insert(
                    parent=root, index=tk.END, iid=new_root,
                    text=_method.__name__, values=(False, 'Method'),
                    tags=(new_root, )
                )

    def __prepare_register_to_test(self, register):
        objects_to_test = dict()
        for key, obj in register.items():
            if(self.tree_files.item(key)['values'][0] == 'False'):
                objects_to_test[key] = obj
        return objects_to_test

    def __start_testing(self):
        self.master.logic.reload_project_files(
            project_name=self.combobox_projects.get()
        )

        classes_to_test = self.__prepare_register_to_test(
            register=self.master.logic.testing_classes_register
        )
        classes_to_test = [val for key, val in classes_to_test.items()]
        methods_to_test = self.__prepare_register_to_test(
            register=self.master.logic.testing_methods_register
        )
        classes_to_test = self.master.logic.prepare_tests(
            _classes=classes_to_test, _methods=methods_to_test
        )

        self.master.logic.read_time_and_date()
        multithreading = self.multithreading_var.get()
        self.master.logic.start_testing(
            test_cases=classes_to_test, multithreading=multithreading
        )
        self.master.logic.copy_modules_and_classes()
        self.master.frame_main_menu.change_frame_results()

    def hide_frame(self):
        self.__update = False
        self.__clear_tree()
        self.master.logic.clear_testing_logic()

    def show_frame(self):
        self.combobox_projects.configure(
            values=self.master.logic.files_creator.get_existing_projects(
                projects_folder=self.master.logic.settings.projects_folder
            )
        )
        self.__update_start_button()
        self.__update = True
        self.__listen_to_checkbuttons()
        self.combobox_projects.set('')


class Frame_Results(my_widgets.My_Label_Frame_Independent):
    def __init__(self, *args, **kwargs):
        my_widgets.My_Label_Frame_Independent.__init__(
            self, *args, text='RESULTS', **kwargs
        )

        self.tests_count = None
        self.counter = 0
        self.__partial = None

        # Counters
        self.__tests_passed = 0
        self.__tests_errors = 0
        self.__tests_failures = 0

        self.master.logger.info(
            'Creating {:s}...'.format(self.__class__.__name__)
        )

    def __listen_to_test_process(self):
        if(not self.master.logic.is_queue_empty()):
            test_result = self.master.logic.queue_get()
            self.__add_method_result(result_data=test_result)
            self.counter += 1
            self.after(ms=20, func=self.__listen_to_test_process)
        else:
            if(self.counter < self.tests_count):
                self.after(ms=20, func=self.__listen_to_test_process)
            else:
                self.counter = 0
                self.__open_items_with_errors(
                    top_level_parents=self.tree_files.get_children()
                )
                self.master.logic.save_results()
                self.__sum_up_tests()

    def __sum_up_tests(self):
        message = 'Testing complete [{:n} tests]\n'.format(self.tests_count)
        message += 'Tests passed: {:n}\n'.format(self.__tests_passed)
        message += 'Tests errors: {:n}\n'.format(self.__tests_errors)
        message += 'Tests failures: {:n}'.format(self.__tests_failures)
        messagebox.showinfo(title='TESTING RESULTS', message=message)

    def _set_parameters(self):
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)

    def _create_widgets(self):
        self.label_project = my_widgets.My_Label(master=self)
        self.label_project.grid(row=0, column=0, columnspan=3, sticky=tk.NSEW)

        self.tree_files = my_widgets.My_Treeview(
            master=self, columns=('Test', 'Type', 'Result', 'ID'),
            selectmode='extended'
        )
        self.tree_files.bind('<Double-Button-1>', self.__show_test_result)
        self.tree_files.heading('#0', text='Test', anchor=tk.CENTER)
        self.tree_files.heading('#1', text='Type', anchor=tk.CENTER)
        self.tree_files.heading('#2', text='Result', anchor=tk.CENTER)
        self.tree_files.column('#0', stretch=tk.YES, minwidth=50)
        self.tree_files.column('#1', stretch=tk.YES, minwidth=50)
        self.tree_files.column('#2', stretch=tk.YES, minwidth=50)
        self.tree_files.grid(row=1, column=1, sticky=tk.NSEW)

        self.scrollbar_vert = my_widgets.My_Scrollbar(
            master=self, command=self.tree_files.yview,
            orient=tk.VERTICAL, cursor='sb_v_double_arrow'
        )
        self.scrollbar_vert.grid(row=1, column=2, sticky=tk.NS, pady=1)

        self.scrollbar_hor = my_widgets.My_Scrollbar(
            master=self, command=self.tree_files.xview,
            orient=tk.HORIZONTAL, cursor='sb_h_double_arrow'
        )
        self.scrollbar_hor.grid(row=2, column=1, sticky=tk.EW, padx=1)

        self.tree_files.configure(yscrollcommand=self.scrollbar_vert.set)
        self.tree_files.configure(xscrollcommand=self.scrollbar_hor.set)

        self.progressbar = my_widgets.My_Progressbar(master=self, length=2)
        self.progressbar.grid(
            row=1, column=0, rowspan=2, sticky=tk.NS, padx=2, pady=2
        )

    def __show_test_result(self, event):
        try:
            item = self.tree_files.selection()[0]
            self.tree_files.selection_remove(item)
        except IndexError as ex:
            self.master.logger.debug(
                'Cannot select this item. {:s}'.format(str(ex))
            )
        else:
            try:
                test_info = self.master.logic.methods_register[item]
            except KeyError as ex:
                self.master.logger.info('Cannot choose anything than method')
            else:
                my_windows.Test_Info(master=self, method_info=test_info)

    def __add_modules(self):
        for key in self.master.logic.modules_keys:
            name = self.master.logic.get_name_from_key(key=key)
            self.tree_files.insert(
                parent='', index=tk.END, iid=key, text=name,
                values=('Module', ''), tags=(key, ), open=True
            )
            self.__add_classes(root=key)

    def __add_classes(self, root):
        for key in self.master.logic.classes_keys:
            if(root in key):
                name = self.master.logic.get_name_from_key(key=key)
                self.tree_files.insert(
                    parent=root, index=tk.END, iid=key, text=name,
                    values=('Class', ''), tags=(key, )
                )

    def __add_method_result(self, result_data):
        for key in self.master.logic.methods_register:
            result_key = '{:s}*{:s}*{:s}'.format(
                result_data['module'], result_data['class'],
                result_data['method']
            )
            if(result_key == key):
                self.master.logic.methods_register[key] = result_data

                new_root = '{:s}*{:s}'.format(
                    result_data['module'], result_data['class']
                )
                test_result = self.__get_result(
                    key=key, result=result_data['result'],
                    error=result_data['error_text'],
                    failure=result_data['failure_text']
                )
                self.tree_files.insert(
                    parent=new_root, index=tk.END, iid=key,
                    text=result_data['method'], values=('Method', test_result),
                    tags=(key, )
                )
                self.__change_color_due_result(
                    key=key, result=result_data['result'],
                    error=result_data['error_text'],
                    failure=result_data['failure_text']
                )
                self.progressbar.step(amount=1)
                self.tree_files.update()

    def __get_result(self, key, result, error=None, failure=None):
        if(result is True):
            return 'PASS'
        else:
            if(error is not None):
                return 'ERROR'
            elif(failure is not None):
                return 'FAILURE'

    def __change_color_due_result(self, key, result, error=None, failure=None):
        if(result is True):
            self.tree_files.set_positive(key=key)
            self.__tests_passed += 1
        else:
            if(error is not None):
                self.tree_files.set_error(key=key)
                self.__tests_errors += 1
            elif(failure is not None):
                self.tree_files.set_failure(key=key)
                self.__tests_failures += 1

    def __open_items_with_errors(self, top_level_parents):
        for parent in top_level_parents:
            self.__start_opening(parent=parent)

    def __start_opening(self, parent):
        children = self.tree_files.get_children(parent)
        for child in children:
            result = self.tree_files.item(child)['values'][1]
            if(result == 'FAILURE' or result == 'ERROR'):
                self.tree_files.item(parent, open=True)
                break
            else:
                self.__start_opening(parent=child)

    def __clear_tree(self):
        self.tree_files.delete(*self.tree_files.get_children())

    def hide_frame(self):
        self.tests_count = None
        self.counter = 0
        self.__partial = None
        self.__tests_passed = 0
        self.__tests_errors = 0
        self.__tests_failures = 0
        self.__clear_tree()
        self.master.logic.clear_result_logic()

    def show_frame(self):
        try:
            self.tests_count = self.master.logic.tests_amount
            self.progressbar.configure(maximum=self.tests_count)
            project_name = self.master.logic.get_project_name()
            project_name = 'Project \'{:s}\' results:'.format(project_name)
            self.label_project.configure(text=project_name)
            self.__add_modules()
            self.__listen_to_test_process()
        except:
            self.master.logger.info('Opening results without project...')


class Inner_Frame_Plot(my_widgets.My_Frame):
    def __init__(self, *args, **kwargs):
        self.fig = None
        self.ax = None
        self.create_default_plot()

        my_widgets.My_Frame.__init__(self, *args, **kwargs)

    def _set_parameters(self):
        pass

    def _create_widgets(self):
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.toolbar = NavigationToolbar2Tk(canvas=self.canvas, window=self)
        self.toolbar.config(background=my_widgets.toolbar_bg)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def create_default_plot(self):
        self.fig, self.ax = plt.subplots()
        self.fig.set_facecolor(my_widgets.fig_color)
        self.ax.set_facecolor(my_widgets.ax_color)
        a = [i for i in range(-10, 11)]
        b = [i**3 for i in range(-10, 11)]
        self.ax.plot(a, b)
        self.ax.set(xlabel='date', ylabel='results', title='Default plot')
        self.ax.grid()

    def add_plot(self, plot_info):
        self.fig, self.ax = plt.subplots()
        self.fig.set_facecolor(my_widgets.fig_color)
        self.ax.set_facecolor(my_widgets.ax_color)
        positives, negatives, dates = list(), list(), list()
        for date, results in plot_info.items():
            dates.append(
                self.master.master.logic.parse_str_to_date(date_str=date)
            )
            positives.append(results[0])
            negatives.append(results[1])
        self.ax.plot(dates, positives, '.-', label='Positive')
        self.ax.plot(dates, negatives, '.-', label='Negative')
        self.ax.legend()
        self.ax.set(xlabel='date', ylabel='results')
        self.ax.grid()
        self.canvas.get_tk_widget().destroy()
        self.toolbar.destroy()
        self._create_widgets()


class Frame_Analysis(my_widgets.My_Label_Frame_Independent):
    def __init__(self, *args, **kwargs):
        my_widgets.My_Label_Frame_Independent.__init__(
            self, *args, text='ANALYSIS', **kwargs
        )

        self.project = None
        self.modules = list()
        self.test_cases = list()
        self.tests = list()
        self.__update = False

        self.master.logger.info(
            'Creating {:s}...'.format(self.__class__.__name__)
        )

    def __listen_to_comboboxes(self):
        sub_comboboxes = (
            self.combobox_project.get(),
            self.combobox_module.get(),
            self.combobox_test_case.get(),
            self.combobox_test.get(),
        )
        if(any(sub_comboboxes)):
            self.button_generate.enable()
        else:
            self.button_generate.disable()

        if(self.__update is True):
            self.after(20, self.__listen_to_comboboxes)

    def _set_parameters(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

    def _create_widgets(self):
        self.frame_navigation = my_widgets.My_Little_Frame(master=self)
        self.frame_navigation.columnconfigure(0, weight=1)
        self.frame_navigation.rowconfigure(0, weight=0)
        self.frame_navigation.rowconfigure(1, weight=0)
        self.frame_navigation.rowconfigure(2, weight=0)
        self.frame_navigation.rowconfigure(3, weight=0)
        self.frame_navigation.rowconfigure(4, weight=0)
        self.frame_navigation.rowconfigure(5, weight=0)
        self.frame_navigation.rowconfigure(6, weight=0)
        self.frame_navigation.rowconfigure(7, weight=0)
        self.frame_navigation.rowconfigure(8, weight=0)
        self.frame_navigation.rowconfigure(9, weight=0)
        self.frame_navigation.grid(row=0, column=0, sticky=tk.NSEW)

        self.label_project = my_widgets.My_Label(
            master=self.frame_navigation, text='Project'
        )
        self.label_project.grid(
            row=0, column=0, sticky=tk.NSEW, padx=10, pady=(10, 0)
        )

        self.combobox_project = my_widgets.My_Combobox(
            master=self.frame_navigation
        )
        self.combobox_project.bind('<<ComboboxSelected>>', self.__load_project)
        self.combobox_project.grid(
            row=1, column=0, sticky=tk.EW, padx=10, pady=(0, 10)
        )

        self.label_module = my_widgets.My_Label(
            master=self.frame_navigation, text='Module'
        )
        self.label_module.grid(
            row=2, column=0, sticky=tk.NSEW, padx=10, pady=(10, 0)
        )

        self.combobox_module = my_widgets.My_Combobox(
            master=self.frame_navigation
        )
        self.combobox_module.bind('<<ComboboxSelected>>', self.__load_module)
        self.combobox_module.disable()
        self.combobox_module.grid(
            row=3, column=0, sticky=tk.EW, padx=10, pady=(0, 10)
        )

        self.label_test_case = my_widgets.My_Label(
            master=self.frame_navigation, text='Test case'
        )
        self.label_test_case.grid(
            row=4, column=0, sticky=tk.NSEW, padx=10, pady=(10, 0)
        )

        self.combobox_test_case = my_widgets.My_Combobox(
            master=self.frame_navigation
        )
        self.combobox_test_case.bind(
            '<<ComboboxSelected>>', self.__load_test_case
        )
        self.combobox_test_case.disable()
        self.combobox_test_case.grid(
            row=5, column=0, sticky=tk.EW, padx=10, pady=(0, 10)
        )

        self.label_test = my_widgets.My_Label(
            master=self.frame_navigation, text='Test'
        )
        self.label_test.grid(
            row=6, column=0, sticky=tk.NSEW, padx=10, pady=(10, 0)
        )

        self.combobox_test = my_widgets.My_Combobox(
            master=self.frame_navigation
        )
        self.combobox_test.disable()
        self.combobox_test.grid(
            row=7, column=0, sticky=tk.EW, padx=10, pady=(0, 10)
        )

        self.separator = my_widgets.My_Separator(master=self.frame_navigation)
        self.separator.grid(row=8, column=0, sticky=tk.NSEW, pady=20)

        self.button_generate = my_widgets.My_Button(
            master=self.frame_navigation, text='Generate',
            command=self.__generate
        )
        self.button_generate.grid(
            row=9, column=0, sticky=tk.NSEW, padx=10, pady=10
        )

        self.frame_plot = Inner_Frame_Plot(master=self)
        self.frame_plot.grid(
            row=0, column=1, sticky=tk.NSEW, padx=(0, 10), pady=10
        )

    def __load_project(self, event):
        self.project = self.master.logic.files_creator.load_project(
            project_name=self.combobox_project.get()
        )
        self.modules.clear()
        self.test_cases.clear()
        self.combobox_test_case.set('')
        self.combobox_test_case.configure(values=tuple())
        self.combobox_test_case.disable()
        self.tests.clear()
        self.combobox_test.set('')
        self.combobox_test.configure(values=tuple())
        self.combobox_test.disable()

        for element in self.project['elements']:
            module_name = str()
            module_path = str()
            for _module_dict_key, _module_dict_val in element.items():
                if(_module_dict_key == 'path'):
                    module_path = _module_dict_val
                else:
                    module_name = _module_dict_key
            module_key = '{:s}*{:s}*{:s}'.format(
                self.project['name'], module_path, module_name
            )
            module_key = module_name + ' '*100 + module_key
            self.modules.append(module_key)

        self.modules.append('>> ALL <<')
        self.combobox_module.configure(values=self.modules)
        self.combobox_module.set('>> ALL <<')
        self.combobox_module.enable()

    def __load_module(self, event):
        self.test_cases.clear()
        self.tests.clear()
        self.combobox_test.set('')
        self.combobox_test.configure(values=tuple())
        self.combobox_test.disable()

        _module_name = self.combobox_module.get().split(' '*100)[0]
        if(_module_name == '>> ALL <<'):
            self.test_cases.clear()
            self.combobox_test_case.configure(values=tuple())
            self.combobox_test_case.set('')
            self.combobox_test_case.disable()
            self.tests.clear()
            self.combobox_test.configure(values=tuple())
            self.combobox_test.set('')
            self.combobox_test.disable()
            return

        for element in self.project['elements']:
            for _module_dict_key, _module_dict_val in element.items():
                if(_module_dict_key == _module_name):
                    for _test_case in _module_dict_val:
                        self.test_cases.append(_test_case)

        self.test_cases.append('>> ALL <<')
        self.combobox_test_case.configure(values=self.test_cases)
        self.combobox_test_case.set('>> ALL <<')
        self.combobox_test_case.enable()

    def __load_test_case(self, event):
        self.tests.clear()
        _module_name = self.combobox_module.get().split(' '*100)[0]
        _test_case_name = self.combobox_test_case.get()
        if(_test_case_name == '>> ALL <<'):
            self.tests.clear()
            self.combobox_test.configure(values=tuple())
            self.combobox_test.set('')
            self.combobox_test.disable()
            return

        for element in self.project['elements']:
            for _module_dict_key, _module_dict_val in element.items():
                if(_module_dict_key == _module_name):
                    for _test_name in _module_dict_val[_test_case_name]:
                        self.tests.append(_test_name)

        self.tests.append('>> ALL <<')
        self.combobox_test.configure(values=self.tests)
        self.combobox_test.set('>> ALL <<')
        self.combobox_test.enable()

    def __generate(self):
        _module = self.combobox_module.get().split(' '*100)[-1]
        _test_case = self.combobox_test_case.get()
        _test = self.combobox_test.get()

        what_to_get = None

        plot_info = dict()
        for record in self.project['history']:
            date = record['date']
            plot_info[date] = [0, 0]
            for key, result in record['results'].items():

                # Getting needed data to analysis
                what_to_get = _module == '>> ALL <<'
                if(_module != '>> ALL <<'):
                    what_to_get = _module in key

                    if(_test_case == '>> ALL <<'):
                        what_to_get = what_to_get and _test_case == '>> ALL <<'
                    else:
                        what_to_get = what_to_get and \
                            _test_case == result['class']

                        if(_test == '>> ALL <<'):
                            what_to_get = what_to_get and _test == '>> ALL <<'
                        else:
                            what_to_get = what_to_get and \
                                _test == result['method']

                if(what_to_get):
                    if(result['result'] is True):
                        plot_info[date][0] += 1
                    else:
                        plot_info[date][1] += 1

        self.frame_plot.add_plot(plot_info=plot_info)

    def hide_frame(self):
        self.__update = False

    def show_frame(self):
        self.combobox_project.configure(
            values=self.master.logic.files_creator.load_projects_names()
        )
        self.__update = True
        self.__listen_to_comboboxes()


class PyEasyTesting_Window(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.logic = logic.Logic()
        logging.config.fileConfig(self.logic.settings._logging)
        self.logger = logging.getLogger('GUI')
        self.__error_logger = logging.getLogger('ERROR')

        self.report_callback_exception = self.__handle_exception

        self.__frames = {
            'EMPTY': Empty_Frame(),
            'LOADING': Frame_Loading(),
            'TESTING': Frame_Testing(),
            'RESULTS': Frame_Results(),
            'ANALYSIS': Frame_Analysis(),
        }

        self.logger.info('Setting main window parameters...')
        self._set_parameters()
        self.logger.info('Bindings keys...')
        self.__bind()
        self.logger.info('Creating static frames...')
        self.__create_static_frames()
        self.logger.info('Adding events...')
        self.__add_events()
        self.logger.info('Setting active frame...')
        self.__frame_changer()
        self.logger.info('Starting main window...')
        self.mainloop()

    def __handle_exception(self, exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        self.__error_logger.error('*'*79)
        self.__error_logger.error(
            'UNCAUGHT EXCEPTION', exc_info=(exc_type, exc_value, exc_traceback)
        )
        self.__error_logger.error('*'*79)

        tb = str()
        for info in traceback.format_tb(tb=exc_traceback):
            tb += info
        tb += exc_type.__name__ + ': ' + str(exc_value)
        messagebox.showerror(exc_type.__name__, tb)

    def _set_parameters(self):
        self.configure(bg='#222222')
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=5)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=5)
        self.geometry('1000x600')
        self.minsize(width=500, height=300)
        self.title('PyEasyTesting Main Window')

    def __create_static_frames(self):
        self.frame_title = Frame_Program_Title()
        self.frame_title.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW)

        self.frame_main_menu = Frame_Main_Menu()
        self.frame_main_menu.grid(row=1, column=0, sticky=tk.NSEW)

        self.__frames['EMPTY'].active = True

    def __bind(self):
        self.bind('<Escape>', self._on_exit)

    def change_frame(self, frame_name):
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

    def __add_events(self):
        self.protocol('WM_DELETE_WINDOW', self._on_exit)

    def _on_exit(self, event=None):
        result = messagebox.askyesno('EXIT', 'Are You sure?')
        if(result is True):
            self.logger.info('Exiting program...\n\n')
            # Save protocol
            self.quit()
            self.destroy()


if(__name__ == '__main__'):
    PyEasyTesting_Window()
