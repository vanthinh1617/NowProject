#document :
#  
# https://www.digitalocean.com/community/tutorials/processing-incoming-request-data-in-flask
# https://www.imaginarycloud.com/blog/flask-python/


from app import create_app, blueprint
# from dotenv import load_dotenv

# load_dotenv()
app = create_app(__name__)
app.register_blueprint(blueprint)

        
if __name__ == '__main__':
    app.run(debug=False)
  
