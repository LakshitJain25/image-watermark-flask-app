from distutils.command.upload import upload
import cv2
from flask import Flask, request, render_template
import numpy as np
import requests
from PIL import Image
import os

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        # image = Image.open(
        #     requests.get(
        #         "https://media.sproutsocial.com/uploads/2017/02/10x-featured-social-media-image-size.png",
        #         stream=True,
        #     ).raw
        # )
        file_upload = request.files["file_upload"]
        filename = file_upload.filename
        image = Image.open(file_upload)
        image_logow = image.resize((500, 300))
        image_textw = image.resize((500, 300))
        logo = Image.open(
            requests.get(
                "https://www.freeiconspng.com/thumbs/logo-whatsapp-png/logo-whatsapp-transparent-background-22.png",
                stream=True,
            ).raw
        )
        image_logow = np.array(image_logow.convert("RGB"))
        h_image, w_image, p = image_logow.shape
        logo = np.array(logo.convert("RGB"))
        h_logo, w_logo, p = logo.shape
        center_y = int(h_image / 2)
        center_x = int(w_image / 2)
        top_y = center_y - int(h_logo / 2)
        left_x = center_x - int(w_logo / 2)
        bottom_y = top_y + h_logo
        right_x = left_x + w_logo
        roi = image_logow[top_y:bottom_y,left_x:right_x]
        app.logger.info(roi.shape,logo.shape)
        result = cv2.addWeighted(roi,1,logo,1,0)
        cv2.line(image_logow,(0,center_y),(left_x,center_y),(0,0,255),1)
        cv2.line(image_logow,(right_x,center_y),(w_image,center_y),(0,0,255),1)
        image_logow[top_y:bottom_y,left_x:right_x] = result
        img = Image.fromarray(image_logow,'RGB')
        img.save(os.path.join("static/uploads","image.jpg"))
        return render_template("index.html",image="../static/uploads/image.jpg")



if __name__ == "__main__":
    app.run(debug=True)
