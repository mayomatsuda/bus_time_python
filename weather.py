import requests
import json
import sys
import time
from datetime import datetime
sys.path.insert(1, '/home/pi/Documents/rpi-rgb-led-matrix/bindings/python')
from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
import urllib.request
from PIL import Image

API_KEY = "9f1b0c1d0f611f5ffb437e3ebbeb98c5"
IMAGE = "icon_file.png"
LAT = 42.985200
LON = -81.265600
URL = f'https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric'

def get_data():
    response = requests.get(URL)
    tx = response.text
    js = json.loads(tx)

    global weather
    global temps
    global currenttime

    weather = js["weather"][0]['main']
    icon = js["weather"][0]['icon']
    temp = round(js["main"]["feels_like"])
    temps = f'{temp}°'
    icon_url = f'http://openweathermap.org/img/wn/{icon}@2x.png'

    urllib.request.urlretrieve(icon_url, "icon_file.png")

    now = datetime.now()
    currenttime = now.strftime("%I:%M ")
    format_text()

def format_text():
    global text
    text = currenttime + temps +  ";" + weather

def run_text():
    global text
    options = RGBMatrixOptions()
    options.cols = 64
    options.hardware_mapping = "adafruit-hat"
    options.brightness = 50

    matrix = RGBMatrix(options=options)
    offscreen_canvas = matrix.CreateFrameCanvas()
    font = graphics.Font()
    font.LoadFont("/home/pi/Documents/rpi-rgb-led-matrix/fonts/7x13.bdf")
    fontSmall = graphics.Font()
    fontSmall.LoadFont("/home/pi/Documents/rpi-rgb-led-matrix/fonts/6x9.bdf")
    textColor = graphics.Color(255, 255, 255)

    try:
        while True:
            get_data()
            text = text.split(';')
            # Too long to fit
            if (text[1] == "Thunderstorm"): text[1] = "Thunder"
            offscreen_canvas.Clear()

            LEFT_POS = 1
            TOP_POS = 13
            BOTTOM_POS = 25

            image = Image.open(IMAGE)
            image.thumbnail((16, 16), Image.ANTIALIAS)

            graphics.DrawText(offscreen_canvas, font, LEFT_POS, TOP_POS, textColor, text[0])
            graphics.DrawText(offscreen_canvas, fontSmall, LEFT_POS + 18, BOTTOM_POS, textColor, text[1])

            offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)

            matrix.SetImage(image.convert('RGB'), LEFT_POS, TOP_POS)

            time.sleep(60)

    except KeyboardInterrupt:
        sys.exit(0)

run_text()