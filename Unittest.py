import unittest

import request
import service


class ServiceTest(unittest.TestCase):

    def test1(self):
        print(service.get_class_to_prompt())

    def test2(self):
        print(service.get_student_info())

    def test3(self):
        service.log(receiver='测试', message='测试消息')


class RequestTest(unittest.TestCase):

    def test1(self):
        for clas in service.get_class_to_prompt():
            print('*' * 30)
            print(clas.class_name)
            un_reported = request.get_unreported(clas)
            print(un_reported)

    def test2(self):
        for clas in service.get_class_list():
            print('*' * 30)
            print(clas.class_name)
            un_reported = request.get_unreported(clas)
            student_list = service.convert_numbers_to_students(un_reported)
            print(student_list)

    def test3(self):
        print(service.get_finished_class_list())
