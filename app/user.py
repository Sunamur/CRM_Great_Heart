
class Person:

    
    def __init__(self, name, birthday, phone, city):
        self.__name = name
        self.__birthday = birthday
        self.__phone = phone
        self.__city = city


# Сотрудник == волонтёр
class Coworker(Person):

    def __init__(self, name, birthday, main_phone, city,
                 work, position, avail, role,
                 email='', messenger='', work_phone='', work_email='',
                 resp='', edu_uni='', edu_spec='', avail_other='',
                 foreign_lang='', hobbies='', other=''):

        super().__init__(name, birthday, main_phone, city)
        self.__role = role
        self.__work = work
        self.__position = position
        self.__avail = avail
        self.__email = email
        self.__messenger = messenger
        self.__work_phone = work_phone
        self.__work_email = work_email
        self.__resp = resp
        self.__edu_uni = edu_uni
        self.__edu_spec = edu_spec
        self.__avail_other = avail_other
        self.__foreign_lang = foreign_lang
        self.__hobbies = hobbies
        self.__other = other


class Pacient(Person):

    def __init__(self, name, birthday, main_phone, city,
                 diagnose, res_phone, messenger, email,
                 profession, hobbies, other, ):

        super().__init__(name, birthday, main_phone, city)
        self.__diagnose = diagnose