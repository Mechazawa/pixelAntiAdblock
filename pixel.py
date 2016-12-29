from flask import Flask, render_template, request, send_from_directory
from uuid import uuid4
from time import sleep

app = Flask(__name__)
cache = {}  # too lazy
check_count = 20  # these numbers make no sense but w/e
check_min = 15


@app.route('/')
def index():
    return render_template('index.html', uuid=uuid4(), check_count=check_count)


@app.route('/adv.css')
def detector_css():
    uuid = request.args.get('tag', '')
    if uuid not in cache:
        cache[uuid] = 0

    cache[uuid] += 1
    return '/* placeholder {} */'.format(uuid4())


@app.route('/img')
def img():
    sleep(0.5)
    uuid = request.args.get('uuid', '')
    filename = 'ad.png'
    if cache.get(uuid, 0) < check_min:
        filename = 'block.jpg'
    if len(uuid) != 36:
        filename = 'err.jpg'
    return send_from_directory(app.static_folder, filename)

if __name__ == "__main__":
    app.run()

# wsgi
application = app
