from fastapi import FastAPI, BackgroundTasks
import time

app = FastAPI()

def background_task(name: str):
    for _ in range(10):  # Run for 10 seconds
        print(f"I'm awake, {name}!")
        time.sleep(1)  # Simulate a long-running task

@app.get("/start-task/")
async def start_background_task(name: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(background_task, name)
    return {"message": f"Background task started for {name}. Check your console for updates."}

@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI app!"}
