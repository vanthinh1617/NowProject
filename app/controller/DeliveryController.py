from flask_restx import Resource
from app.dto.delivery_dto import DeliveryDto

api = DeliveryDto.api
_searchGlobalField = DeliveryDto.search_global_field

@api.route('/delivery/search_global')
@api.expect(_searchGlobalField)
class Delivery(Resource):
    def post(self):
        pass



@api.route('/delivery/get_infos')
class GetInfo(Resource):
    def post(self):
        pass

@api.route('/get_statistics_by_city_category')
class StatisticalByCityCategory(Resource):
    def post(self):
        pass