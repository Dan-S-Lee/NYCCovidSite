from app import create_app
from app.routing import server_bp

server = create_app()
server.register_blueprint(server_bp)

if __name__ == '__main__':
    server.run('localhost', debug=True)
