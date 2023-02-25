from flask import Flask
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

def create_app():
    server = Flask(__name__)

    from app.stats.layout import layout as layout1
    from app.stats.callbacks import register_callbacks as register_callbacks1

    register_dashapp(server, 'Stats', 'dashboard', layout1, register_callbacks1)

    from app.analysis.layout import layout as layout2
    from app.analysis.callbacks import register_callbacks as register_callbacks2
    register_dashapp(server, 'Analysis', 'regress', layout2, register_callbacks2)

    register_blueprints(server)

    return server


def register_extensions(server):
    from app.extensions import db
    from app.extensions import migrate

    db.init_app(server)
    migrate.init_app(server, db)


def register_blueprints(server):
    from app.routing import server_bp


def register_dashapp(app, title, base_pathname, layout, register_callbacks_fun):
    # Meta tags for viewport responsiveness
    meta_viewport = {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}

    my_dashapp = dash.Dash(__name__,
                           server=app,
                           url_base_pathname=f'/{base_pathname}/',
                           meta_tags=[meta_viewport])
    # Push an application context so we can use Flask's 'current_app'
    with app.app_context():
        my_dashapp.title = title
        my_dashapp.layout = layout
        register_callbacks_fun(my_dashapp)