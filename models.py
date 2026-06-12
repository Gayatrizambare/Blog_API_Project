from sqlalchemy import Column , Integer, String ,Text
from database import Base

#Blog table
class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer,primary_key=True ,index=True)  #index=True makes the database search through your data much faster.
    title = Column(String)
    content=Column(Text)