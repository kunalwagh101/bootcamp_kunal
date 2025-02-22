"""

NO.5 Database Integration

Objective: Integrate a simple database (e.g., SQLite) with FastAPI for persisting data.
Task: Connect FastAPI to a SQLite database and modify CRUD operations to use the database.
Expected Output: CRUD operations interact with a SQLite database. (To add, update, and delete items),
from sqlalchemy import create_engine
"""


from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CarModel(Base):
    __tablename__ = "cars"
    
    id = Column(Integer, primary_key=True, index=True)
    name =Column(String ,index=True, nullable =True)
    company = Column(String, index=True, nullable =True)
    model = Column(String, nullable=True)
    color = Column(String, nullable =True )

    def __repr__(self):
        return f"<CarModel(id= {self.id} , name = {self.name}, company = {self.company} ,model=  {self.model}, color ={self.color})>"
    
    def __str__(self):
        return f" id   =  {self.id} , name = {self.name}, company = {self.company} ,model=  {self.model}, color ={self.color}"
    
 

# Base.metadata.create_all(bind=engine)

#  python -c "from database import engine; from models import Base; Base.metadata.drop_all(bind=engine)"