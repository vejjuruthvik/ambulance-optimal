from geopy.geocoders import Nominatim
import requests
import folium
import pandas as pd

class Planner:
    def __init__(self) -> None:
        self.sz = 0
        self.router = (256, 256)

    def get_lat_long_from_address(self, address):
        locator = Nominatim(user_agent='myGeocoder')
        location = locator.geocode(address)
        return location.latitude, location.longitude

    def get_directions_response(self, lat1, long1, lat2, long2, mode='drive'):
        url = "https://route-and-directions.p.rapidapi.com/v1/routing"
        key = "d136a898admsh769a12d85806a56p1d0f24jsna19b023692ae"
        host = "route-and-directions.p.rapidapi.com"
        headers = {"X-RapidAPI-Key": key, "X-RapidAPI-Host": host}
        querystring = {"waypoints":f"{str(lat1)},{str(long1)}|{str(lat2)},{str(long2)}","mode":mode}
        response = requests.request("GET", url, headers=headers, params=querystring)
        return response


    def create_map(self, response):
        # use the response
        mls = response.json()['features'][0]['geometry']['coordinates']
        points = [(i[1], i[0]) for i in mls[0]]
        m = folium.Map()
        # add marker for the start and ending points
        for point in [points[0], points[-1]]:
            folium.Marker(point).add_to(m)
        # add the lines
        folium.PolyLine(points, weight=5, opacity=1).add_to(m)
        # create optimal zoom
        df = pd.DataFrame(mls[0]).rename(columns={0:'Lon', 1:'Lat'})[['Lat', 'Lon']]
        sw = df[['Lat', 'Lon']].min().values.tolist()
        ne = df[['Lat', 'Lon']].max().values.tolist()
        m.fit_bounds([sw, ne])
        return m

    def get_vals(self):
        response = self.get_directions_response(52.4013, 4.5425, 52.402, 4.5426)
        print(list(response))
        #m = self.create_map(response)
        return 0
    
    
# plan = Planner()
# map = plan.get_vals()
#map.save('map1.html')
