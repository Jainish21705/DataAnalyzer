import sys
class CustomException(Exception):
    def __init__(self, message,details:sys):
        self.message = message
        _,_,exc = details.exc_info()
        lineno = exc.tb_lineno
        filename = exc.tb_frame.f_code.co_filename
    
    def __str__(self):
        return f"Custom Exception: {self.message} at {self.filename}:{self.lineno}"

        