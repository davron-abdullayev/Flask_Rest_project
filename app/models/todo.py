from sqlalchemy import BigInteger,Boolean,String
from sqlalchemy.orm import Mapped,mapped_column,relationship
from datetime import datetime
from sqlalchemy import DateTime
from enum import Enum
from sqlalchemy import Enum as SQLEnum,ForeignKey
from . import db

class Todo(db.Model):
    __tablename__='todos'

    id:Mapped[int]=mapped_column(BigInteger(),primary_key=True)
    title:Mapped[str]=mapped_column(String(100),nullable=False)
    description:Mapped[str]=mapped_column(String(255),nullable=False)
    user_id:Mapped[int]=mapped_column(BigInteger(),ForeignKey("users.id"),nullable=False)
    user:Mapped["User"]=relationship(back_populates="todos")


    def _dict(self):
        return{
            "id":self.id,
            "title":self.title,
            "description":self.description,
            "user_id":self.user_id
        }
