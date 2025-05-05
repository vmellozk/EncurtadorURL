from flask import Flask, request, redirect, render_template
from models import URL, Session, create_tables
import base62

app = Flask(__name__)
create_tables()

@app.route('/', methods=['GET', 'POST'])
def index():
    short_url = None
    if request.method == 'POST':
        original_url = request.form['url']
        session = Session()

        new_url = URL(original_url=original_url)
        session.add(new_url)
        session.commit()

        short_code = base62.encode(new_url.id)
        new_url.short_code = short_code
        session.commit()
        session.close()

        short_url = request.host_url + short_code

    return render_template('index.html', short_url=short_url)

@app.route('/<short_code>')
def redirect_to_url(short_code):
    session = Session()
    url = session.query(URL).filter_by(short_code=short_code).first()
    session.close()

    if url:
        return redirect(url.original_url)
    return "URL não encontrada", 404

if __name__ == '__main__':
    app.run(debug=True)
