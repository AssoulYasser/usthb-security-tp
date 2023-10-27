import datetime

def is_case_1(s):
    if len(s) != 3:
        return False
    
    if all(char in '01' for char in s):
        return True
    else:
        return False

def is_case_2(s):
    return s.isdigit() and len(s) == 5

def is_case_3(s):
    if len(s) != 5:
        return False

    for char in s:
        if(ord(char) not in range(32, 128)):
            return False
    return True

def dict_password_1_case(password):
    for character in password:
        if character != '0' and character != '1':
            return 
        
    dic = open('./tp1/password_dicts/combinaisons_3.txt', mode="r")
    itterations = 0
    estimated_time = datetime.datetime.now()
    for mot in dic:
        mot = mot.strip()
        itterations += 1
        if mot == password:
            dic.close()
            return {"found": True, "iterations": itterations, "estimated_time": (datetime.datetime.now() - estimated_time).total_seconds()}
    return {"found": False, "iterations": itterations, "estimated_time": (datetime.datetime.now() - estimated_time).total_seconds()}

def dict_password_2_case(password):
    if len(password) != 5 and password.isdigit() == False : 
        return
    
    dic = open('./tp1/password_dicts/combinations_5.txt', mode="r")
    itterations = 0
    estimated_time = datetime.datetime.now()
    for mot in dic:
        mot = mot.strip()
        itterations += 1
        if mot == password:
            dic.close()
            return {"found": True, "iterations": itterations, "estimated_time": (datetime.datetime.now() - estimated_time).total_seconds()}
    return {"found": False, "iterations": itterations, "estimated_time": (datetime.datetime.now() - estimated_time).total_seconds()}

def force_brut_password_3_case(password):
    pwd = ''
    estimated_time = datetime.datetime.now()
    itterations = 0
    for character in password:
        x = 32
        while x < 127:
            itterations += 1
            if x == ord(character):
                pwd = pwd + chr(x)
                break
            x += 1
        else:
            return {"found": False, "iterations": itterations, "estimated_time": (datetime.datetime.now() - estimated_time).total_seconds()}
    return {"found": True, "iterations": itterations, "estimated_time": (datetime.datetime.now() - estimated_time).total_seconds()}
