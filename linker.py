import inspect
import time
from functools import wraps
from queue import Queue

__q = Queue()


def __extract_info(test_method):
    def list_2_reason(test_method, exc_list):
        if(exc_list and exc_list[-1][0] is test_method):
            return exc_list[-1][1]

    if(hasattr(test_method, '_outcome')):
        result = test_method.defaultTestResult()
        test_method._feedErrorsToResult(result, test_method._outcome.errors)

    error = list_2_reason(test_method=test_method, exc_list=result.errors)
    failure = list_2_reason(test_method=test_method, exc_list=result.failures)
    result = not error and not failure

    return {
        'result': result,
        'error': error,
        'failure': failure
    }


def info_sniffer(test_class):
    buffer = dict()

    @wraps(test_class)
    def __test_class_wrapper(*args, **kwargs):
        def __test_modifier(test):
            @wraps(test)
            def __test_wrapper(*args, **kwargs):
                buffer['method'] = test.__name__
                buffer['doc'] = test.__doc__
                start = time.time()
                test(*args, **kwargs)
                stop = time.time()
                buffer['time'] = stop - start

            return __test_wrapper

        def __tear_down_modifier(tearDown):
            @wraps(tearDown)
            def __tear_down_wrapper(*args, **kwargs):
                tearDown(*args, **kwargs)
                info = __extract_info(test_method=args[0])
                buffer['result'] = info['result']
                buffer['error_text'] = info['error']
                buffer['failure_text'] = info['failure']
                __q.put(buffer.copy())
                buffer.clear()

            return __tear_down_wrapper

        attributes = dir(test_class)
        for attribute_name in attributes:
            attribute = getattr(test_class, attribute_name)
            if(inspect.ismethod(attribute) or inspect.isfunction(attribute)):
                if(attribute_name[:4].lower() == 'test'):
                    setattr(
                        test_class, attribute_name,
                        __test_modifier(test=attribute)
                    )
                elif(attribute_name == 'tearDown'):
                    setattr(
                        test_class, attribute_name,
                        __tear_down_modifier(tearDown=attribute)
                    )

        return test_class

    return __test_class_wrapper()


def queue_get():
    return __q.get_nowait()


def queue_empty():
    return __q.empty()
