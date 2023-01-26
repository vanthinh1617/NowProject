from flask_restx import Resource
from flask import request
from app.dto.delivery_dto import DeliveryDto
from app.util.helpers import _success, _throw
from app.service.delivery_service import DeliveryService
import inspect, i18n
api = DeliveryDto.api
_searchGlobalField = DeliveryDto.search_global_field

@api.route('/search_global')
@api.expect(_searchGlobalField)
class Delivery(Resource):
    def post(self):
        payload = request.get_json()
        return _success(inspect.stack(), DeliveryService.search_global(payload))



@api.route('/get_infos')
class GetInfo(Resource):
    def post(self):
        pass

@api.route('/get_statistics_by_city_category')
class StatisticalByCityCategory(Resource):
    def post(self):
        pass