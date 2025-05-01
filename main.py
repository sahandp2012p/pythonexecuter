from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
from typing import Any

app = FastAPI()

class Script(BaseModel):
    code: str

@app.post("/execute/")
async def execute_script(script: Script) -> Any:
    try:
        # Save the code to a temporary Python file
        with open("temp_script.py", "w") as file:
            file.write(script.code)

        # Run the script using subprocess (adjusted for Windows)
        result = subprocess.run(
            ["python3", "temp_script.py"], capture_output=True, text=True
        )

        # Remove the temporary script file after execution
        subprocess.run(["rm", "temp_script.py"], shell=True)

        # Return the standard output or error
        return {"stdout": result.stdout, "stderr": result.stderr}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
