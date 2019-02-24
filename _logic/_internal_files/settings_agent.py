import datetime
import sys
import os
import configparser


class Settings():
    def __init__(self):
        self.main_path = sys.path[0]
        self._settings = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), 'settings.ini'
        )
        self._logging = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), '_logging.ini'
        )

        # Configuration file loading
        self.__config_parser = configparser.ConfigParser()
        self.__config_parser.read(filenames=self._settings)

        # Current date loading
        self.current_date_object = datetime.datetime.now()
        self.current_year = self.current_date_object.year
        self.current_month = self.current_date_object.month
        self.current_day = self.current_date_object.day
        self.current_date = self.current_date_object.strftime(
            '%H:%M:%S-%d/%m/%Y'
        )

        # System detecting
        self.current_platform = sys.platform
        self.current_platform_prefix = self.current_platform[:3]

        # Paths loading
        self.projects_folder = self.__config_parser.get('PATHS', 'projects')
        self.logs_folder = self.__config_parser.get('PATHS', 'logs')

        # Date update
        if(
            self.current_year != self.__config_parser.get('DATE', 'year') or
            self.current_month != self.__config_parser.get('DATE', 'month') or
            self.current_day != self.__config_parser.get('DATE', 'day')
        ):
            self.__config_parser.set('DATE', 'year', str(self.current_year))
            self.__config_parser.set('DATE', 'month', str(self.current_month))
            self.__config_parser.set('DATE', 'day', str(self.current_day))

        # System platform update
        if(
            self.__config_parser.get('SYSTEM', 'platform') !=
                self.current_platform
           ):
            self.__config_parser.set(
                'SYSTEM', 'platform', self.current_platform
            )

        # Save changes
        with open(self._settings, 'w') as settings_file:
            self.__config_parser.write(settings_file)

    def set_logger(self, logger):
        self.logger = logger

    def update_logging_settings(self):
        logging_date = self.current_date_object.strftime('%d_%m_%Y')
        path = os.path.join(self.main_path, self.logs_folder, logging_date)
        logging_config_parser = configparser.ConfigParser()
        logging_config_parser.read(filenames=self._logging)
        new_args = '(\'{:s}.log\', \'a\')'.format(path)
        new_args = new_args.replace(chr(92), '/')
        logging_config_parser.set('handler_file_stream', 'args', new_args)
        with open(self._logging, 'w') as logging_file:
            logging_config_parser.write(logging_file)
        logging_config_parser.clear()

    def log_initialization_info(self):
        self.logger.info('Initialization of settings agent')
        self.logger.info('Main path: {:s}'.format(self.main_path))
        self.logger.info('Settings path: {:s}'.format(self._settings))
        self.logger.info('Logging settings path: {:s}'.format(self._logging))
        self.logger.info('Current date: {:s}'.format(self.current_date))
        self.logger.info('Current platform: {:s}'.format(
            self.current_platform
        ))
        self.logger.info('Projects folder: {:s}'.format(self.projects_folder))
        self.logger.info('Logs folder: {:s}'.format(self.logs_folder))
