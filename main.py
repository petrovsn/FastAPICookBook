from fastapi import APIRouter, FastAPI,Request, Response
import uvicorn
from api.routes.route1 import router_mod1
from api.routes.route2 import router_mod2
from starlette.responses import JSONResponse

app = FastAPI()

app.include_router(router_mod1)
app.include_router(router_mod2)

@app.exception_handler(Exception)
async def value_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": str(exc),
        },
    )

@app.middleware("http")
async def execution_timer(request: Request, call_next):
    import time
    start = time.perf_counter()
    try:
        response = await call_next(request)
        stop = time.perf_counter()
        delta = stop - start
        response.headers["X-Execution-Time"] = f"{delta}"
        return response

    except Exception as e:
        print("Middlware exception:",e)
        
    finally:
        stop = time.perf_counter()
        delta = stop - start
        print(f"Request {request} completed for {delta} sec")
        

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
    )