import os

import requests as req


def register_new_agent() -> None:
    # curl --request POST \
    # --url 'https://api.spacetraders.io/v2/register' \
    # --header 'Content-Type: application/json' \
    # --data '{
    #     "symbol": "INSERT_CALLSIGN_HERE",
    #     "faction": "COSMIC"
    # }'
    data: str = '{"symbol": "YoShi", "faction": "COSMIC"}'
    response = req.post(
        url = "https://api.spacetraders.io/v2/register",
        headers = {"Content-Type": "application/json"},
        data = data,
    )
    print(response.text)

def get_agent_info(bearer_token: str) -> None:
    # curl 'https://api.spacetraders.io/v2/my/agent' \
    # --header 'Authorization: Bearer INSERT_TOKEN_HERE'
    response = req.get(
        url = "https://api.spacetraders.io/v2/my/agent",
        headers = {"Authorization": f"Bearer {bearer_token}"}
    )
    print(response.text)

def view_starting_location(bearer_token: str, system: str, waypoint: str) -> None:
    # noqa curl 'https://api.spacetraders.io/v2/systems/:systemSymbol/waypoints/:waypointSymbol' \
    # --header 'Authorization: Bearer INSERT_TOKEN_HERE'
    response = req.get(
        url = f"https://api.spacetraders.io/v2/systems/{system}/waypoints/{waypoint}",
        headers = {"Authorization": f"Bearer {bearer_token}"}
    )
    print(response.text)

if __name__ == "__main__":
    # register_new_agent()
    get_agent_info(os.getenv("SPACE_TRADERS_BEARER_TOKEN", "No token!"))
    view_starting_location(
        os.getenv("SPACE_TRADERS_BEARER_TOKEN", "No token!"),
        "X1-KS52",
        "X1-KS52-07960X",
    )
