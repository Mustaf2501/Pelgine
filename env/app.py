from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import requests
import colorgram
from colormath.color_conversions import convert_color
from colormath.color_objects import sRGBColor, LabColor

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app=app)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img_url = db.Column(db.String(1024), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    lab1 = db.Column(db.String(200), nullable=False)
    lab2 = db.Column(db.String(200), nullable=False)
    lab3 = db.Column(db.String(200), nullable=False)
    lab4 = db.Column(db.String(200), nullable=False)
    lab5 = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return 'Image - id: {} - img_url: {} - title:{} - lab1:{} - lab2:{} - lab3:{} - lab4:{} - lab5:{}"'.format(self.id, self.img_url, self.title, self.lab1, self.lab2, self.lab3, self.lab4, self.lab5) 


def updateDB():
    base_url = 'https://collectionapi.metmuseum.org/public/collection/v1/objects/100'
    response = requests.get(base_url)
    app.logger.info(response.status_code)
    if response.status_code == 200:
        app.logger.info('Success!')
        json = response.json()
        if json["isPublicDomain"] == True:
            url = json["primaryImage"]
            app.logger.info(json["primaryImage"])
            app.logger.info(json["title"])
            img_data = requests.get(url).content
            with open('temp.jpg', 'wb') as handler:
                handler.write(img_data)
            # colorgram only creates 4 colors for this image
            # need to shop around for another color extractor

            # Going to create a Node.js server that will run 
            # The Google experiment script that extracts color palettes
            colors = colorgram.extract('temp.jpg', 5)
            app.logger.info("COLORS {}".format(len(colors)))
            app.logger.info("CONVERTING...")
            for color in colors:
                rgb = color.rgb
                srgbObj =  sRGBColor(rgb.r, rgb.g, rgb.b)
                lab = convert_color(srgbObj, LabColor)
                app.logger.info(lab)

@app.route('/')
def index():
    updateDB()
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)