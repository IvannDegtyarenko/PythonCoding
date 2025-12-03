from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_tables, delete_tables
from router import router as tasks_router
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    print("База готова") 
    yield
    await delete_tables()
    print("База очищена")

app = FastAPI(
    title="Todo API", 
    version="1.0.0",
    lifespan=lifespan
)


app.include_router(tasks_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://10.155.179.72:"],  
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "message": "Todo API Server",
        "endpoints": {
            "GET /tasks": "Get all tasks",
            "GET /tasks/{id}": "Get task by ID",
            "POST /tasks": "Create new task",
            "PUT /tasks/{id}": "Update task",
            "DELETE /tasks/{id}": "Delete task",
            "POST /tasks/{id}/complete": "Mark task as complete"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  
        port=8000,
        reload=True
    )