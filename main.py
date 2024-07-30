from fastapi import FastAPI, Request
from starlette.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
import traceback
import time
from dotenv import load_dotenv
import os

load_dotenv()

from routers import config, scanOrg, scanRepo, whitelistSecret, webhookConfig, logs, webhookScanSecret, dashboard
from services.helpers.logService import LogService

app = FastAPI()

my_values = os.getenv('CORS_ORIGINS')

# Convert the comma-separated string to a Python list
if my_values:
    origins = my_values.split(',')
else:
    origins = []


# Add CORSMiddleware to the application instance
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Allows specified origins
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods
    allow_headers=["*"], # Allows all headers
)
'''
def send_slack_notification(message: str):
    payload = {"text": message}
    SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"
    response = requests.post(SLACK_WEBHOOK_URL, json=payload)
    # Check response status code for success/failure
    response.raise_for_status()


@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        
        body = await request.body()
        start_time = time.time()
        response =  await call_next(request)
        process_time = time.time() - start_time

        # Prepare the log record with request time
        log_data = {
            "request_time": start_time,  # Unix timestamp of the request time
            "request_method": request.method,
            "request_path": request.url.path,
            "request_body": body,
            "response_status": response.status_code,
            "process_time": process_time,
        }

        #logger.info(response)
        # Insert the log record into MongoDB
        LogService.insertLogs(log_data)

        return response
    except Exception as exc:
        error_trace = traceback.format_exc()
        send_slack_notification(f"Internal Server Error:\n```\n{error_trace}\n```")
        return JSONResponse(
            content={"detail": "Internal Server Error"},
            status_code=500
        )
'''

app.include_router(config.router)
app.include_router(scanOrg.router)
app.include_router(scanRepo.router)
app.include_router(whitelistSecret.router)
app.include_router(webhookConfig.router)
app.include_router(logs.router)
app.include_router(webhookScanSecret.router)
app.include_router(dashboard.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
