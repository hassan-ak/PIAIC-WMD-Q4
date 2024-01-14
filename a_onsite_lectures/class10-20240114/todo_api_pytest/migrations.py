from api.database_connection.database import engine
from api.models.sqlalchemy_model import Base

Base.metadata.create_all(bind=engine)
# Base.metadata.drop_all(bind=engine)
