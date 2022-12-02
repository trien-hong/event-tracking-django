import os
import requests
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


def getEvents(input):
    TICKERTMASTER_API_KEY = os.getenv("TICKETMASTER_API_KEY")

    if len(input) == 5 and input.isnumeric():
        url = (
            "https://app.ticketmaster.com/discovery/v2/events?apikey=" + TICKERTMASTER_API_KEY + "&postalCode=" + input + "&locale=*"
        )
    else:
        url = (
            "https://app.ticketmaster.com/discovery/v2/events?apikey=" + TICKERTMASTER_API_KEY + "&keyword=" + input + "&locale=*"
        )

    ticketmaster_request = requests.get(url=url)

    ticketmaster_response_json = ticketmaster_request.json()

    idList = []
    titleList = []
    imageList = []
    dateList = []
    cityList = []
    minPriceList = []
    maxPriceList = []

    try:
        for x in ticketmaster_response_json["_embedded"]["events"]:
            try:
                idList.append(x["id"])
            except KeyError as e:
                idList.append("TBD")

            try:
                titleList.append(x["name"])
            except KeyError as e:
                titleList.append("TBD")
            
            try:
                imageList.append(x["images"][0]["url"])
            except KeyError as e:
                imageList.append("TBD")

            try:
                dateList.append(x["dates"]["start"]["localDate"])
            except KeyError as e:
                dateList.append("TBD")

            try:
                cityList.append(x["_embedded"]["venues"][0]["city"]["name"])
            except KeyError as e:
                cityList.append("TBD")
            
            try:
                minPriceList.append("$" + str(x["priceRanges"][0]["min"]))
            except KeyError as e:
                minPriceList.append("TBD")

            try:
                maxPriceList.append("$" + str(x["priceRanges"][0]["max"]))
            except KeyError as e:
                maxPriceList.append("TBD")
    except KeyError as e:
        return False

    return zip(idList, titleList, imageList, dateList, cityList, minPriceList, maxPriceList)