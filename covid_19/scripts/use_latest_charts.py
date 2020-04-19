from main_app.views import GraphFile
import shutil
import os
def run():
    source = os.path.join(os.path.abspath(GraphFile.graph_image_store_path))+"/"
    dest1 = os.path.join(os.path.abspath(GraphFile.graph_image_load_path))+"/"

    files = os.listdir(source)

    for f in files:
        shutil.move(source+f, dest1+f)

    print("Done")