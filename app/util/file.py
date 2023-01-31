from flask import app
import os, time
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def allow_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



def save_file_local(files):
    pathUrl = os.getenv("STATIC_PATH")
    store_name = []
    for file in files:
        if file  and  allow_file( file.filename) is True: 
            name =  f"{int(time.time())}.{file.filename.rsplit('.', 1)[1].lower()}"
            store_name.append(name)
            file.save(pathUrl+name)

    return store_name

def remove_file(file_name):
    static_path = os.getenv('STATIC_PATH')
    path = static_path+"/"+file_name
    if os.path.exists(path):
        os.remove(path)
        return True
    else:
        return False
        
    
 