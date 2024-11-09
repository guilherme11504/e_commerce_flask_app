from app import create_app, db
import os


app = create_app()

with app.app_context():
    db.create_all()


if __name__ == "__main__":
    debug_mode = os.getenv('DEBUG_MODE', 'True') == 'True'  # Mude para 'False' em produção
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)
