# way to upload image
# way to save the image
# function to make
import os
import random
from flask import Flask
from flask import request
from flask import render_template
# import deepfake_detector.forensics as fp
import pytube
from pytube import YouTube
from flask import Flask,redirect, url_for,render_template,request
import requests, random
requests.packages.urllib3.disable_warnings()
import ssl
import moviepy.editor as moviepy
from detect_fake_videos import test_full_image_network

"""Adapted from https://www.youtube.com/watch?v=BUh76-xD5qU"""

app = Flask(__name__)
UPLOAD_FOLDER = "static"
DEVICE = "cp"
# filename ="deepfakevideo.mp4"

def fetch(url):
    print("Inside Fetch")
    global yt
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        # Legacy Python that doesn't verify HTTPS certificates by default
        pass
    else:
        # Handle target environment that doesn't support HTTPS verification
        ssl._create_default_https_context = _create_unverified_https_context

    try:
        yt = pytube.YouTube(url)
        stream = yt.streams.first()

        print(yt)
        print(url)
    except Exception:
        print("Exception", Exception)
        return -1
    else:
        # return yt.get_videos()
        print("downloading")
        #return stream.download('/Users/shreyus/Desktop/Master_project/untitled_folder/fakeVideoForensics_html/static')
        return stream.download('static')

        # return stream.download()

def convert_pred():
    clip = moviepy.VideoFileClip("static/video.avi")
    clip.write_videofile("static/pred_video.mp4")

@app.route('/work', methods=['POST','GET'])
def work():
    print("Inside work")
    global list
    global rng
    print("Inside predict")
    video_path = "static/video.mp4"
    output_path = "static"
    model_path = "models/full/xception/full_c40.p"
    if request.method == 'POST':
        url_dw = request.form['url']
        y='https://www.youtube.com/watch'
        if y in url_dw:
            list=fetch(url_dw)
            print("list", list)
            if list==-1:
                return render_template('index.html', eval=1)
            print("list",list)
            print("Renaming")
            if "./static/video.mp4":
                os.system("rm ./static/video.mp4")
            os.rename(list,"./static/video.mp4")
            p=len(list)
            rng=[]
            # for k in range(p):
            #     rng.append(k)
            #     # return render_template('index.html', packet=zip(list,rng))
            real, fake = test_full_image_network(video_path, model_path, output_path, start_frame=0, end_frame=None,
                                                 fast=1, cuda=False)
            convert_pred()
            return render_template("success.html", real=real, fake=fake)
        else:
            # return render_template('index.html',eval=1)
            real, fake = test_full_image_network(video_path, model_path, output_path, start_frame=0, end_frame=None,
                                                 fast=1, cuda=False)
            convert_pred()
            return render_template("success.html", real=real, fake=fake)

@app.route("/", methods=["GET", "POST"])
def upload_predict():
    print("Inside predict")
    video_path = "static/video.mp4"
    output_path = "static"
    model_path = "models/full/xception/full_c40.p"
    if request.method == "POST":
        print("Inside post")
        if request.files != "":
            print("request", request.files.keys())
            for i in request.files.keys():
                print(i)

            image_file = request.files["image"]
            if image_file:
                image_location = os.path.join(
                    UPLOAD_FOLDER,
                    "video.mp4"

                )
                print("imagefile", image_location)
                image_file.save(image_location)

                if video_path.endswith('.mp4') or video_path.endswith('.avi'):
                    # test_full_image_network(**vars(args))
                    real, fake = test_full_image_network(video_path, model_path, output_path, start_frame=0, end_frame=None,
                                                         fast=1,cuda=False)
                    convert_pred()
                    return render_template("success.html", real=real, fake=fake)
        real, fake = test_full_image_network(video_path, model_path, output_path, start_frame=0, end_frame=None,
                                                     fast=1,cuda=False)
        convert_pred()
        return render_template("success.html",real=real, fake=fake)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5008, debug=True)
    #app.run(host='35.184.128.190',port=5008, debug=True)
