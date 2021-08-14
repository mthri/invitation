from datetime import datetime

def format_date(date:str):
    return datetime.fromtimestamp(int(date[:10]))