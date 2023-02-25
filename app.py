from skate_app.routes import main
from skate_app.routes import auth
from skate_app.extensions import app, db

app.register_blueprint(main)
app.register_blueprint(auth)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)