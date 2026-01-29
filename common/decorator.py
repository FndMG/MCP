import functools
import logging
import inspect

def log_function_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__

        sig = inspect.signature(func)
        param_names = list(sig.parameters.keys())

        log_arg_list = []

        start_index = 0
        if param_names and param_names[0] == "self" and args:
            start_index = 1

        pos_args = args[start_index:]
        pos_names = param_names[start_index : len(pos_args) + start_index]

        for name, val in zip(pos_names, pos_args):
            log_arg_list.append(f"{name}={repr(val)}")
        for name, val in kwargs.items():
            log_arg_list.append(f"{name}={repr(val)}")

        logging.info(f"Request received: {func_name}({', '.join(log_arg_list)})")

        return func(*args, **kwargs)

    return wrapper
