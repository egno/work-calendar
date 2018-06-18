#!/usr/bin/python3

import requests
import sys

URL = "http://localhost:8111/day/"

def isHoliday():
    resp = requests.get(URL)
    result = resp.json()
    return(result.get('holiday', True))

if __name__ == "__main__":
    if isHoliday():
        sys.exit(1)
    else:
        sys.exit(0)

