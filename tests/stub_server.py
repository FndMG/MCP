"""
API Stub Server for testing.
Supports busy state simulation.
"""

import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI(title="API Stub Server")

# Stub state
class StubState:
    busy: bool = False
    busy_delay: float = 5.0
    response_delay: float = 0.0

state = StubState()


# Control endpoints
class BusyConfig(BaseModel):
    busy: bool
    delay: Optional[float] = 5.0

@app.post("/stub/config/busy")
async def set_busy(config: BusyConfig):
    """Set busy state for the stub server."""
    state.busy = config.busy
    state.busy_delay = config.delay or 5.0
    return {"busy": state.busy, "delay": state.busy_delay}

@app.get("/stub/config/busy")
async def get_busy():
    """Get current busy state."""
    return {"busy": state.busy, "delay": state.busy_delay}

@app.post("/stub/config/delay")
async def set_delay(delay: float):
    """Set response delay for all endpoints."""
    state.response_delay = delay
    return {"delay": state.response_delay}


# Simulated API endpoints
async def check_busy():
    """Check if server is busy and apply delay."""
    if state.busy:
        raise HTTPException(status_code=503, detail="Service temporarily unavailable")
    if state.response_delay > 0:
        await asyncio.sleep(state.response_delay)


@app.get("/templates")
async def get_templates():
    """Get template list."""
    await check_busy()
    return {
        "template_list": [
            {
                "template_id": 1,
                "account": 100,
                "valid": 1,
                "template_name": "Template A",
                "to_adr": "to@example.com",
                "cc_adr": "cc@example.com",
                "subject": "Subject A"
            },
            {
                "template_id": 2,
                "account": 100,
                "valid": 1,
                "template_name": "Template B",
                "to_adr": "to2@example.com",
                "cc_adr": "",
                "subject": "Subject B"
            }
        ]
    }

@app.get("/templates/{template_id}")
async def get_template_detail(template_id: int):
    """Get template detail."""
    await check_busy()

    templates = {
        1: {
            "template_id": 1,
            "account": 100,
            "valid": 1,
            "template_name": "Template A",
            "to_adr": "to@example.com",
            "cc_adr": "cc@example.com",
            "subject": "Subject A",
            "body": "This is the body of Template A."
        },
        2: {
            "template_id": 2,
            "account": 100,
            "valid": 1,
            "template_name": "Template B",
            "to_adr": "to2@example.com",
            "cc_adr": "",
            "subject": "Subject B",
            "body": "This is the body of Template B."
        }
    }

    if template_id not in templates:
        raise HTTPException(status_code=404, detail="Template not found")

    return templates[template_id]


# --- System2: User endpoints ---

@app.get("/users")
async def get_users():
    """Get user list."""
    await check_busy()
    return {
        "user_list": [
            {
                "user_id": 1,
                "name": "Alice",
                "email": "alice@example.com",
                "role": "admin"
            },
            {
                "user_id": 2,
                "name": "Bob",
                "email": "bob@example.com",
                "role": "member"
            }
        ]
    }

@app.get("/users/{user_id}")
async def get_user_detail(user_id: int):
    """Get user detail."""
    await check_busy()

    users = {
        1: {
            "user_id": 1,
            "name": "Alice",
            "email": "alice@example.com",
            "role": "admin"
        },
        2: {
            "user_id": 2,
            "name": "Bob",
            "email": "bob@example.com",
            "role": "member"
        }
    }

    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")

    return users[user_id]


# --- Common endpoints ---

@app.get("/login")
async def login():
    """Login endpoint."""
    await check_busy()
    return {"status": "ok", "token": "dummy_token_12345"}

@app.get("/logout")
async def logout():
    """Logout endpoint."""
    await check_busy()
    return {"status": "ok"}


def run_stub_server(host: str = "0.0.0.0", port: int = 8081):
    """Run the stub server."""
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    run_stub_server()
