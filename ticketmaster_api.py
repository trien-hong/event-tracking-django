import os
import requests
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


def getEvents(parameter):
    TICKERTMASTER_API_KEY = os.getenv("TICKETMASTER_API_KEY")

    if len(parameter) == 5 and parameter.isnumeric():
        url = (
            "https://app.ticketmaster.com/discovery/v2/events?apikey=" + TICKERTMASTER_API_KEY + "&postalCode=" + parameter + "&locale=*"
        )

        ticketmaster_request = requests.get(url=url)

        ticketmaster_response_json = ticketmaster_request.json()

        if "page" in ticketmaster_response_json:
            if "totalElements" in ticketmaster_response_json["page"]:
                if ticketmaster_response_json["page"]["totalElements"] == 0:
                    return False

        idList = []
        nameList = []
        imageList = []
        dateList = []
        cityList = []
        minPriceList = []
        maxPriceList = []
        
        if "_embedded" in ticketmaster_response_json:
            if "events" in ticketmaster_response_json["_embedded"]:
                index = 0
                for x in ticketmaster_response_json["_embedded"]["events"]:
                    idList.append(x["id"])
                    
                    if "name" in ticketmaster_response_json["_embedded"]["events"][index]:
                        nameList.append(x["name"])
                    else:
                        nameList.append("TBD")
                    
                    if "images" in ticketmaster_response_json["_embedded"]["events"][index]:
                        if "url" in ticketmaster_response_json["_embedded"]["events"][index]["images"][0]:
                            imageList.append(x["images"][0]["url"])
                    else:
                        imageList.append("TBD")

                    if "dates" in ticketmaster_response_json["_embedded"]["events"][index]:
                        if "start" in ticketmaster_response_json["_embedded"]["events"][index]["dates"]:
                            if "localDate" in ticketmaster_response_json["_embedded"]["events"][index]["dates"]["start"]:
                                dateList.append(x["dates"]["start"]["localDate"])
                    else:
                        dateList.append("TBD")
                    
                    if "_embedded" in ticketmaster_response_json["_embedded"]["events"][index]:
                        if "venues" in ticketmaster_response_json["_embedded"]["events"][index]["_embedded"]:
                            if "city" in ticketmaster_response_json["_embedded"]["events"][index]["_embedded"]["venues"][0]:
                                if "name" in ticketmaster_response_json["_embedded"]["events"][index]["_embedded"]["venues"][0]["city"]:
                                    cityList.append(x["_embedded"]["venues"][0]["city"]["name"])
                    else:
                        cityList.append("TBD")

                    if "priceRanges" in ticketmaster_response_json["_embedded"]["events"][index]:
                        if "min" in ticketmaster_response_json["_embedded"]["events"][index]["priceRanges"][0]:
                            minPriceList.append("$" + str(x["priceRanges"][0]["min"]))
                    else:
                        minPriceList.append("TBD")

                    if "priceRanges" in ticketmaster_response_json["_embedded"]["events"][index]:
                        if "max" in ticketmaster_response_json["_embedded"]["events"][index]["priceRanges"][0]:
                            maxPriceList.append("$" + str(x["priceRanges"][0]["max"]))
                    else:
                        maxPriceList.append("TBD")

        return zip(idList, nameList, imageList, dateList, cityList, minPriceList, maxPriceList)