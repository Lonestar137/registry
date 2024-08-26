import os
from fastapi import FastAPI

app = FastAPI()

@app.post("/create-file")
async def create_file():
    default_text = "This is the default text for the file."
    file_path = "output.txt"
    
    with open(file_path, "w") as file:
        file.write(default_text)
    
    return {"message": f"File created at {file_path} with default text"}

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI server"}
