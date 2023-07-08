import os

import requests as req


def find_shipyard(bearer_token: str, system_symbol: str) -> None:
    # curl 'https://api.spacetraders.io/v2/systems/:systemSymbol/waypoints' \
    # --header 'Authorization: Bearer INSERT_TOKEN_HERE'
    response = req.get(
        url = f"https://api.spacetraders.io/v2/systems/{system_symbol}/waypoints",
        headers = {"Authorization": f"Bearer {bearer_token}"}
    )
    for waypoint in response.json()["data"]:
        for trait in waypoint["traits"]:
            if trait["symbol"] == "SHIPYARD":
                print(waypoint)

def view_available_ships(bearer_token: str, system: str, waypoint: str) -> None:
    # noqa curl 'https://api.spacetraders.io/v2/systems/:systemSymbol/waypoints/:shipyardWaypointSymbol/shipyard' \
    #  --header 'Authorization: Bearer INSERT_TOKEN_HERE'
    response = req.get(
        url = f"https://api.spacetraders.io/v2/systems/{system}/waypoints/{waypoint}/shipyard", # noqa
        headers = {"Authorization": f"Bearer {bearer_token}"}
    )
    for ship in response.json()["data"]["ships"]:
        print(ship)

def purchase_ship(bearer_token: str, waypoint: str) -> None:
    # curl --request POST \
    # --url 'https://api.spacetraders.io/v2/my/ships' \
    # --header 'Authorization: Bearer INSERT_TOKEN_HERE' \
    # --header 'Content-Type: application/json' \
    # --data '{
    # "shipType": "SHIP_MINING_DRONE",
    # "waypointSymbol": ":shipyardWaypointSymbol"
    # }'
    data = {"shipType": "SHIP_MINING_DRONE", "waypointSymbol": waypoint}
    response = req.post(
        url = "https://api.spacetraders.io/v2/my/ships",
        headers = {
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json"
        },
        json = data,
    )
    print(response.json())




if __name__ == "__main__":
    bearer_token = os.getenv("SPACE_TRADERS_BEARER_TOKEN", "No token!")

    # find_shipyard(bearer_token, "X1-KS52")
    # view_available_ships(bearer_token, "X1-KS52", "X1-KS52-23717D")
    purchase_ship(bearer_token, "X1-KS52-23717D")
