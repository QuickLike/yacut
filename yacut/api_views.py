from http import HTTPStatus

from flask import jsonify, request

from settings import ViewMessage
from . import app
from .error_handlers import InvalidUsage
from .models import URLMap


@app.route('/api/id/<short>/', methods=['GET'])
def get_url(short):
    url_map = URLMap.get(short)
    if url_map is None:
        raise InvalidUsage(ViewMessage.ID_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def create_url():
    data = request.get_json(silent=True)

    if not data:
        raise InvalidUsage(ViewMessage.EMPTY_BODY)

    if 'url' not in data:
        raise InvalidUsage(ViewMessage.URL_REQUIRED)

    return jsonify(
        URLMap.create(
            data['url'],
            data.get('custom_id', '')
        )[0].to_dict()
    ), HTTPStatus.CREATED
