def init(blueprint):
    # index

    @blueprint.route('')
    def index():
        return 'Chess index'
