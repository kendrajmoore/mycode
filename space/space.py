#!/usr/bin/env python3
"""Returning the location of the ISS in latitude/longitude"""
import requests
import time
import reverse_geocoder as rg
    
URL= "http://api.open-notify.org/iss-now.json"
def main():
    resp= requests.get(URL).json()
    print("CURRENT LOCATION OF THE ISS: ")
    longitude = (resp["iss_position"]["longitude"]) 
    latitude = (resp["iss_position"]["latitude"])
    coords_tuple = (latitude, longitude)
    result = rg.search(coords_tuple)
    city = result[0]['cc']
    stamp = (resp["timestamp"])
    current = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime(stamp))
    print("Long: ", longitude)
    print("Lat: ", latitude)
    print("Country: ", city)
    print("Timestamp: ", current)

if __name__ == "__main__":
    main()

