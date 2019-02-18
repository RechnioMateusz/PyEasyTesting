import os
import json


class Files_Creator():
    def __init__(self, main_path, directories):
        self.main_path = main_path
        self.directories = directories
        self._create_directories()
        self.logger = None
        self.__dirs_creation_info = str()

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
                    'history': list()
                }
            )
        file_name = '{:s}.json'.format(project_name)
        path = os.path.join(self.main_path, folder, file_name)
        with open(path, 'w') as project_file:
            json.dump(project, project_file)

        self.logger.info(
            'Project \'{:s}\' was succesfully saved'.format(project_name)
        )

    def load_project(self, folder, project_name):
        path = os.path.join(self.main_path, folder, project_name)
        project = None
        with open(path, 'r') as project_file:
            project = json.load(project_file)
        return project

    def get_file_from_path(self, path):
        last_dir = path.split('/')[-1]
        last_dir = last_dir.split('\\')[-1]
        return last_dir

    def _create_directories(self):
        for directory in self.directories:
            path = os.path.join(self.main_path, directory)
            try:
                os.mkdir(path)
            except Exception as ex:
                self.__dirs_creation_info = \
                    'Cannot create directory {:s} with error: {:s}'.format(
                        path, str(ex)
                    )

    def get_existing_projects(self, projects_folder):
        path = os.path.join(self.main_path, projects_folder)
        projects_names = os.listdir(path)
        return projects_names

    def save_results(self, project_name, register, current_date):
        project_name += '.json'
        project = self.load_project(
            folder=self.directories[0], project_name=project_name
        )
        records = list()
        for i in range(len(project['tests'])):
            for key, method_results in register.items():
                if(project['tests'][i]['path'] in key):
                    records.append(method_results)
            new_record = {current_date: records}
            project['tests'][i]['history'].append(new_record)

        new_path = os.path.join(self.directories[0], project_name)
        try:
            with open(new_path, 'w') as project_file:
                json.dump(project, project_file)
        except Exception as ex:
            self.logger.info(
                'Cannot remove old project with error: {:s}'.format(str(ex))
            )
        else:
            self.logger.info(
                'Project \'{:s}\' was succesfully saved'.format(project_name)
            )

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
        self.logger.info(self.__dirs_creation_info)
