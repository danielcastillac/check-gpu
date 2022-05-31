from fastapi import FastAPI
import subprocess
import psutil

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Check GPU service running."}

@app.get("/check_gpu_verbose")
async def gpu_usage():
    result = subprocess.run(
        ["nvidia-smi"], capture_output = True,
        text=True
    )
    return {"GPU":str(result.stdout)}

@app.get("/check_gpu")
async def gpu_usage():
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=timestamp,name,utilization.gpu,utilization.memory,memory.used,memory.free,memory.total", "--format=csv,noheader"], capture_output = True,
            text=True
        )
        return {"GPU":str(result.stdout)}
    except Exception as e:
        return {"GPU": str(e)}

@app.get("/free_gpu_resources")
async def free_gpu_resources():
    try:
        proc_PID = [proc.pid for proc in psutil.process_iter() if proc.name() == 'python3']
        proc = str(proc_PID[0])
        subprocess.run(["sudo", "kill", "-9", proc])
        subprocess.run(["docker-compose", "up", "-d"], cwd="/home/ubuntu/src")
        return {"GPU": "Succesfully restarted GPU usage."}
    except Exception as e:
        return {"GPU": str(e)}