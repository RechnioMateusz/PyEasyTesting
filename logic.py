import logging
import logging.config

import settings_agent
import files_creator
import test_detector
import linker


class Logic():
    def __init__(self):
        # Initialization of settings and files creator
        self.settings = settings_agent.Settings()
        self.files_creator = files_creator.Files_Creator(
            main_path=self.settings.main_path,
            directories=(
                self.settings.projects_folder,
                self.settings.logs_folder,
            )
        )

        # Setting logging data
        self.settings.update_logging_settings()
        logging.config.fileConfig(self.settings._logging)
        self.logger = logging.getLogger('LOGIC')
        self.settings.set_logger(logger=logging.getLogger('SAGENT'))
        self.files_creator.set_logger(logger=logging.getLogger('FCREATOR'))
        self.settings.log_initialization_info()
        self.files_creator.log_initialization_info(
            directories=(
                self.settings.projects_folder,
                self.settings.logs_folder,
            )
        )
        self.logger.info('Initialization of logic class')

        # Initialization of test detector
        self.detector = test_detector.Test_Detector(
            logger=logging.getLogger('TDETECTOR')
        )

        # Initialization of logic attributes
        self.loading_directory = None
        self.loading_files_register = dict()
        self.testing_modules_register = dict()
        self.testing_classes_register = dict()
        self.testing_methods_register = dict()

    def clear_loading_logic(self):
        self.loading_directory = None
        self.loading_files_register = dict()

    def clear_testing_logic(self):
        self.testing_methods_register = dict()
        self.testing_classes_register = dict()
        self.testing_modules_register = dict()
