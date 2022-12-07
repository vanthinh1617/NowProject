""" TUTORIAL OR EXAMPLE DOCUMENT 
    PYDANTIC tutorial: https://www.youtube.com/watch?v=Vj-iU-8_xLs    (validator example, )
"""
from pydantic import BaseModel, Field
from app.util.objectid import PydanticObjectId
from typing import Optional,Text, List, Union
from bson.objectid import ObjectId
from datetime import datetime
from fastapi.encoders import jsonable_encoder

class GenericModel(BaseModel):
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True  # required for the _id
        json_encoders = {ObjectId: str}
  
    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)
        
   
    def to_bson(self):
        data = self.dict(by_alias=True, exclude_none=False)
        if data.get("_id") is None:
            data.pop("_id", None)
        return data



class Users(GenericModel):
    class Address(GenericModel): 
        street: str
        city: str
        zipcode: str

    class Name(GenericModel):
        firstName: str
        lastName: str

    id: Optional[PydanticObjectId] = Field(None, alias="_id")
    username: str
    password: str
    email: Optional[str]
    name: Union[Name, None]  
    address: Optional[Address] 
    createTime: datetime = Field(default_factory=datetime.utcnow)

class FoodCategories(GenericModel):
    id: Optional[PydanticObjectId] = Field(None, alias="_id")
    oldDishTypeID: PydanticObjectId
    foodPlaceID: PydanticObjectId
    createTime: datetime = Field(default_factory=datetime.utcnow)


class FoodPlaces(GenericModel):
    id: Optional[PydanticObjectId] = Field(None, alias="_id")
    userID: Optional[PydanticObjectId]
    # oldRestaurentID: Optional[PydanticObjectId]
    name: str
    nameWithoutAccent: Optional[str]
    amennities: Optional[Text]
    phone: Optional[str] 
    email: Optional[str]
    website: Optional[str]
    maxPrice: Optional[int]
    minPrice: Optional[int]
    allowView: Optional[int]
    status: int = 0
    avgRating: int = 0
    totalReview: int=0
    createTime: datetime = Field(default_factory=datetime.utcnow)

class FoodVideos(GenericModel):
    id: Optional[PydanticObjectId] = Field(None, alias="_id")
    foodPlaceID:  PydanticObjectId = Field(alias='foodPlaceID')
    address: Optional[str]
    country: Optional[str]
    city: Optional[str]
    postcode: Optional[str]
    location: Optional[str]
    createTime: datetime = Field(default_factory=datetime.utcnow)

class FoodDrink(GenericModel):
    id: Optional[PydanticObjectId] = Field(None, alias="_id")
    foodCategoryID: PydanticObjectId
    oldDishID: PydanticObjectId
    image: Optional[str]
    price: Optional[int]
    createTime: datetime = Field(default_factory=datetime.utcnow)
    
class FoodOpenTimes(GenericModel):
    id: Optional[PydanticObjectId] = Field(None, alias="_id")
    foodPlaceID: PydanticObjectId 
    openTime: Optional[Text]
    createTime: datetime = Field(default_factory=datetime.utcnow)

class FoodImages(GenericModel):
    id: Optional[PydanticObjectId] = Field(None, alias="_id")
    foodPlaceID: PydanticObjectId 
    facebook :Optional[str]
    twitter: Optional[str]
    youtube:Optional[str]
    instagram:Optional[str]
    whatsapp:Optional[str]
    skype:Optional[str]
    createTime: datetime = Field(default_factory=datetime.utcnow)
    
class FoodTypeAndStyles(GenericModel):
    id: Optional[PydanticObjectId] = Field(None, alias="_id")
    foodPlaceID: PydanticObjectId
    type: Optional[str]
    dining_times: Optional[str]
    prices: Optional[str]
    styles: Optional[str]
    goodFor: Optional[str]
    standFoods: Optional[Text]
    capacity: PydanticObjectId
    lastAdminssionTime: Optional[Text]
    preparationTime: Optional[Text]
    holiday: Optional[Text]
    createTime: datetime = Field(default_factory=datetime.utcnow)

class FoodPromotion(GenericModel):
    id: Optional[PydanticObjectId] = Field(None, alias="_id")
    foodPLaceID: PydanticObjectId
    foodPromotionCode: str 
    expireAt: datetime = Field(default_factory=datetime.utcnow)
    createTime: datetime = Field(default_factory=datetime.utcnow)

class FoodReviews(GenericModel):
    id: Optional[PydanticObjectId] = Field(None, alias="_id")
    foodPlaceID: PydanticObjectId
    userID: PydanticObjectId
    oldReviewID: PydanticObjectId
    title: Optional[str]
    content: Optional[str]
    images: Optional[Text]
    avg_ration: Optional[str]
    rating: Optional[str]
    prentID: PydanticObjectId
    numOfReports: PydanticObjectId
    createTime: datetime = Field(default_factory=datetime.utcnow)

class FoodReviewReport(GenericModel):
    id: Optional[PydanticObjectId] = Field(None, alias="_id")
    foodReviewID: PydanticObjectId
    userID: PydanticObjectId
    content: Text
    
