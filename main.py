from fastapi import status, FastAPI, Response, Depends, Path, HTTPException
from sqlalchemy import update, delete, insert

from schema import BookSchema
from model import get_db, Book,async_get_db
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

app = FastAPI()


@app.post('/add', status_code=status.HTTP_201_CREATED)
async def create_book(body: BookSchema, response: Response, db: AsyncSession = Depends(async_get_db)):
    try:
        query = insert(Book).values(**body.model_dump())
        result = await db.execute(query)
        await db.commit()
        pk = result.inserted_primary_key
        return {'message': "Book added Successfully", 'status': 201,'data':pk}
    except Exception as ex:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(ex), 'status': 400}


@app.get('/get', status_code=status.HTTP_200_OK)
async def get_all_books(response: Response, db: AsyncSession = Depends(async_get_db)):
    try:
        query = select(Book).filter()
        result = await db.execute(query)
        if result is None:
            raise HTTPException(detail="The books are not present ",status_code=status.HTTP_400_BAD_REQUEST)
        return {'message': "Data retrieved Successfully", 'data': result.scalars().all()}
    except Exception as ex:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(ex), 'status': 400}


@app.patch('/update/{id}', status_code=status.HTTP_200_OK)
async def update_book(body: BookSchema, response: Response, db: AsyncSession = Depends(async_get_db),
                      id: int = Path(..., description="Enter the book id ")):
    try:
        query = update(Book).where(Book.id==id).values(**body.model_dump())
        result = await db.execute(query)
        is_updated = result.rowcount > 0
        if is_updated is None:
            raise HTTPException(detail='This book is not present', status_code=status.HTTP_200_OK)
        # [setattr(data, key, value) for key, value in body.model_dump().items()]
        await db.commit()
        # db.refresh(data)
        return {'message': 'Book found successfully', 'status': 200,'data':is_updated}
    except Exception as ex:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(ex), 'status': 400}


@app.get('/get/{id}', status_code=status.HTTP_200_OK)
async def get_book(response: Response, db: AsyncSession = Depends(async_get_db), id: int = Path(..., description="Enter the book id")):
    try:
        query = select(Book).where(Book.id==id)
        result = await db.execute(query)
        if result is None:
            raise HTTPException(detail='This Book is not present', status_code=status.HTTP_400_BAD_REQUEST)
        return {'message': "The Book Found successfully", 'status': 200, 'data':result.scalar_one_or_none() }
    except Exception as ex:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(ex), 'status': 400}


@app.delete('/del/{id}', status_code=status.HTTP_200_OK)
async def delete_book(response: Response, db: AsyncSession = Depends(async_get_db),
                      id: int = Path(..., description="Enter the book id you want to delete ")):
    try:
        query = delete(Book).where(Book.id==id)
        result = await db.execute(query)
        is_deleted = result.rowcount > 0
        if is_deleted is None:
            raise HTTPException(detail="The book is not present ", status_code=status.HTTP_400_BAD_REQUEST)
        await db.commit()
        return {'message': "Book deleted Successfully", "status": 200,'data':is_deleted}
    except Exception as ex:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(ex), 'status': 400}




