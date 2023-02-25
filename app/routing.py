from flask import Blueprint, render_template, send_from_directory

server_bp = Blueprint('main', __name__)


@server_bp.route('/')
def index():
    return render_template('home.html')


@server_bp.route('/statistics')
def statistics():
    return render_template('statistics.html')

@server_bp.route('/regressions')
def regressions():
    return render_template('regressions.html')

@server_bp.route('/map')
def covid_map():
    return render_template('new_master.html')


@server_bp.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@server_bp.route('/resume.pdf')
def resume():
    image_path = r'/home/SleepingTuna/NYCCovid/app/static/images/'
    resume_name = 'Daniel Resume Data Science 8-2.pdf'
    return send_from_directory(directory=image_path, filename=resume_name, mimetype='application/pdf')

if __name__ == '__main__':
    server_bp.run('localhost', debug=True)