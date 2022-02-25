import math
import geojson
from geojson.feature import FeatureCollection
from itertools import groupby


def length(lat_1, lon_1, lat_2, lon_2):
    lat = (lat_2 - lat_1) * (math.pi / 180)
    lon = (lon_2 - lon_1) * (math.pi / 180)
    answer = math.sin(lat / 2) ** 2 + math.cos(lat_1 * math.pi / 180) * math.cos(lat_2 * math.pi / 180) * (
            math.sin(lon / 2) ** 2)
    return 2 * 6371 * math.atan2(math.sqrt(answer), math.sqrt(1 - answer))


class Data:
    @staticmethod
    def lviv(path):
        loc = []
        with open(path, 'r', encoding='utf-8') as file:
            data = FeatureCollection(geojson.load(file))
            for el in data["features"]:
                try:
                    coords = [float(el["properties"]["y"])] + [float(el["properties"]["x"])]
                    street = f'{el["properties"]["street_type"]} {el["properties"]["street_name"]}, {el["properties"]["housenumber"]}'
                    coords.append(street)
                    loc.append(coords)
                except:
                    pass
        return [el for el, _ in groupby(sorted(loc))]

    def __init__(self):
        self.lst = self.lviv("data/shelter_lviv.geojson")

    def closest(self, point, frm, to):
        try:
            return sorted(self.lst, key=lambda x: length(point[0], point[1], x[0], x[1]))[frm:to]
        except:
            return []
