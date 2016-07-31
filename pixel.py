from flask import Flask, render_template, request, send_from_directory
from uuid import uuid4
from time import sleep
import base64

app = Flask(__name__)
app.debug = True
cache = {}  # too lazy
check_count = 20  # these numbers make no sense but w/e
check_min = 15

pixel = base64.b64decode("R0lGODlhAQABAIAAAP8AAP8AACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==")


@app.route('/')
def index():
    use_pixel = request.args.get('pixel', '0') == '1'
    return render_template('index.html', uuid=uuid4(), check_count=check_count, pixel=use_pixel)


@app.route('/adpix/<uuid>/<id>')
def detector_pixel(uuid, id):
    if uuid not in cache:
        cache[uuid] = 0

    cache[uuid] += 1
    return pixel


@app.route('/adv.css')
def detector_css():
    uuid = request.args.get('tag', '')
    if uuid not in cache:
        cache[uuid] = 0

    cache[uuid] += 1
    return '//{}'.format(uuid4())


@app.route('/img')
def img():
    sleep(0.5)
    uuid = request.args.get('uuid', '')
    filename = 'ad.png'
    if cache.get(uuid, 0) < check_min:
        filename = 'block.jpg'
    return send_from_directory(app.static_folder, filename)

if __name__ == "__main__":
    app.run()
