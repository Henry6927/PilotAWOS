import requests

def scraperX(ICAO):
    ICAO= str(ICAO)
    data=requests.get("https://aviationweather.gov/cgi-bin/data/metar.php?ids="+ICAO + "&hours=0&order=id%2C-obs&sep=true")
    html=data.text
    if html=='':
        weather="not a valid airport"
    else:
        weather=html
        return weather