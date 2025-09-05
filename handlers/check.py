async def check_phone(phone):
    if not phone.startswith("+998"):
        return False
    if not len(phone) == 13:
        return False
    return True

async def location_check(latitude, longitude):

    # O'zbekistonning taxminiy geografik chegaralari
    min_lat = 37.18   # eng janubiy nuqta
    max_lat = 45.58   # eng shimoliy nuqta
    min_lon = 55.97   # eng g‘arbiy nuqta
    max_lon = 73.15   # eng sharqiy nuqta

    return min_lat <= latitude <= max_lat and min_lon <= longitude <= max_lon
