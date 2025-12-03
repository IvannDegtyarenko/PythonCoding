from typing import List
from repasitory import TaskRepository
from fastapi import APIRouter, HTTPException, Body, Depends
from schemas import STaskAdd, STask
from typing import Annotated
router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

@router.post("", response_model=dict)
async def add_task(task: Annotated[STaskAdd, Depends()]): 
    """Создать новую задачу"""
    task_id = await TaskRepository.add_task(task)
    return {"ok": True, "task_id": task_id}

@router.get("", response_model=List[STask])
async def get_tasks():
    """Получить все задачи"""
    tasks = await TaskRepository.get_tasks()
    return tasks

@router.get("/{task_id}", response_model=STask)
async def get_task(task_id: int):
    try:
        task = await TaskRepository.get_task_by_id(task_id)
        return task
    except Exception:
        raise HTTPException(status_code=404, detail="Task not found")

@router.put("/{task_id}", response_model=STask)
async def update_task(task_id: int, task: STaskAdd = Body(...)):
    try:
        updated_task = await TaskRepository.update_task(task_id, task)
        return updated_task
    except Exception:
        raise HTTPException(status_code=404, detail="Task not found")

@router.delete("/{task_id}", response_model=dict)
async def delete_task(task_id: int):
    success = await TaskRepository.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"ok": True, "message": "Task deleted"}

@router.post("/{task_id}/complete", response_model=STask)
async def complete_task(task_id: int):
    try:
        task = await TaskRepository.complete_task(task_id)
        return task
    except Exception:
        raise HTTPException(status_code=404, detail="Task not found")