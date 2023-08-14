from datetime import date

def calculate_age(born):
    birth = date.fromisoformat(born)
    today = date.today()
    return today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))