from project import create_app
from rate_updater import start as updater_start

app = create_app()
scheduler = updater_start()


if __name__ == '__main__':
    app.run()
    scheduler.shutdown()
