from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import subprocess
from typing import Any

app = FastAPI()

# ✅ Allow requests from your frontend (use your actual domain in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with ["http://localhost:5173"] or your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Script(BaseModel):
    code: str

@app.post("/execute/")
async def execute_script(script: Script) -> Any:
    try:
        # Save the code to a temporary Python file
        with open("temp_script.py", "w") as file:
            file.write(script.code)

        # Run the script
        result = subprocess.run(
            ["python3", "temp_script.py"], capture_output=True, text=True
        )

        # Clean up the temporary file
        subprocess.run(["rm", "temp_script.py"], shell=True)

        return {"stdout": result.stdout, "stderr": result.stderr}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
