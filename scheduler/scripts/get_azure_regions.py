# type: ignore
import os

import httpx

USERNAME = os.getenv("WATTTIME_USERNAME")
PASSWORD = os.getenv("WATTTIME_PASSWORD")

# Azure region coordinate data
azure_regions = {
    "eastus": {"Latitude": "37.3719", "Longitude": "-79.8164", "Name": "eastus"},
    "eastus2": {"Latitude": "36.6681", "Longitude": "-78.3889", "Name": "eastus2"},
    "southcentralus": {"Latitude": "29.4167", "Longitude": "-98.5", "Name": "southcentralus"},
    "westus2": {"Latitude": "47.233", "Longitude": "-119.852", "Name": "westus2"},
    "westus3": {"Latitude": "33.448376", "Longitude": "-112.074036", "Name": "westus3"},
    "australiaeast": {"Latitude": "-33.86", "Longitude": "151.2094", "Name": "australiaeast"},
    "southeastasia": {"Latitude": "1.283", "Longitude": "103.833", "Name": "southeastasia"},
    "northeurope": {"Latitude": "53.3478", "Longitude": "-6.2597", "Name": "northeurope"},
    "swedencentral": {"Latitude": "60.67488", "Longitude": "17.14127", "Name": "swedencentral"},
    "uksouth": {"Latitude": "50.941", "Longitude": "-0.799", "Name": "uksouth"},
    "westeurope": {"Latitude": "52.3667", "Longitude": "4.9", "Name": "westeurope"},
    "centralus": {"Latitude": "41.5908", "Longitude": "-93.6208", "Name": "centralus"},
    "southafricanorth": {
        "Latitude": "-25.73134",
        "Longitude": "28.21837",
        "Name": "southafricanorth",
    },
    "centralindia": {"Latitude": "18.5822", "Longitude": "73.9197", "Name": "centralindia"},
    "eastasia": {"Latitude": "22.267", "Longitude": "114.188", "Name": "eastasia"},
    "japaneast": {"Latitude": "35.68", "Longitude": "139.77", "Name": "japaneast"},
    "koreacentral": {"Latitude": "37.5665", "Longitude": "126.978", "Name": "koreacentral"},
    "canadacentral": {"Latitude": "43.653", "Longitude": "-79.383", "Name": "canadacentral"},
    "francecentral": {"Latitude": "46.3772", "Longitude": "2.373", "Name": "francecentral"},
    "germanywestcentral": {
        "Latitude": "50.110924",
        "Longitude": "8.682127",
        "Name": "germanywestcentral",
    },
    "italynorth": {"Latitude": "45.46888", "Longitude": "9.18109", "Name": "italynorth"},
    "norwayeast": {"Latitude": "59.913868", "Longitude": "10.752245", "Name": "norwayeast"},
    "polandcentral": {"Latitude": "52.23334", "Longitude": "21.01666", "Name": "polandcentral"},
    "spaincentral": {"Latitude": "40.4259", "Longitude": "3.4209", "Name": "spaincentral"},
    "mexicocentral": {"Latitude": "20.588818", "Longitude": "-100.389888", "Name": "mexicocentral"},
    "brazilsouth": {"Latitude": "-23.55", "Longitude": "-46.633", "Name": "brazilsouth"},
    "eastus2euap": {"Latitude": "36.6681", "Longitude": "-78.3889", "Name": "eastus2euap"},
    "israelcentral": {"Latitude": "31.2655698", "Longitude": "33.4506633", "Name": "israelcentral"},
    "qatarcentral": {"Latitude": "25.551462", "Longitude": "51.439327", "Name": "qatarcentral"},
    "brazilus": {"Latitude": "0", "Longitude": "0", "Name": "brazilus"},
    "eastusstg": {"Latitude": "37.3719", "Longitude": "-79.8164", "Name": "eastusstg"},
    "northcentralus": {"Latitude": "41.8819", "Longitude": "-87.6278", "Name": "northcentralus"},
    "westus": {"Latitude": "37.783", "Longitude": "-122.417", "Name": "westus"},
    "jioindiawest": {"Latitude": "22.470701", "Longitude": "70.05773", "Name": "jioindiawest"},
    "switzerlandnorth": {
        "Latitude": "47.451542",
        "Longitude": "8.564572",
        "Name": "switzerlandnorth",
    },
    "uaenorth": {"Latitude": "25.266666", "Longitude": "55.316666", "Name": "uaenorth"},
    "centraluseuap": {"Latitude": "41.5908", "Longitude": "-93.6208", "Name": "centraluseuap"},
    "westcentralus": {"Latitude": "40.89", "Longitude": "-110.234", "Name": "westcentralus"},
    "southafricawest": {
        "Latitude": "-34.075691",
        "Longitude": "18.843266",
        "Name": "southafricawest",
    },
    "australiacentral": {
        "Latitude": "-35.3075",
        "Longitude": "149.1244",
        "Name": "australiacentral",
    },
    "australiacentral2": {
        "Latitude": "-35.3075",
        "Longitude": "149.1244",
        "Name": "australiacentral2",
    },
    "australiasoutheast": {
        "Latitude": "-37.8136",
        "Longitude": "144.9631",
        "Name": "australiasoutheast",
    },
    "japanwest": {"Latitude": "34.6939", "Longitude": "135.5022", "Name": "japanwest"},
    "jioindiacentral": {
        "Latitude": "21.146633",
        "Longitude": "79.08886",
        "Name": "jioindiacentral",
    },
    "koreasouth": {"Latitude": "35.1796", "Longitude": "129.0756", "Name": "koreasouth"},
    "southindia": {"Latitude": "12.9822", "Longitude": "80.1636", "Name": "southindia"},
    "westindia": {"Latitude": "19.088", "Longitude": "72.868", "Name": "westindia"},
    "canadaeast": {"Latitude": "46.817", "Longitude": "-71.217", "Name": "canadaeast"},
    "francesouth": {"Latitude": "43.8345", "Longitude": "2.1972", "Name": "francesouth"},
    "germanynorth": {"Latitude": "53.073635", "Longitude": "8.806422", "Name": "germanynorth"},
    "norwaywest": {"Latitude": "58.969975", "Longitude": "5.733107", "Name": "norwaywest"},
    "switzerlandwest": {
        "Latitude": "46.204391",
        "Longitude": "6.143158",
        "Name": "switzerlandwest",
    },
    "ukwest": {"Latitude": "53.427", "Longitude": "-3.084", "Name": "ukwest"},
    "uaecentral": {"Latitude": "24.466667", "Longitude": "54.366669", "Name": "uaecentral"},
    "brazilsoutheast": {
        "Latitude": "-22.90278",
        "Longitude": "-43.2075",
        "Name": "brazilsoutheast",
    },
}


