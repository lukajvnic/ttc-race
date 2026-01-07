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


def main():
    speeds = fetch_speeds()

    for route, speeds in speeds.items():
        print(f"{route}: {sum(speeds) / len(speeds)}")


main()
