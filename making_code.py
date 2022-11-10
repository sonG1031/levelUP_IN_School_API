import random
import string

def rand_code():
    n = 10  # 문자의 개수(문자열의 크기)
    school_code = ""

    for i in range(n):
        school_code += str(random.choice(string.ascii_letters + string.digits))

    class_code = school_code

    for i in range(n):
        class_code += str(random.choice(string.ascii_letters + string.digits))

    return [school_code, class_code]

def make_qr():
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    num = string.digits

    all = lower + upper + num
    tmp = random.sample(all, 15)
    code = r"".join(tmp)
    return code

# qV8ugGBVT3Ditm0VxXbu
# ['7TokPeTWfH', '7TokPeTWfHPxbZNLikCy']
# ['J605kkDwTe', 'J605kkDwTee6sVDwV8GE']
# ['sJVuOVg20a', 'sJVuOVg20aElZurkds1O']
#
# from api.models import *
# from api import db
# s = School(school_code='qV8ugGBVT3', school_name='한양공업고등학교')
# c = SchoolClass(school_code='qV8ugGBVT3', class_code='qV8ugGBVT3Ditm0VxXbu', class_name="2컴넷B")
# s1 = School(school_code='7TokPeTWfH', school_name='test_school1')
# s2 = School(school_code='J605kkDwTe', school_name='test_school2')
# s3 = School(school_code='sJVuOVg20a', school_name='test_school3')
# c1 = SchoolClass(school_code='7TokPeTWfH', class_code='7TokPeTWfHPxbZNLikCy', class_name="3학년 1반")
# c2 = SchoolClass(school_code='J605kkDwTe', class_code='J605kkDwTee6sVDwV8GE', class_name="3학년 2반")
# c3 = SchoolClass(school_code='sJVuOVg20a', class_code='sJVuOVg20aElZurkds1O', class_name="3학년 3반")
# db.session.add(s)
# db.session.add(c)
# db.session.add(s1)
# db.session.add(s2)
# db.session.add(s3)
# db.session.add(c1)
# db.session.add(c2)
# db.session.add(c3)
# db.session.commit()

