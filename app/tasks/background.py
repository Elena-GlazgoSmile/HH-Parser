import asyncio
from datetime import datetime
from app.services.parser import parser
from app.services.nats_client import nats_client
from app.websocket.ws_manager import manager
from app.database import get_db
from app.crud import crud_vacancy
from app.config import settings

class BackgroundTask:
    def __init__(self):
        self.is_running = False
        self.task_id = None
    
    async def run(self, manual: bool = False):
        if self.is_running and not manual:
            return {"status": "already_running"}
        
        self.is_running = True
        self.task_id = datetime.utcnow().isoformat()
        
        try:
            print(f"Запуск фоновой задачи: {self.task_id}")
            
            data = await parser.fetch_vacancies("Python", 1)
            
            new_vacancies = 0
            updated_vacancies = 0
            
            async for session in get_db():
                for vacancy_data in data:
                    parsed_vacancy = parser.parse_vacancy(vacancy_data)
                    
                    existing = await crud_vacancy.get_by_hh_id(session, parsed_vacancy.hh_id)
                    
                    if not existing:
                        await crud_vacancy.create(session, parsed_vacancy)
                        new_vacancies += 1
                        
                        await manager.broadcast({
                            "type": "new_vacancy",
                            "data": {
                                "id": parsed_vacancy.hh_id,
                                "name": parsed_vacancy.name,
                                "employer": parsed_vacancy.employer,
                                "salary_from": parsed_vacancy.salary_from,
                                "salary_to": parsed_vacancy.salary_to
                            },
                            "timestamp": datetime.utcnow().isoformat()
                        })
                    
                await session.commit()
            
            if new_vacancies > 0:
                await nats_client.publish(
                    settings.NATS_SUBJECT,
                    {
                        "type": "new_vacancies",
                        "task_id": self.task_id,
                        "count": new_vacancies,
                        "timestamp": datetime.utcnow().isoformat()
                    }
                )
            
            result = {
                "status": "success",
                "task_id": self.task_id,
                "timestamp": datetime.utcnow().isoformat(),
                "vacancies_found": len(data),
                "new_vacancies": new_vacancies,
                "updated_vacancies": updated_vacancies
            }
            
            print(f"Задача завершена: {len(data)} вакансий, {new_vacancies} новых")
            
            return result
            
        except Exception as e:
            error_msg = str(e)
            print(f"Ошибка в фоновой задаче: {error_msg}")
            
            await manager.broadcast({
                "type": "task_error",
                "task_id": self.task_id,
                "timestamp": datetime.utcnow().isoformat(),
                "error": error_msg
            })
            
            return {
                "status": "error",
                "task_id": self.task_id,
                "error": error_msg
            }
            
        finally:
            if not manual:
                self.is_running = False
    
    async def start_periodic(self):
        while True:
            await self.run()
            await asyncio.sleep(settings.BACKGROUND_TASK_INTERVAL)

background_task = BackgroundTask()
