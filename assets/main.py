from flask import Flask, render_template

server = Flask(__name__)


@server.route('/')
def index():
    return render_template('home.html')


@server.route('/statistics')
def statistics():
    return render_template('statistics.html')


@server.route('/map')
def covid_map():
    return render_template('new_master.html')


@server.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')


if __name__ == '__main__':
    server.run('localhost', debug=True)