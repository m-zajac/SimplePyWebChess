def init(app):
    # index

    @app.route('/')
    def index():
        return 'Index page'
