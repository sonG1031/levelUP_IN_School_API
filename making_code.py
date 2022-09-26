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