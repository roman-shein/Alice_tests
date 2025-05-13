from flask import Flask, request
import logging
import json
from geo import get_country, get_distance, get_coordinates

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, filename='app.log', format='%(asctime)s %(levelname)s %(name)s %(message)s')

@app.route('/post', methods=['POST'])
def main():

    logging.info('Request: %r', request.json)

    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    handle_dialog(response, request.json)

    logging.info('Request: %r', response)

    return json.dumps(response)


def handle_dialog(res, req):

    user_id = req['session']['user_id']

    if req['session']['new']:

        res['response']['text'] = 'РџСЂРёРІРµС‚! РЇ РјРѕРіСѓ СЃРєР°Р·Р°С‚СЊ РІ РєР°РєРѕР№ СЃС‚СЂР°РЅРµ РіРѕСЂРѕРґ РёР»Рё СЃРєР°Р·Р°С‚СЊ СЂР°СЃСЃС‚РѕСЏРЅРёРµ РјРµР¶РґСѓ РіРѕСЂРѕРґР°РјРё!'

        return

    cities = get_cities(req)

    if len(cities) == 0:

        res['response']['text'] = 'РўС‹ РЅРµ РЅР°РїРёСЃР°Р» РЅР°Р·РІР°РЅРёРµ РЅРµ РѕРґРЅРѕРіРѕ РіРѕСЂРѕРґР°!'

    elif len(cities) == 1:

        res['response']['text'] = 'РС‚РѕС‚ РіРѕСЂРѕРґ РІ СЃС‚СЂР°РЅРµ - ' + get_country(cities[0])

    elif len(cities) == 2:

        distance = get_distance(get_coordinates(cities[0]), get_coordinates(cities[1]))
        res['response']['text'] = 'Р Р°СЃСЃС‚РѕСЏРЅРёРµ РјРµР¶РґСѓ СЌС‚РёРјРё РіРѕСЂРѕРґР°РјРё: ' + str(round(distance)) + ' РєРј.'

    else:

        res['response']['text'] = 'РЎР»РёС€РєРѕРј РјРЅРѕРіРѕ РіРѕСЂРѕРґРѕРІ!'


def get_cities(req):

    cities = []

    for entity in req['request']['nlu']['entities']:

        if entity['type'] == 'YANDEX.GEO':

            if 'city' in entity['value'].keys():
                cities.append(entity['value']['city'])

    return cities

if __name__ == '__main__':
    app.run()