import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    import app

    a = app.App()
    a.run()
