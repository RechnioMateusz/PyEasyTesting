import importlib.util
import inspect


class Test_Detector():
    def __init__(self, logger):
        self.logger = logger
        self.logger.info('Initialization of test detector class...')

    def get_module_name(self, module_path):
        module_name = module_path.split('/')[-1]
        module_name = module_name.split('\\')[-1]
        return module_name

    def load_module(self, module_path):
        module_name = self.get_module_name(module_path=module_path)
        spec = importlib.util.spec_from_file_location(
            module_name, module_path
        )
        _module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_module)
        return _module

    def is_python_module(self, module_name):
        is_python_module = ('.py' in module_name or '.pyw' in module_name)
        is_python_module = is_python_module and '.pyc' not in module_name
        return is_python_module

    def is_test_file(self, module_path, del_module=True):
        if(self.is_python_module(module_name=module_path)):
            try:
                _module = self.load_module(module_path=module_path)
            except:
                return 'FAILED'
            else:
                result = hasattr(_module, 'unittest')
                if(del_module is True):
                    del _module
                return result
        else:
            return None

    def get_module_classes(self, _module):
        attributes = dir(_module)
        classes = list()
        for attribute in attributes:
            _object = getattr(_module, attribute)
            if(inspect.isclass(_object)):
                classes.append(_object)
        return classes

    def get_class_methods(self, _class):
        attributes = dir(_class)
        methods = list()
        for attribute in attributes:
            _object = getattr(_class, attribute)
            if(inspect.ismethod(_object) or inspect.isfunction(_object)):
                methods.append(_object)
        return methods

    def is_test_class(self, _class):
        if(_class.__base__.__name__ == 'TestCase'):
            return True
        else:
            return False

    def is_test_method(self, _method):
        if(_method.__name__[:4].lower() == 'test'):
            return True
        else:
            return False
