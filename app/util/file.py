from flask import app
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

class AllowFile:
    @staticmethod
    def allowFile(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class SaveFileToLocal:
    @staticmethod
    def process(files):
        pathUrl = f"app/static/photos/"
        storeNames = []
        for file in files:
            if file and not AllowFile.allowFile( file.filename): continue
            storeNames.append("photos"+file)
            file.save(pathUrl+file.filename)

        return storeNames
