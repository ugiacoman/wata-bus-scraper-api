#!flask/bin/python
from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests
app = Flask(__name__)



@app.route('/', methods=['GET'])
def get_tasks():

    routes = []    
    # Get Green Line Outbound (Outbound means Monticello -> Caf)
    url = 'http://bustime.gowata.org/bustime/wireless/html/eta.jsp?route=GREEN&direction=OUTBOUND&id=1077&showAllBusses=off'
    r = requests.get(url)

    soup = BeautifulSoup(r.text, "html.parser")
    # soup = soup.find( text="MIN")
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    text = text.encode('utf-8')
    text_list = text.split("\n")
    count = 0
    print("")
    print("Monticello -> Caf")
    for line in text_list:
        if "MIN" in line:
            line = line.replace("\xc2\xa0", " ")
            route = {
                    'id': count,
                    'type': "OUTBOUND",
                    'time': line,
                }
            count +=1
            routes.append(route)
        if "DUE" in line:
            route = {
                    'id': count,
                    'type': "OUTBOUND",
                    'time': "DUE",
                }
            count +=1
            routes.append(route)



    '''
    Get Green Line Inbound (Inbound means Sadler -> Monticello)
    '''
    url = 'http://bustime.gowata.org/bustime/wireless/html/eta.jsp?route=GREEN&direction=INBOUND&id=1091&showAllBusses=off'
    r = requests.get(url)


    soup = BeautifulSoup(r.text, "html.parser")
    # soup = soup.find( text="MIN")
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    text = text.encode('utf-8')
    text_list = text.split("\n")
    print("")
    print("Sadler -> Monticello")
    for line in text_list:
        if "MIN" in line:
            line = line.replace("\xc2\xa0", " ")
            route = {
                    'id': count,
                    'type': "INBOUND",
                    'time': line,
                }
            count += 1
            routes.append(route)
        if "DUE" in line:
            route = {
                    'id': count,
                    'type': "INBOUND",
                    'time': "DUE",
                }
            count += 1
            routes.append(route)
    return jsonify({'routes': routes})

if __name__ == '__main__':
    app.run(debug=True)