from pathlib import Path
import os

path = Path(os.getcwd())
url = path.resolve()+"asd"
print(url)
# print(path.parents[0],"/translate/lang")
# sys.path.append(folder.parent.parent)