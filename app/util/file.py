from flask import app
class SaveFileToLocal:
    @staticmethod
    def process(files):
        # pathUrl = f"app/static/photos/s{width}x{height}/{image['value'].split('/')[-1]}"
        pathUrl = f"app/static/photos/"
        for file in files :
             file.save(pathUrl, file.filename)
        pass
