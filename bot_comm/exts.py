from flask_sqlalchemy import SQLAlchemy
from db import models

db = SQLAlchemy(metadata=models.metadata)
