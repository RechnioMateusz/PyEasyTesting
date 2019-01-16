import json


def save_project(project_name, tests_paths):
    project = dict()
    project['name'] = project_name
    project['tests'] = list()
    for test_name, test_path in tests_paths.items():
        # test_name = test_name.split('-')[-1]
        project['tests'].append(
            {
                'file': test_name,
                'path': test_path,
            }
        )
    file_name = '{:s}.json'.format(project_name)
    with open(file_name, 'w') as project_file:
        json.dump(project, project_file)


def get_file_from_path(path):
    last_dir = path.split('/')[-1]
    last_dir = last_dir.split('\\')[-1]
    return last_dir
