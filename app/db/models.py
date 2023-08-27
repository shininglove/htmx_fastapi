from datetime import datetime
from sqlalchemy import DateTime, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


class Base(DeclarativeBase):
    pass


class DirectoryState(Base):
    __tablename__ = "directory"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    path: Mapped[str] = mapped_column(String(255))
    date: Mapped[datetime] = mapped_column(DateTime)

    def __repr__(self) -> str:
        return f"DirectoryState(name={self.name},path={self.path})"

class StateType(Base):
    __tablename__ = "directory"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    state: Mapped[bool] = mapped_column(String(255))
    date: Mapped[datetime] = mapped_column(DateTime)

    def __repr__(self) -> str:
        return f"DirectoryState(name={self.name},state={self.state})"


engine = create_engine("sqlite:///cache.db", echo=True)

session = Session(engine)
