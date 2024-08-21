from sqlalchemy import create_engine, Column, String, Integer, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = 'sqlite:///chat_history.db'  # Choose your own db address
engine = create_engine(DATABASE_URL)

Base = declarative_base()


class ChatHistory(Base):
    __tablename__ = "chathistory"
    user_id = Column(String, primary_key=True)
    username = Column(String)
    full_name = Column(String)
    first_interaction = Column(Date)
    last_interaction = Column(Date)
    current_model = Column(String)
    current_chat_mode = Column(String)

    role = Column(String)
    msg = Column(String)


Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)