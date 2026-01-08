import requests
import xmltodict


def fetch_speeds():
    resp = requests.get("https://webservices.umoiq.com/service/publicXMLFeed?command=vehicleLocations&a=ttc")

    if resp.status_code == 200:
        data = xmltodict.parse(resp.content)
        vehicles = data['body']['vehicle']

        trams = {}

        for vehicle in vehicles:
            if len(vehicle["@routeTag"]) == 3 and vehicle["@routeTag"].startswith("5"):
                route = vehicle["@routeTag"]
                if route not in trams:
                    trams[route] = []
                trams[route].append(int(vehicle["@speedKmHr"]))

        return trams
    else:
        print(f"Failed to fetch: {resp.status_code}")


def get_leaderboard(top=5):
    speeds = fetch_speeds()
    
    leaderboard = []
    for route, speeds in speeds.items():
        leaderboard.append((route, sum(speeds) / len(speeds)))
    
    leaderboard.sort(key=lambda x: x[1], reverse=True)
    
    return leaderboard[:top]


def main():
    print(get_leaderboard())


if __name__ == "__main__":
    main()
