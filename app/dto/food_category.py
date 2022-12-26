from flask_restx import Namespace, fields


class FoodCategoryDto:
    api = Namespace("FoodCategory",  description="Api food category document")

    food_category_field = api.model('FoodCategory', {
        "_id": fields.String(),
        "oldDishTypeID": fields.String(),
        "foodPlaceID": fields.String(),
        "createTime": fields.String()
    })

    category_mutil_lang = api.model("LangSpecify", {
        "vn": fields.String(),
        "en": fields.String(),
    })
    category_create_form = api.model('Category Create Form', {
        "foodPlaceID": fields.String(),
        "categoryLangs": fields.List(fields.Nested(category_mutil_lang))
    })

    category_update_form = api.model('Category update form', {
        "foodCategoryID": fields.String(),
        "categoryLangs": fields.Nested(category_mutil_lang)
    })