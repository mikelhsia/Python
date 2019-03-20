import flask
import psycopg2
import psycopg2.extensions
import select

'''
We could have used a library that provides an abstraction layer, such as sqlalchemy, 
but abstracted libraries don’t provide access to the LISTEN and NOTIFY functionality of PostgreSQL.
'''
app = flask.Flask(__name__)


def stream_messages(channel):
    conn = psycopg2.connect(database='michael', user='michael', password='hsia0521', host='localhost')

    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    curs = conn.cursor()
    curs.execute(f"LISTEN channel_{int(channel)};")

    while True:
        select.select([conn], [], [])
        conn.poll()
        while conn.notifies:
            notify = conn.notifies.pop()
            # print(f"Got NOTIFY: {notify.pid}, {notify.channel}, {notify.payload}")
            yield(f"data: {notify.payload}\n")

@app.route("/message/<channel>", methods=['GET'])
def get_message(channel):
    return flask.Response(stream_messages(channel), mimetype='text/event-stream')


if __name__ == '__main__':
    app.run()

