from validate_email_address import validate_email
import re, os
from utils.label import * 

CODE_LABLE = dict(zip(LABEL_CODE.values(), LABEL_CODE.keys()))

def isvalidFormatEmail(email):
    pattern = "^\S+@\S+\.\S+$"
    objs = re.search(pattern, email)
    try:
        if objs.string == email:
            return True
    except:
        return False

def check_validate_email(email):

    if isvalidFormatEmail(email):
        isvalid=validate_email(email)
        return isvalid
    return False

def check_exist_and_make(PATH):
    if not os.path.exists(PATH):
        os.makedirs(PATH)

def code2name(code:int):
    try:
        return CODE_LABLE[code]
    except:
        return code