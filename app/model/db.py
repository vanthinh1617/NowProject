from pymongo import MongoClient
from flask_pymongo import PyMongo

client = MongoClient('localhost', 27017)
mongo = PyMongo()

db = client.Now
userCollection = db.users
foodDrinksCollection = db.foodDrinks
foodPlacesCollection = db.foodPlaces
foodVideosCollection = db.foodVideos
foodLocationsCollection = db.foodLocations
foodCategoriesCollection = db.foodCategories
foodOpenTimesCollection = db.foodOpenTimes
foodImagesCollection = db.foodImages
foodSocialNetworkCollection = db.foodSocialNetworks
foodTypeAndStylesCollection = db.foodTypeAndStyles
foodPromotionsCollection = db.foodPromotions
foodReviewsCollection = db.foodPreviews
foodReviewReportsCollection = db.foodReviewReports


def initialize_db(app):
    mongo.init_app(app)