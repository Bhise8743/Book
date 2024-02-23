from sqlalchemy.orm import declarative_base, Session, relationship,sessionmaker
from sqlalchemy import Integer, String, Column, create_engine
#________________________________________________
from Core.setting import postgresSQL_password, database_name
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession
DATABASE_URL = f'postgresql+psycopg2://postgres:{postgresSQL_password}@localhost:5432/{database_name}'
ASYNC_DATABASE_URL = f'postgresql+asyncpg://postgres:{postgresSQL_password}@localhost:5432/{database_name}'
async_engine = create_async_engine(ASYNC_DATABASE_URL)
async_session = AsyncSession(async_engine)

async def async_get_db():
    async with async_session as db:
        yield db
        await db.commit()
# ---------------------------
engine = create_engine(DATABASE_URL)

session = Session(engine)

Base = declarative_base()


def get_db():
    db = session
    try:
        yield db
    finally:
        db.close()
# ---------------------------


class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    author = Column(String, nullable=False)
    release_year = Column(Integer, nullable=False)
