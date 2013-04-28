from flask import render_template, redirect, url_for


def init(app):
    @app.route('/')
    def index():
        return redirect(url_for('chess.index'))

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('page_not_found.html'), 404
