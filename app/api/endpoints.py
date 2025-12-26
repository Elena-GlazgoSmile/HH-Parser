from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime

from app.database import get_db
from app import schemas
from app.crud import crud_vacancy
from app.tasks.background import background_task

router = APIRouter()

@router.get("/items", response_model=List[schemas.VacancyResponse])
async def get_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db)
):
    items = await crud_vacancy.get_all(db, skip=skip, limit=limit)
    
    return items

@router.get("/items/{item_id}", response_model=schemas.VacancyResponse)
async def get_item(item_id: str, db: AsyncSession = Depends(get_db)):
    item = await crud_vacancy.get_by_hh_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Элемент не найден")
    return item

@router.post("/items", response_model=schemas.VacancyResponse)
async def create_item(
    item: schemas.VacancyCreate,
    db: AsyncSession = Depends(get_db)
):
    existing = await crud_vacancy.get_by_hh_id(db, item.hh_id)
    if existing:
        raise HTTPException(status_code=400, detail="Элемент уже существует")
    
    created = await crud_vacancy.create(db, item)
    return created

@router.patch("/items/{item_id}", response_model=schemas.VacancyResponse)
async def update_item(
    item_id: str,
    item_update: schemas.VacancyUpdate,
    db: AsyncSession = Depends(get_db)
):
    updated = await crud_vacancy.update(db, item_id, item_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Элемент не найдена")
    return updated

@router.delete("/items/{item_id}")
async def delete_item(item_id: str, db: AsyncSession = Depends(get_db)):
    deleted = await crud_vacancy.delete(db, item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Элемент не найден")
    return {"message": "Элемент удален"}

@router.post("/tasks/run", response_model=schemas.TaskRunResponse)
async def run_background_task():
    result = await background_task.run(manual=True)
    
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["error"])
    
    return {
        "message": "Фоновая задача запущена",
        "task_id": result["task_id"],
        "started_at": datetime.utcnow()
    }
