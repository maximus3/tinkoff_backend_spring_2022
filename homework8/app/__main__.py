from app.main import create_app
from config.config import cfg
from database import create_all
from tests.static_create import create_data

app = create_app()
created = create_all()
if created and cfg.debug:
    create_data()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8090, debug=cfg.debug)
