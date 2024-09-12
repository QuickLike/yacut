from http import HTTPStatus

from flask import jsonify, request

from settings import ViewMessage
from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap


@app.route('/api/id/<short>/', methods=['GET'])
def get_url(short):
    url_map = URLMap.get(short)
    if url_map is None:
        raise InvalidAPIUsage(ViewMessage.ID_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def create_url():
    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage(ViewMessage.EMPTY_BODY)
    if 'url' not in data:
        raise InvalidAPIUsage(ViewMessage.URL_REQUIRED)
    url = data.get('url')
    short = data.get('custom_id')

    url_map, errors = URLMap.create(url, short)
    for error in errors:
        raise InvalidAPIUsage(error)

    return jsonify(
        url_map.to_dict()
    ), HTTPStatus.CREATED
