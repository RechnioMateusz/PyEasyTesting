import importlib.util


class Test_Detector():
    def __init__(self, logger):
        self.logger = logger

    def __load_module(self, module_path):
        module_name = module_path.split('/')[-1]
        module_name = module_name.split('\\')[-1]
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
                _module = self.__load_module(module_path=module_path)
            except:
                return 'FAILED'
            else:
                result = hasattr(_module, 'unittest')
                if(del_module is True):
                    del _module
                return result
        else:
            return None

    def is_test_class(self):
        pass

    def is_test_method(self):
        pass
