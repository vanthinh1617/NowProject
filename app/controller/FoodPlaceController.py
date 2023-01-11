

from app.dto.food_place_dto import FoodPlaceDto
from flask_restx import Resource
from  ..service.food_service import FoodPlaceService
from ..util.helpers import _success, _throw
from flask import request
import inspect
from flask_jwt_extended import jwt_required
from app.util.middleware import cookie_required
api = FoodPlaceDto.api
_foodFields= FoodPlaceDto.food_place_fields
@api.route('/get_by_id/<id>')
class FoodPlace(Resource):
    @api.param('lang', _in="cookie")
    @cookie_required
    def get(self, id):
        try:
            foodPlace = FoodPlaceService.getByID(id)
            return  _success(inspect.stack(), foodPlace)
        except Exception as e:
            _throw(e)

@api.route('/update/<id>')
class FoodPlaceUpdate(Resource):
    @api.expect(_foodFields)
    @jwt_required()
    @cookie_required
    def post(self, id):
        payload = request.get_data()
        return _success(inspect.stack(), FoodPlaceService.update(id=id, payload=payload))
    

@api.route('/get_list')
class FoodPlaceList(Resource):
    @api.doc(params={'page': '1', 'pageSize' :'50'})
    def get(self):
        payload = request.args
        page = payload.get('page') if payload.get('page') is not None else 1
        pageSize = payload.get('pageSize') if payload.get('pageSize') is not None else 50

        return _success(inspect.stack(),  FoodPlaceService.getList(page = page, pageSize= pageSize))

@api.route("/create")
@api.expect(_foodFields)
class FoodCreate(Resource):
    @jwt_required()
    def post(self):
            payload = request.get_json()
            return _success(inspect.stack(),  FoodPlaceService.create(payload))
  

@api.route('/delete/<id>')
class FoodDelete(Resource):
        def delete(self, id):
            return _success(inspect.stack(), FoodPlaceService.deleteByID(id))