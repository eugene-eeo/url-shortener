import os

from flask import Flask, request, jsonify, abort, redirect
from flask_mysqldb import MySQL
from shortener import shorten
import validators


app = Flask(__name__)
app.config['MYSQL_DB'] = os.environ.get('URLSHORTENER_DB', 'urlshortener')
mysql = MySQL(app)


@app.route('/fwd/<id>')
def fwd(id):
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute('SELECT destination FROM url WHERE id = %s', (id,))
    row = cur.fetchone()
    if row is None:
        abort(404)

    cur.execute('UPDATE url SET hits = hits + 1 WHERE id = %s', (id,))
    conn.commit()
    return redirect(row[0])


@app.route('/url/<id>')
def get(id):
    cur = mysql.connection.cursor()
    cur.execute('''
        SELECT url.id, url.hits, url.destination, url_tags.tag FROM url
        LEFT OUTER JOIN url_tags ON url.id = url_tags.id
        WHERE url.id = %s
    ''', (id,))
    res = cur.fetchall()
    if len(res) == 0:
        abort(404)

    rv = {'tags': []}
    for id, hits, destination, tag in res:
        rv['id'] = id
        rv['hits'] = hits
        rv['destination'] = destination
        if tag is not None:
            rv['tags'].append(tag)

    return jsonify(rv)


@app.route('/tagged/<tag>')
def tagged(tag):
    c = mysql.connection.cursor()
    c.execute('''
        SELECT url.id, url.hits, url.destination, url_tags.tag
        FROM url
            LEFT OUTER JOIN url_tags ON url.id = url_tags.id
            WHERE url.id IN (
                SELECT id FROM url_tags WHERE tag = %s
                )
    ''', (tag,))

    urls = []
    r = {'id': None, 'tags': []}

    for id, hits, destination, tag in c.fetchall():
        if id != r['id']:
            r = {'id': id,
                 'hits': hits,
                 'destination': destination,
                 'tags': []}
            urls.append(r)
        if tag is not None:
            r['tags'].append(tag)

    return jsonify(urls)


@app.route('/url/<id>', methods=['DELETE'])
def delete(id):
    conn = mysql.connection
    cur  = conn.cursor()
    try:
        cur.execute('DELETE FROM url WHERE id = %s', (id,))
        conn.commit()
        return jsonify({'id': id}), 200
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500


@app.route('/url', methods=['POST'])
@app.route('/url/<id>', methods=['POST'])
def create(id=None):
    json = request.get_json()
    url  = json['url']
    id   = id or shorten(url)
    tags = json.get('tags', [])
    conn = mysql.connection
    cur  = conn.cursor()
    if not validators.url(url):
        return jsonify({'error': 'not a valid url: "%s"' % url}), 500

    try:
        cur.execute('INSERT INTO url(id, hits, destination) VALUES (%s, %s, %s);', (id, 0, url))
        cur.executemany('INSERT INTO url_tags VALUES (%s, %s);', [
            (id, tag) for tag in tags
        ])
        conn.commit()
        return jsonify({'id': id}), 200

    except Exception as exc:
        return jsonify({'error': str(exc)}), 500


if __name__ == '__main__':
    app.run(debug=True)
