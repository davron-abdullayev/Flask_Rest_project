
from sqlalchemy import BigInteger,Boolean,String
from sqlalchemy.orm import Mapped,mapped_column,relationship
from datetime import datetime
from sqlalchemy import DateTime
from enum import Enum
from sqlalchemy import Enum as SQLEnum

from . import db

class UserRole(Enum):
    ADMIN="admin"
    USER="user"


class User(db.Model):
    __tablename__='users'

    id:Mapped[int]=mapped_column(BigInteger(),primary_key=True)
    first_name:Mapped[str]=mapped_column(String(255))
    last_name:Mapped[str]=mapped_column(String(255))
    username:Mapped[str]=mapped_column(String(100),unique=True,nullable=False)
    create_at:Mapped[datetime]=mapped_column(DateTime(),default=datetime.now)
    password:Mapped[str]=mapped_column(String(255),nullable=False)
    is_role:Mapped[UserRole]=mapped_column(SQLEnum(UserRole),default=UserRole.USER,nullable=False)
    todos: Mapped[list["Todo"]] = relationship(back_populates="user")

    def _dict(self):
        return{
            "id":self.id,
            "first_name":self.first_name,
            "last_name":self.last_name,
            "username":self.username,
            "is_role":self.is_role.value
            
        }