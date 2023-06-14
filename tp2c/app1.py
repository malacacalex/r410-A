from fastapi import FastAPI
from fastapi_sqlalchemy import SQLalchemyMiddleware
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String

app = FastAPI()

SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Data(Base):
    __tablename__ = "data"
 
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)

Base.metadata.create_all(bind=engine)

@app.post("/data/")
async def create_data(data: DataCreate):
    db = SessionLocal()
    db_data = Data(name=data.name, description=data.description)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

@app.get("/data/{data_id}")
async def read_data(data_id: int):
    db = SessionLocal()
    db_data = db.query(Data).filter(Data.id == data_id).first()
    if db_data is None:
        raise HTTPException(status_code=404, detail="Data not found")
    return db_data

@app.get("/data/")
async def read_all_data():
    db = SessionLocal()
    db_data = db.query(Data).all()
    return db_data
	
