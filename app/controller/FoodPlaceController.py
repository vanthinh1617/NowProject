

from app.dto.food_place_dto import FoodPlaceDto
from flask_restx import Resource
from  ..service.food_service import FoodPlaceService
from ..util.helpers import _success, _throw
from flask import request
import inspect
from flask_jwt_extended import jwt_required
api = FoodPlaceDto.api
_foodPlace = FoodPlaceDto.food_place
_foodFields= FoodPlaceDto.food_place_fields

@api.route('/get_by_id/<id>')
class FoodPlace(Resource):
    def get(self, id):
        foodPlace = FoodPlaceService.getByID(id)
        return  _success(inspect.stack(), foodPlace)

@api.route('/update/<id>')
class FoodPlaceUpdate(Resource):
    @api.expect(_foodFields)
    @jwt_required()
    @api.doc(security="Bearer")
    def put(self, id):
        payload = request.get_json()
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
    @api.doc(security="Bearer")
    def post(self):
            payload = request.get_json()
            return _success(inspect.stack(),  FoodPlaceService.create(payload))
  

@api.route('/delete/<id>')
@api.doc(security="Bearer")
class FoodDelete(Resource):
        def delete(self, id):
            return _success(inspect.stack(), FoodPlaceService.deleteByID(id))