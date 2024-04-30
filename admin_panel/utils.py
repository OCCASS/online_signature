def format_phone_number(phone_number: str) -> str:
    numbers = list(filter(str.isdigit, phone_number))[1:]
    return "+7 ({}{}{}) {}{}{}-{}{}-{}{}".format(*numbers)
