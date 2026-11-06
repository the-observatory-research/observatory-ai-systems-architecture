from typing import Any
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


class LatestPulseResponse(BaseModel):
    pulse_number: int
    text: str


def create_dashboard_api(memory: Any) -> FastAPI:
    app = FastAPI(title="Horizon Dashboard API")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["GET"],
        allow_headers=["*"],
    )

    app.state.memory = memory

    @app.get(
        "/api/v1/pulse/latest",
        response_model=LatestPulseResponse,
    )
    def latest_pulse(request: Request) -> LatestPulseResponse:
        memory = request.app.state.memory
        pulse_count = memory.get_pulse_count()
        latest = memory.get_latest_pulse()

        text = latest["content"] if latest else "Awaiting first pulse..."

        return LatestPulseResponse(
            pulse_number=pulse_count,
            text=text,
        )

    return app