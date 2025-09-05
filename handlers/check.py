async def check_phone(phone):
    if not phone.startswith("+998"):
        return False
    if not len(phone) == 13:
        return False
    return True