import re

username_min_string_length = 5
username_max_string_length = 30

username_regex = "^[a-zA-Z0-9_.-]+$"

def validate(username):
    if not username_min_string_length <= len(username) <= username_max_string_length:
        return False
    
    if not re.match(username_regex, username):
        return False

    return True