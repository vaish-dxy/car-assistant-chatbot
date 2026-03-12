import re

def extract_attributes(query):

    query = query.lower()

    attributes = {
        "fuel": None,
        "type": None,
        "price": None
    }

    # detect fuel type
    if "petrol" in query:
        attributes["fuel"] = "petrol"

    elif "diesel" in query:
        attributes["fuel"] = "diesel"

    elif "electric" in query:
        attributes["fuel"] = "electric"

    # detect vehicle type
    if "suv" in query:
        attributes["type"] = "suv"

    elif "sedan" in query:
        attributes["type"] = "sedan"

    elif "hatchback" in query:
        attributes["type"] = "hatchback"

    # detect price like "15 lakh"
    price_match = re.search(r"(\d+)\s*lakh", query)

    if price_match:
        attributes["price"] = int(price_match.group(1)) * 100000

    return attributes