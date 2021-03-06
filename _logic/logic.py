import threading
import unittest
import copy
import datetime
import logging
import logging.config

from _internal_files import settings_agent
from _internal_files import files_creator
from _internal_files import test_detector
from _internal_files import linker


class Logic():
    def __init__(self):
        # Initialization of settings and files creator
        self.settings = settings_agent.Settings()
        self.files_creator = files_creator.Files_Creator(
            main_path=self.settings.main_path,
            directories={
                'projects': self.settings.projects_folder,
                'logs': self.settings.logs_folder,
            }
        )

        # Setting logging data
        self.settings.update_logging_settings()
        logging.config.fileConfig(self.settings._logging)
        self.logger = logging.getLogger('LOGIC')
        self.settings.set_logger(logger=logging.getLogger('SAGENT'))
        self.files_creator.set_logger(logger=logging.getLogger('FCREATOR'))
        self.settings.log_initialization_info()
        self.files_creator.log_initialization_info(
            directories={
                'projects': self.settings.projects_folder,
                'logs': self.settings.logs_folder,
            }
        )
        self.logger.info('Initialization of logic class')

        # Initialization of test detector
        self.detector = test_detector.Test_Detector(
            logger=logging.getLogger('TDETECTOR')
        )

        # Initialization of logic attributes for loading
        self.loading_directory = None
        self.loading_files_register = dict()

        # Initialization of logic attributes for testing
        self.testing_modules_register = dict()
        self.testing_classes_register = dict()
        self.testing_methods_register = dict()

        # Initialization of logic attributes for results
        self.date_formatter = '%d/%m/%Y %H:%M:%S.%f'
        self.date = None
        self.tests_amount = 0
        self.modules_keys = list()
        self.classes_keys = list()
        self.methods_register = dict()

# ========== LOADING ==========
    def clear_loading_logic(self):
        self.loading_directory = None
        self.loading_files_register = dict()

# ========== TESTING ==========
    def clear_testing_logic(self):
        self.testing_methods_register = dict()
        self.testing_classes_register = dict()
        self.testing_modules_register = dict()

    def __get_class_module_name(self, class_name):
        for key, _module in self.testing_modules_register.items():
            if(class_name in dir(_module)):
                return key

    def modify_test_case(self, _class, _methods):
        module_name = self.__get_class_module_name(class_name=_class.__name__)
        test_case = linker.sniff_info(
            test_class=_class, module_name=module_name
        )
        test_case, tests_amount_to_do = linker.ignore_tests(
            test_class=test_case, not_ignored_tests=_methods
        )
        self.tests_amount += tests_amount_to_do
        return test_case

    def start_testing(self, test_cases, multithreading=False):
        if(multithreading is True):
            jobs = list()
            for test_case in test_cases:
                suites = unittest.TestSuite()
                suites.addTest(unittest.makeSuite(test_case))
                test_runner = unittest.TextTestRunner()
                thread = threading.Thread(
                    target=test_runner.run, name=test_case.__name__,
                    kwargs={'test': suites}
                )
                jobs.append(thread)
            for job in jobs:
                job.start()
        else:
            suites = unittest.TestSuite()
            for test_case in test_cases:
                suites.addTest(unittest.makeSuite(test_case))
            test_runner = unittest.TextTestRunner()
            thread = threading.Thread(
                target=test_runner.run, name='Normal', kwargs={'test': suites}
            )
            thread.start()

    def reload_project_files(self, project_name):
        self.clear_testing_logic()
        project = self.files_creator.load_project(project_name=project_name)
        self.__reload_modules(project=project, root=project['name'])

    def __reload_modules(self, project, root):
        for test in project['tests']:
            _module = self.detector.load_module(module_path=test['path'])
            new_root = '{:s}*{:s}*{:s}'.format(
                root, test['path'], _module.__name__
            )
            self.testing_modules_register[new_root] = _module
            self.__reload_classes(_module=_module, root=new_root)

    def __reload_classes(self, _module, root):
        _classes = self.detector.get_module_classes(_module=_module)
        for _class in _classes:
            if(self.detector.is_test_class(_class=_class)):
                new_root = '{:s}*{:s}'.format(root, _class.__name__)
                self.testing_classes_register[new_root] = _class
                self.__reload_methods(_class=_class, root=new_root)

    def __reload_methods(self, _class, root):
        _methods = self.detector.get_class_methods(_class=_class)
        for _method in _methods:
            if(self.detector.is_test_method(_method=_method)):
                new_root = '{:s}*{:s}'.format(root, _method.__name__)
                self.testing_methods_register[new_root] = _method

    def __prepare_methods_to_test(self, _methods, class_name):
        methods_to_check = list()
        for key, _method in _methods.items():
            if(class_name in key):
                methods_to_check.append(_method.__name__)
        return methods_to_check

    def prepare_tests(self, _classes, _methods):
        for i in range(len(_classes)):
            methods_to_test = self.__prepare_methods_to_test(
                _methods=_methods, class_name=_classes[i].__name__
            )
            _classes[i] = self.modify_test_case(
                _class=_classes[i], _methods=methods_to_test
            )
        return _classes

# ========== RESULTS ==========
    def read_time_and_date(self):
        self.date = datetime.datetime.now()
        self.date = self.date.strftime(self.date_formatter)

    def clear_result_logic(self):
        self.tests_amount = 0
        self.modules_keys = list()
        self.classes_keys = list()
        self.methods_register = dict()

    def copy_modules_and_classes(self):
        for key in self.testing_modules_register:
            self.modules_keys.append(key)
        for key in self.testing_classes_register:
            self.classes_keys.append(key)
        for key in self.testing_methods_register:
            self.methods_register[key] = None

    def get_project_name(self):
        for key in self.modules_keys:
            key_component = key.split('*')
            return key_component[0]

    def get_name_from_key(self, key):
        name = key.split('*')
        return name[len(name) - 1]

    def queue_get(self):
        return linker.queue_get()

    def is_queue_empty(self):
        return linker.queue_empty()

    def save_results(self):
        self.read_time_and_date()
        self.files_creator.save_results(
            project_name=self.get_project_name(),
            register=self.methods_register.copy(),
            current_date=self.date
        )

# ========== ANALYSIS ==========
    def parse_str_to_date(self, date_str):
        return datetime.datetime.strptime(date_str, self.date_formatter)
