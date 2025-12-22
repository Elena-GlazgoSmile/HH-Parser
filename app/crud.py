from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app import models, schemas
from datetime import datetime

class CRUDVacancy:
    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 100):
        result = await db.execute(
            select(models.Vacancy)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_by_hh_id(self, db: AsyncSession, hh_id: str):
        result = await db.execute(
            select(models.Vacancy)
            .where(models.Vacancy.hh_id == hh_id)
        )
        return result.scalar_one_or_none()
    
    async def create(self, db: AsyncSession, vacancy: schemas.VacancyCreate):
        db_vacancy = models.Vacancy(**vacancy.dict())
        db.add(db_vacancy)
        await db.commit()
        await db.refresh(db_vacancy)
        return db_vacancy
    
    async def update(self, db: AsyncSession, hh_id: str, vacancy_update: schemas.VacancyUpdate):
        stmt = (
            update(models.Vacancy)
            .where(models.Vacancy.hh_id == hh_id)
            .values(**vacancy_update.dict(exclude_unset=True), updated_at=datetime.utcnow())
            .returning(models.Vacancy)
        )
        
        result = await db.execute(stmt)
        await db.commit()
        return result.scalar_one_or_none()
    
    async def delete(self, db: AsyncSession, hh_id: str):
        vacancy = await self.get_by_hh_id(db, hh_id)
        if vacancy:
            await db.delete(vacancy)
            await db.commit()
            return True
        return False

crud_vacancy = CRUDVacancy()
