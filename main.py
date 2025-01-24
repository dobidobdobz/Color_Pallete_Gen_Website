from flask import *
import numpy
from PIL import Image
from collections import Counter
import os

SECRET_KEY = os.environ.get('SECRET_KEY')

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":

        # grabs file from front end
        image = request.files["image"]

        # this is creating the file path to save the image to
        image_path = os.path.join("static/uploads", "user-image")
        image.save(image_path)

        # try open image if error no image was selected
        try:
            # open image in PIL
            user_img = Image.open(image)
            # retrieve array from image
            user_img_array = numpy.array(user_img)
            # flatten image to 2D
            reshaped_array = user_img_array.reshape(-1, 3)
            # tuples the reshaped array, & Counter counts how many times each tuple appears in the iterable.
            color_counts = Counter(map(tuple, reshaped_array))

            # finds the most common colors
            most_common_colors = color_counts.most_common()

            # if user does not request number of color assume number is 10
            if request.form.get('numColors') == '':
                number_of_colors = 10
            else:
                number_of_colors = int(request.form.get('numColors'))

            # Get the top 10 or requested number of colors
            top_10_colors = most_common_colors[:number_of_colors]

            dict_top_10_colors = []

            # append the top colors in dict_top_10_colors
            for color, count in top_10_colors:
                x = (color, count)
                dict_top_10_colors.append(x)

            return render_template("index.html", top_10_colors=dict_top_10_colors, user_img=image_path)

        # no image was selected flash msg to user in front end
        except:
            flash("Error No file was chosen. please select a file.")
            return render_template("index.html")

    return render_template("index.html")


# runs flask server in debug mode applying changes as they are made when you refresh.
if __name__ == '__main__':
    app.run(debug=True)
