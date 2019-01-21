import os
import json


class Files_Creator():
    def __init__(self, main_path, directories):
        self.main_path = main_path
        self._create_directories(directories=directories)

    def save_project(self, project_name, tests_paths, folder):
        project = dict()
        project['name'] = project_name
        project['tests'] = list()
        for test_name, test_path in tests_paths.items():
            test_name = test_name.split('-')[-1]
            project['tests'].append(
                {
                    'file': test_name,
                    'path': test_path,
                }
            )
        project['history'] = list()
        file_name = '{:s}.json'.format(project_name)
        path = os.path.join(self.main_path, folder, file_name)
        with open(path, 'w') as project_file:
            json.dump(project, project_file)

        self.logger.info(
            'Project \'{:s}\' was succesfully saved'.format(project_name)
        )

    def get_file_from_path(self, path):
        last_dir = path.split('/')[-1]
        last_dir = last_dir.split('\\')[-1]
        return last_dir

    def _create_directories(self, directories):
        for directory in directories:
            path = os.path.join(self.main_path, directory)
            try:
                os.mkdir(path)
            except:
                pass

    def set_logger(self, logger):
        self.logger = logger

    def log_initialization_info(self, directories):
        self.logger.info(
            'Initialization of files creator with path: {:s}'.format(
                self.main_path
            )
        )
        directories_str = str()
        for directory in directories:
            directories_str += '{:s}, '.format(directory)
        directories_str = directories_str[:-2]
        self.logger.info('Creating folders: {:s}'.format(directories_str))
