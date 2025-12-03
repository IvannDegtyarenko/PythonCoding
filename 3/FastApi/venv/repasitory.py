from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound
from database import TaskOrm, new_session
from schemas import STaskAdd, STask

class TaskRepository:
    @classmethod
    async def add_task(cls, data: STaskAdd) -> int:
        async with new_session() as session:
            task_dict = data.model_dump()
            task = TaskOrm(**task_dict)
            session.add(task)
            await session.commit()
            await session.refresh(task)
            return task.id

    @classmethod
    async def get_tasks(cls) -> list[STask]:
        async with new_session() as session:
            query = select(TaskOrm)
            result = await session.execute(query)
            task_models = result.scalars().all()
            tasks = [STask.model_validate(task_model) for task_model in task_models]
            return tasks

    @classmethod
    async def get_task_by_id(cls, task_id: int) -> STask:
        async with new_session() as session:
            query = select(TaskOrm).where(TaskOrm.id == task_id)
            result = await session.execute(query)
            task_model = result.scalar_one_or_none()
            if not task_model:
                raise NoResultFound(f"Task with id {task_id} not found")
            return STask.model_validate(task_model)

    @classmethod
    async def update_task(cls, task_id: int, data: STaskAdd) -> STask:
        async with new_session() as session:
            query = select(TaskOrm).where(TaskOrm.id == task_id)
            result = await session.execute(query)
            task_model = result.scalar_one_or_none()
            
            if not task_model:
                raise NoResultFound(f"Task with id {task_id} not found")
            
            for key, value in data.model_dump().items():
                setattr(task_model, key, value)
            
            await session.commit()
            await session.refresh(task_model)
            return STask.model_validate(task_model)

    @classmethod
    async def delete_task(cls, task_id: int) -> bool:
        async with new_session() as session:
            query = delete(TaskOrm).where(TaskOrm.id == task_id)
            result = await session.execute(query)
            await session.commit()
            return result.rowcount > 0

    @classmethod
    async def complete_task(cls, task_id: int) -> STask:
        async with new_session() as session:
            query = select(TaskOrm).where(TaskOrm.id == task_id)
            result = await session.execute(query)
            task_model = result.scalar_one_or_none()
            
            if not task_model:
                raise NoResultFound(f"Task with id {task_id} not found")
            
            task_model.completed = True
            await session.commit()
            await session.refresh(task_model)
            return STask.model_validate(task_model)