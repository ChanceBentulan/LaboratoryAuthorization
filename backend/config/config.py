import os

def configure_app(app):
    postgres_host = 'postgres-db'
    postgres_port = os.environ.get('POSTGRES_PORT')
    postgres_user = os.environ.get('POSTGRES_USER')
    postgres_password = os.environ.get('POSTGRES_PASSWORD')
    postgres_db = os.environ.get('POSTGRES_DB')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"
