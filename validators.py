import re

def validate_non_empty(value, field="Value"):
    if not value or not value.strip():
        raise ValueError(f"{field} cannot be empty.")
    return value.strip()

def validate_positive_int(value, field="Value"):
    try:
        value = int(value)
        if value <= 0:
            raise ValueError
        return value
    except:
        raise ValueError(f"{field} must be a positive integer.")

def validate_non_negative_int(value, field="Value"):
    try:
        value = int(value)
        if value < 0:
            raise ValueError
        return value
    except:
        raise ValueError(f"{field} must be a non-negative integer.")

def validate_positive_float(value, field="Value"):
    try:
        value = float(value)
        if value <= 0:
            raise ValueError
        return value
    except:
        raise ValueError(f"{field} must be a positive number.")

def validate_phone(value):
    value = value.strip()
    if value and not re.match(r'^\d{10}$', value):
        raise ValueError("Contact must be 10 digits.")
    return value

def validate_email(value):
    value = value.strip()
    if value and not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
        raise ValueError("Invalid email format.")
    return value
