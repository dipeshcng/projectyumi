from datetime import date, datetime

def calculate_age(born):
    birth = date.fromisoformat(born)
    today = date.today()
    return today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))


#convert Date format from dd/mm/yyyy to yyyy-mm-dd
def convert_date(date):
    input_date = datetime.strptime(date, '%d/%m/%Y')
    output_date = input_date.strftime('%Y-%m-%d')
    return output_date