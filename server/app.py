from fastapi import FastAPI
from server.environment import FraudEnv
from tasks.easy import transactions as easy_transactions

app = FastAPI(
    docs_url="/docs",
    redoc_url=None,
    openapi_url="/openapi.json"
)

GLOBAL_ENV = None

@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Fraud AI Environment is running"
    }

@app.post("/reset")
def reset():
    global GLOBAL_ENV

    GLOBAL_ENV = FraudEnv(easy_transactions)
    result = GLOBAL_ENV.reset()

    return {
        "state": result["state"],
        "reward": result["reward"],
        "done": result["done"]
    }

@app.post("/step")
def step(action: dict):
    global GLOBAL_ENV

    if GLOBAL_ENV is None:
        return {"error": "Environment not initialized. Call /reset first."}

    result = GLOBAL_ENV.step(action["action"])

    return {
        "state": result["state"],
        "reward": result["reward"],
        "done": result["done"]
    }

@app.get("/health")
def health():
    return {"status": "ok"}