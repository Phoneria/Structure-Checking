# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 16:05:27 2024

@author: ayhan
"""


import traceback
import sys

def get_exception_info():
        exception_type, exception_value, exception_traceback = sys.exc_info()
        file_name, line_number, procedure_name, line_code = traceback.extract_tb(exception_traceback)[-1]
        exception_info=" [File Name]:" + str(file_name)+"\n"+" [Procedure Name]:"+str(procedure_name) +"\n [Error Message]:"+ str(exception_value)+"\n [Error Type]:"+str(exception_type)+"\n [Line Number]:"+str(line_number)+"\n [Line Code]:" + str(line_code)
        return exception_info
    #+"\n"+"[Procedure Name]:"+str(procedure_name) +"\n [Error Message]:"+ str(exception_value)+"\n [Error Type]:"+str(exception_type)+"\n [Line Number]:"+str(line_number)+"\n [Line Code]:" + str(line_code)

if __name__ == '__main__':
    try:
        division = 1/0
    except:
        exception_information= get_exception_info()
        print(exception_information)
    finally:
        pass
