import networkx as nx
import osmnx as ox
from geopy.geocoders import Nominatim
from random import randint
from os.path import exists
#ox.config(use_cache=True, log_console=True)
geolocator = Nominatim(user_agent="geoapiExercises")

class Bus():
    number = randint(1, 300)
    passangers_count = randint(1, 40)

class Station():
    number = randint(1, 200)

class Route(object):
    transport = ""
    G = None
    orig = None
    des = None
    length = None
    travel_time = None

    def get_map(self):
        if exists("Kiyv.graphml"):
            self.G = ox.load_graphml("Kiyv.graphml")
        else:
            self.G = ox.graph_from_place("Ukraine, Kyiv", network_type=self.transport)
            self.G = ox.add_edge_speeds(self.G)
            self.G = ox.add_edge_travel_times(self.G)
            ox.save_graphml(self.G, "Kiyv.graphml")
        return

    def get_short_path(self):
        start_node = get_node_from_string(self.orig)
        end_node = get_node_from_string(self.des)
        route = nx.shortest_path(self.G, start_node, end_node, 'travel_time')
        self.length = nx.shortest_path_length(self.G, source=start_node, target=end_node, weight=None, method='dijkstra')
        self.travel_time = self.length/0.5
        route_map = ox.plot_route_folium(self.G, route)
        route_map.save("index.html")
        return


class Bike_Route(Route):
    transport = "bike"

class Foot_Route(Route):
    transport = "foot"

class Drive_Route(Route):
    transport = "drive"
    buses = {}
    stations = {}
    path = ""

    def __init__(self):
        for i in range(randint(2, 3)):
            self.buses["bus_{0}".format(i)] = Bus()
        for i in range(len(self.buses)+1):
            self.stations["Station_{0}".format(i)] = Station()
        for i in range(len(self.buses)):
            if i+1 != len(self.buses):
                self.path += f"Station_{self.stations['Station_{0}'.format(i)].number}, Bus_{self.buses['bus_{0}'.format(i)].number} -> "
            else:
                self.path += f"Station_{self.stations['Station_{0}'.format(i)].number}"

class RouteFactory():
    def create_route(self, typ):
        return globals()[typ]()

def get_node_from_string(query_place: str):
    location = geolocator.geocode(query_place)
    print(f"target: {location} - ({location.longitude}, {location.latitude})")
    return ox.nearest_nodes(mroute.G, location.longitude, location.latitude)


if __name__ == "__main__":
    print("Виберіть тип пересування:\n1. Автобус/Машина\n2. Велосипед\n3. Пішки\n - ", end="")
    while(True):
        try:
            choise = int(input())
            if 3 <= choise >= 1:
                print("Введіть від 1 до 10!")
                continue
            else:
                break
        except:
            print("Спробуйте ще раз!")
            continue
    route_obj = RouteFactory()
    if choise == 1:
        mroute = route_obj.create_route("Drive_Route")
    elif choise == 2:
        mroute = route_obj.create_route("Bike_Route")
    else:
        mroute = route_obj.create_route("Foot_Route")
    temp = []
    for i in range(2):
        while(True):
            try:
                print(i)
                if i == 0:
                    print("Введіть місце відправки: ", end="")
                else:
                    print("Введіть місце призначення: ", end="")
                temp.append(input())
                break
            except:
                print("Спробуйте ще раз!")
                continue
    mroute.orig = temp[0]
    mroute.des = temp[1]
    mroute.get_map()
    mroute.get_short_path()
    if choise == 1:
        print(f"Ваш шлях: {mroute.path}")
    print(f"Довжина шляху: {mroute.length} км\nТривалість шляху {mroute.travel_time} хв")

