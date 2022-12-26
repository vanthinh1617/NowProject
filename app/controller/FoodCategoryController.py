

from flask_restx import Resource
from flask import request
import inspect
from flask_jwt_extended import jwt_required
from ..util.helpers import _success, _throw
from  ..service.food_service import FoodPlaceService
from app.dto.food_category import FoodCategoryDto
from app.service.food_category_service import FoodCategoryService

api = FoodCategoryDto.api
_category_create_field = FoodCategoryDto.category_create_form

@api.route('/create')
@api.expect(_category_create_field)
class CreateCategory(Resource):
    def post(self):
        try:
            payload = request.get_json() 
            if payload['foodPlaceID'] == "" or payload['foodPlaceID'] is None :  raise Exception("missing field foodPlaceID") 
            
            return _success(inspect.stack(),  FoodCategoryService.create(payload= payload))
        except Exception as e:
            _throw(e)

@api.route('/update')
@api.expect(FoodCategoryDto.category_update_form)
class UpdateCategory(Resource):
    def post(self):
        try:
            payload = request.get_json()
            return _success(inspect.stack(), FoodCategoryService.update(payload))
        except Exception as e:
            _throw(e)   

@api.route('/delete/<id>')
@api.doc(security="Bearer")
class DeleteCategory(Resource):
    def post(self, id):
        try:
            return _success(inspect.stack(), FoodCategoryService.deleteByID(id))
        except Exception as e: 
            _throw(e)