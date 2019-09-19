"""
Author: Gaurav Dharra
Date: 01/18/2019
Description: Updates file names in the image folder updated and calls an app that renders a web vr of the images
Revision: 03/27/2019
Revision 2:
Data: 09/14/2019
Integrating with vrticl
"""
import fnmatch
import shutil, urllib

from flask import Flask, render_template, request
import aframetour.aframetour as aft
import os, urllib, logging

image_list = []
app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

app.config['SECRET_KEY'] = 'dev'


@app.route("/", methods=['GET', 'POST'])
def main():
    try:
        if request.method == 'POST':
            print("I am in post request")
            grid_row = int(request.form['grid_row'])
            grid_column = int(request.form['grid_column'])

            title = request.form['title']
            email = request.form['email']
            session_id = ''
            message = ''

            if request.form['submit_button'] == 'Preview':
                grid_location = request.files['grid_location']
                message, session_id = aft.generate_package_web_tour(grid_location, title, grid_row, grid_column, 'static')
                if message == '':
                    return render_template('index2.html', numberOfRows=grid_row, numberOfCol=grid_column,
                                           path=os.path.join('static', str(session_id), 'static', 'images'),
                                           image_type=str('jpg'),
                                           title=title, email=email, is_file_ready='No', file_location='')
                else:
                    return render_template('Success_Page.html', category='danger',
                                           html_to_display='<h1>'+message+'</h1>',
                                           )
            elif request.form['submit_button'] == 'Download':
                print("I am in download")
                grid_location = request.form['grid_location']
                filename = grid_location
                print('filename = ',filename)
                session_id = filename.split('\\')[1]
                print('session_id = ', session_id)
                return render_template('index2.html', numberOfRows=grid_row, numberOfCol=grid_column,
                                       path=grid_location, image_type=str('jpg'),
                                       title=title, email=email,
                                       is_file_ready='Yes', file_location=os.path.join('static', str(session_id)+'.zip')
                                       )
        else:
            return render_template('WebVR_BuildingTour_FE.html')
    except Exception as err:
        logging.error(str(err))
        print('Error = ', err)


@app.route("/web_vr", methods=['GET', 'POST'])
def web_vr_page():
    return render_template('WebVR_BuildingTour_FE.html')


def before_request():
    app.jinja_env.cache = {}


if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.before_request(before_request)
    temp_map={}
    app.run(debug=True, use_reloader = True)
