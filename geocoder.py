from geopy.geocoders import ArcGIS, Nominatim

arcgis = ArcGIS(timeout=100)
nominatim = Nominatim(timeout=100, user_agent='http')
geocoders = [arcgis, nominatim]


def geocode(address):
    try:
        i = 0
        while i < len(geocoders):
            location = geocoders[i].geocode(address)
            if location is not None:
                return location.latitude, location.longitude
            else:
                i += 1
    except:
        return None
