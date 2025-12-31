import requests
import base64

# API endpoint and credentials
BASE_URL = "https://ua4t4so3ba.execute-api.eu-west-2.amazonaws.com/prod/v2/custom-objects/contract"
USERNAME = "custom.integrations+olisystems_user@velaris.io"
PASSWORD = "hja*NMD1upu_ubn!xne"
LIMIT = 100

def get_auth_header(username, password):
    token = f"{username}:{password}"
    encoded = base64.b64encode(token.encode()).decode()
    return {"Authorization": f"Basic {encoded}"}

def fetch_all_contract():
    all_contract = []
    after = None

    while True:
        params = {"limit": LIMIT}
        if after is not None:
            params["after"] = after

        headers = get_auth_header(USERNAME, PASSWORD)
        response = requests.get(BASE_URL, headers=headers, params=params)
        response.raise_for_status()

        data = response.json()


        # Extract contracts from 'data' key
        contract = data.get("data", [])
        all_contract.extend(contract)

        # Pagination: check if there's a next page using 'pagination' key
        pagination = data.get("pagination", {})
        after = pagination.get("after")
        if not after:
            print("No more pages to fetch.")
            break
        print(f"Fetched {len(contract)} contracts, total so far: {len(all_contract)}")
    return all_contract

def fetch_contract_by_external_id(external_id, token=None, include_links=True):
    url = f"https://ua4t4so3ba.execute-api.eu-west-2.amazonaws.com/prod/custom-objects/contract/extid-{external_id}"
    params = {}
    if include_links:
        params["include"] = "links"
    headers = get_auth_header(USERNAME, PASSWORD)
    if token:
        headers["x-velaris-internal-token"] = token
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

# Example usage:
# contract_data = fetch_contract_by_external_id("8001W000003wKeWQAU", token="your_token_here")
# print(contract_data)

if __name__ == "__main__":
    contract = fetch_all_contract()
    print(f"Fetched {len(contract)} contract.")
    external_ids = [c.get("externalId") for c in contract if "externalId" in c]
    print("External IDs:", external_ids)
    # Optionally, save to a file:
    # import json
    # with open("all_contract.json", "w") as f:
    #     json.dump(contract, f, indent=2)