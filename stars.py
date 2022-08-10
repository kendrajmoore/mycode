#!/usr/bin/python3

import requests


print("Do you want to see planets[0], people[1], or starships[2]?")
para = "people"
answer = input("Enter 0, 1, 2")
if answer == 0:
    para = "planets"
if answer == 1:
    para = "people"
if answer == 2:
    para = "starships"


def build_api_url(book_id, format, token):
    return f"{BASE_URL}/api/v1/book/{book_id}?format={format}&token={token}":

API = "https://swapi.dev/api/{para}/1"
print(API)


# this is our main function
def main():
    ## first grab credentials

    ## make a call to NASAAPI with our key
    apodresp = requests.get(API)

    ## strip off json
    apod = apodresp.json()

    print(apod)


if __name__ == "__main__":
    main()
