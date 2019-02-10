import folium
import pandas
from geopy.geocoders import ArcGIS


def read_and_map(file, year, amount):
    """
    :param file: str
    :param year: str
    :param amount: int
    :return: None

    This function creates an html file, which contains a map with given features
    """

    # read the csv file
    data = pandas.read_csv(file, error_bad_lines=False)
    movies = data['movie']
    years = data['year']
    locations = data['location']

    # get coordinates of movie locations and create a map
    geolocator = ArcGIS(timeout=10)
    mymap = folium.Map()
    fg1 = folium.FeatureGroup(name='Movies_map ' + year)
    counter = 0
    for mv, yr, lc in zip(movies, years, locations):
        if yr == year:
            counter += 1
            if counter <= amount:
                loc = geolocator.geocode(lc)
                if loc != None:
                    fg1.add_child(folium.Marker(location=[loc.latitude, loc.longitude], popup=mv, icon=folium.Icon()))

    # add another population layer to the map
    fg2 = folium.FeatureGroup(name='Population')
    fg2.add_child(folium.GeoJson(data=open('world.json', 'r',
                                           encoding='utf-8-sig').read(),
                                 style_function=lambda x: {'fillColor': 'green'
                                 if x['properties']['POP2005'] < 10000000
                                 else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000
                                 else 'red'}))

    # add layers to the main map and save it as an html file
    mymap.add_child(fg1)
    mymap.add_child(fg2)
    mymap.add_child(folium.LayerControl())
    mymap.save('MyMap.html')


def check_year(inp):
    """
    :param inp: str
    :return: bool
    Returns True if the user input is valid and False otherwise
    """
    try:
        inp = int(inp)
        if inp in range(1874, 2025):
            return True
    except:
        return False


def check_amount(inp):
    """
    :param inp: str
    :return: bool
    """
    try:
        inp = int(inp)
        return True
    except:
        return False


if __name__ == '__main__':
    year = input('Please enter a year (1874-2025): ')
    amount = input("Please enter amount of movies you'd like to see on the map (a big amount of movies can cause\
    problems in proceeding through the program, so choose wisely:) : ")
    if check_year(year) and check_amount(amount):
        read_and_map('locations.csv', year, int(amount))
    else:
        print("Your input was incorrect. Please restart the program again.")

