from app import create_app

app = create_app(True)
app.run('0.0.0.0')
