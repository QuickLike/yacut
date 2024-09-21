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
        raise InvalidAPIUsage(
            ViewMessage.SHORT_NOT_FOUND,
            HTTPStatus.NOT_FOUND
        )
    return jsonify({'url': url_map.original}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def create_url():
    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage(ViewMessage.EMPTY_BODY)
    if 'url' not in data:
        raise InvalidAPIUsage(ViewMessage.URL_REQUIRED)
    try:
        return jsonify(
            URLMap.create(
                data.get('url'),
                data.get('custom_id')
            ).to_dict()
        ), HTTPStatus.CREATED
    except (URLMap.InvalidShort, URLMap.InvalidURL, URLMap.LimitReached) as e:
        raise InvalidAPIUsage(str(e))
