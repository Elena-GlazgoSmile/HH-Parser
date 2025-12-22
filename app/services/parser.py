import httpx
import asyncio
from datetime import datetime
from typing import Dict, Any, List
from app.config import settings
from app import schemas

class HHParser:
    def __init__(self):
        self.client = httpx.AsyncClient(
            timeout=30.0,
            headers={"User-Agent": "HH-Parser/1.0"}
        )
    
    async def fetch_vacancies(self, search_text: str = "Python", area: int = 1) -> List[Dict[str, Any]]:
        try:
            params = {
                "text": search_text,
                "area": area,
                "per_page": 50,
                "page": 0
            }
            
            response = await self.client.get(settings.HH_API_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            vacancies = []
            for item in data.get("items", []):
                vacancy_detail = await self.fetch_vacancy_detail(item["id"])
                if vacancy_detail:
                    vacancies.append(vacancy_detail)
            
            return vacancies
            
        except httpx.RequestError as e:
            print(f"Ошибка запроса: {e}")
            return []
    
    async def fetch_vacancy_detail(self, vacancy_id: str) -> Dict[str, Any]:
        try:
            response = await self.client.get(f"{settings.HH_API_URL}/{vacancy_id}")
            response.raise_for_status()
            return response.json()
        except:
            return {}
    
    def parse_vacancy(self, data: Dict[str, Any]) -> schemas.VacancyCreate:
        salary_from = None
        salary_to = None
        salary_currency = None
        
        if data.get("salary"):
            salary = data["salary"]
            salary_from = salary.get("from")
            salary_to = salary.get("to")
            salary_currency = salary.get("currency")
        
        skills = ", ".join([skill["name"] for skill in data.get("key_skills", [])])
        
        vacancy = schemas.VacancyCreate(
            hh_id=data["id"],
            name=data["name"],
            salary_from=salary_from,
            salary_to=salary_to,
            salary_currency=salary_currency,
            employer=data.get("employer", {}).get("name", "Не указано"),
            experience=data.get("experience", {}).get("name", "Не указано"),
            employment=data.get("employment", {}).get("name", "Не указано"),
            schedule=data.get("schedule", {}).get("name", "Не указано"),
            description=data.get("description", "")[:1000],
            skills=skills,
            area=data.get("area", {}).get("name", "Не указано"),
            url=data.get("alternate_url", ""),
            published_at=datetime.strptime(data["published_at"], "%Y-%m-%dT%H:%M:%S%z")
        )
        
        return vacancy
    
    async def close(self):
        await self.client.aclose()

parser = HHParser()