def get_token(username, password):
    login_url = "https://api.watttime.org/login"
    rsp = httpx.get(login_url, auth=(username, password))
    rsp.raise_for_status()
    return rsp.json()["token"]


def get_accessible_regions(token):
    url = "https://api.watttime.org/v3/my-access"
    headers = {"Authorization": f"Bearer {token}"}
    response = httpx.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()

    regions = data["signal_types"][0]["regions"]
    return [region["region"] for region in regions]


def get_grid_region(token, lat, lon):
    url = "https://api.watttime.org/v3/region-from-loc"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"latitude": lat, "longitude": lon, "signal_type": "co2_moer"}
    response = httpx.get(url, headers=headers, params=params)
    if response.status_code == httpx.codes.OK:
        return response.json().get("region")
    else:
        print(f"Failed to find region for ({lat}, {lon}): {response.status_code} {response.text}")
        return None


def main():
    token = get_token(USERNAME, PASSWORD)
    accessible_regions = get_accessible_regions(token)

    print("Azure regions with access to co2_moer grid regions:")
    region_map = {}
    for name, coords in azure_regions.items():
        lat = float(coords["Latitude"])
        lon = float(coords["Longitude"])
        grid_region = get_grid_region(token, lat, lon)

        if grid_region in accessible_regions:
            region_map[name] = grid_region

    print(region_map)
    print(list(region_map.keys()))


if __name__ == "__main__":
    main()
