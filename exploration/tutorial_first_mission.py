import os

import requests as req


def view_contracts(bearer_token: str) -> None:
    # curl 'https://api.spacetraders.io/v2/my/contracts' \
    # --header 'Authorization: Bearer INSERT_TOKEN_HERE'
    response = req.get(
        url = "https://api.spacetraders.io/v2/my/contracts",
        headers = {"Authorization": f"Bearer {bearer_token}"}
    )
    print(response.json())

def accept_contract(bearer_token: str, contract_id: str) -> None:
    # curl --request POST \
    # --url 'https://api.spacetraders.io/v2/my/contracts/:contractId/accept' \
    # --header 'Authorization: Bearer INSERT_TOKEN_HERE'
    response = req.post(
        url = f"https://api.spacetraders.io/v2/my/contracts/{contract_id}/accept",
        headers = {"Authorization": f"Bearer {bearer_token}"}
    )
    print(response.json())

if __name__ == "__main__":
    bearer_token = os.getenv("SPACE_TRADERS_BEARER_TOKEN", "No token!")

    view_contracts(bearer_token)
    accept_contract(bearer_token, "clirkqs4m2bj6s60dwa923jj1")
