#!/usr/bin/python3

import requests

def returncreds():
    ## first I want to grab my credentials
    with open("/home/student/weather.creds", "r") as mycreds:
        creds = mycreds.read()
    ## remove any newline characters from the api_key
    creds = creds.strip("\n")
    return creds

geocreds = returncreds()

print("This app helps you pack for vacation")

print(" ____    ____  ___       ______     ___      .______      ___       ______  __  ___")
print(" \   \  /   / /   \     /      |   /   \     |   _  \    /   \     /      ||  |/  /")
print("  \   \/   / /  ^  \   |  ,----'  /  ^  \    |  |_)  |  /  ^  \   |  ,----'|  '  / ")
print("   \      / /  /_\  \  |  |      /  /_\  \   |   ___/  /  /_\  \  |  |     |    <  ")
print("    \    / /  _____  \ |  `----./  _____  \  |  |     /  _____  \ |  `----.|  .  \ ")
print("     \__/ /__/     \__\ \______/__/     \__\ | _|    /__/     \__\ \______||__|\__\ ")


city_name = input("What town are you visiting")
limit = 5
GEOAPI = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={geocreds}"

# this is our main function
def main():
    ## make a call to NASAAPI with our key
    resp = requests.get(GEOAPI)

    ## strip off json
    new_response = resp.json()

    desc = new_response["weather"][0]["description"]
    temp = new_response["main"]["temp"] 
    fah = (int(temp)) * 1.8 - 459.67
    fah_new = int(fah)
    print("The weather is: ")
    print(f"{desc}")
    print(f"The temperature is: ")
    print(f"{fah_new}")


    if fah_new < 50:
         print("Pack a jack")
    if fah_new < 70 and fah_new > 50 :
         print("Pack some pants and t-shirts")
    if fah_new < 85 and fah_new > 70:
         print("Its time for shorts")
    if fah_new < 100 and fah_new > 85:
        print("Its hot as hell")


if __name__ == "__main__":
    main()

