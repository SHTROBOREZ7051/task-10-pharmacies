import requests
import math


def lonlat_distance(a, b):

    degree_to_meters_factor = 111 * 1000 # 111 километров в метрах
    a_lon, a_lat = a
    b_lon, b_lat = b

    # Берем среднюю по широте точку и считаем коэффициент для нее.
    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)

    # Вычисляем смещения в метрах по вертикали и горизонтали.
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor

    # Вычисляем расстояние между точками.
    distance = math.sqrt(dx * dx + dy * dy)
    
    return distance


search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"


spn = input("Введите широту: ")
spn1 = input("Введите долготу: ")
#address_ll = "37.588392,55.734036"
address_ll = f"{spn1},{spn}"

search_params = {
    "apikey": api_key,
    "text": "Аптека",
    "lang": "ru_RU",
    "ll": address_ll,
    "type": "biz"
}
address_llInt = tuple(map(float, address_ll.split(",")))
response = requests.get(search_api_server, params=search_params)
if not response:
    pass

json_response = response.json()

organization = json_response["features"][:]
coords = sorted(organization, key=lambda x: lonlat_distance(x["geometry"]["coordinates"], address_llInt))
if len(coords) >= 10:
    coords = coords[:10]

stringCoordsAndTime = ""

for i in coords:
    cr = i['geometry']['coordinates']
    stringCoordsAndTime = stringCoordsAndTime + f"{cr[0]},{cr[1]}"
    shift = i['properties']['CompanyMetaData']['Hours']['text']
    if shift == "":
        stringCoordsAndTime = stringCoordsAndTime + ",pm2grm"
    elif "круглосуточно" in shift:
        stringCoordsAndTime = stringCoordsAndTime + ",pm2gnm"
    else:
        stringCoordsAndTime = stringCoordsAndTime + ",pm2blm"
    stringCoordsAndTime = stringCoordsAndTime + "~"
    
stringCoordsAndTime = stringCoordsAndTime[:-1]
delta = "0.025"

map_params = {
    "ll": address_ll,
    "spn": ",".join([delta, delta]),
    "l": "map",
    "pt": f"{address_ll},ya_ru~{stringCoordsAndTime}"
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)
mapName = "image.png"
with open(mapName, "wb") as img:
    img.write(response.content)