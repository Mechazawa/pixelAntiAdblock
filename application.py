from flask import Flask, render_template, request, send_from_directory
from uuid import uuid4
from time import sleep
import re
import redis
from flask import Response

app = Flask(__name__)
cache = {}  # too lazy
check_count = 20  # these numbers make no sense but w/e
check_min = 15 # content detection only
redis_connection = redis.from_url('redis://127.0.0.1:6379')
uuid_regex = re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')
max_wait = 5


def render_template_lazy(template_name, **context):
    app.update_template_context(context)
    return app.jinja_env.get_template(template_name).render(**context)


@app.route('/')
def r_index():
    return render_template('index.html')


@app.route('/content')
def r_content():
    return render_template('content.html', uuid=uuid4(), check_count=check_count)


@app.route('/streaming')
def r_streaming():
    uuid = str(uuid4())

    def generate():
        yield render_template_lazy('streaming.html', uuid=uuid, check_count=check_count)

        wait_total = 0.0

        while wait_total < max_wait and not completed_challenge(uuid):
            sleep(0.05)
            wait_total += 0.05

        if completed_challenge(uuid):
            yield render_template_lazy('streaming_advert.html')
        else:
            yield render_template_lazy('streaming_block.html')

        yield '</body></html>'
    return Response(generate())


@app.route('/adv.css')
def detector_css():
    uuid = request.args.get('tag', '')
    if uuid_regex.match(uuid) is not None:
        name = "httpclient-{}".format(uuid)
        redis_connection.setnx(name, 0)
        redis_connection.expire(name, 30)  # Expire in 30 seconds
        redis_connection.incr(name)
    return '/* placeholder {} */'.format(uuid4())


def completed_challenge(uuid):
    if uuid_regex.match(uuid) is None:
        return False

    name = "httpclient-{}".format(uuid)
    value = int(redis_connection.get(name) or 0)
    return value >= check_min


@app.route('/img')
def img():
    uuid = request.args.get('uuid', '')

    filename = 'ad.png'
    if not completed_challenge(uuid):
        filename = 'block.jpg'
    if len(uuid) != 36:
        filename = 'err.jpg'
    return send_from_directory(app.static_folder, filename)

if __name__ == "__main__":
    app.run()

# wsgi
application = app
