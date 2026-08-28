from fastapi import FastAPI, HTTPException

from backend.models.security_event import SecurityEvent
from backend.services.event_service import save_event
from backend.core.behavior_analyzer import analyze_behavior, analyze_behavior
from backend.core.threat_detector import calculate_risk
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from backend.core.websocket_manager import manager
from sqlalchemy import text
from backend.database.mysql import engine



app = FastAPI(
    title="CyberShield API",
    description="Real-Time Cybersecurity Monitoring API",
    version="1.0.0"
)
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await manager.connect(websocket)

    try:

        while True:

            await websocket.receive_text()

    except WebSocketDisconnect:

        manager.disconnect(websocket)

@app.get("/")
def root():

    return {
        "message": "CyberShield API is running",
        "status": "online"
    }


@app.post("/events")
async def receive_event(event: SecurityEvent):

    try:

        # -----------------------------
        # Threat Detection
        # -----------------------------

        analysis = calculate_risk(event)

        event.severity = analysis["severity"]
        behavior = analyze_behavior(event)
        final_risk_score = min(
    100,
    analysis["risk_score"] + behavior["risk_boost"]
)
        final_threat_type = (
    behavior["threat_type"]
    if behavior["behavior_detected"]
    else analysis["threat_type"]
)
        # -----------------------------
        # Store Event
        # -----------------------------

        event_id = save_event(
    event,
    risk_score=final_risk_score,
    threat_type=final_threat_type
)

        # -----------------------------
        # Build real-time message
        # -----------------------------

        alert = {
            "event_id": event_id,
            "timestamp": event.timestamp.isoformat(),
            "source_ip": event.source_ip,
            "event_type": event.event_type,
            "severity": event.severity,
            "risk_score": final_risk_score,
            "threat_type": final_threat_type,
            "behavior_detected": behavior["behavior_detected"],
            "behavior_reason": behavior["reason"],
            "message": event.message
        }

        # -----------------------------
        # Broadcast to dashboards
        # -----------------------------

        await manager.broadcast(alert)

        return {
            "status": "stored",
            **alert
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
@app.get("/events")
def get_events():

    query = text(
        """
        SELECT
            id,
            timestamp,
            source_ip,
            destination_ip,
            event_type,
            severity,
            username,
            message,
            risk_score
        FROM security_events
        ORDER BY id DESC
        LIMIT 100
        """
    )

    with engine.connect() as connection:

        result = connection.execute(query)

        events = [
            dict(row._mapping)
            for row in result
        ]

    return events
@app.get("/stats")
def get_stats():

    query = text(
        """
        SELECT
            COUNT(*) AS total_events,

            SUM(
                CASE
                    WHEN severity = 'CRITICAL'
                    THEN 1
                    ELSE 0
                END
            ) AS critical_events,

            SUM(
                CASE
                    WHEN severity = 'HIGH'
                    THEN 1
                    ELSE 0
                END
            ) AS high_events,

            SUM(
                CASE
                    WHEN risk_score >= 60
                    THEN 1
                    ELSE 0
                END
            ) AS detected_threats

        FROM security_events
        """
    )

    with engine.connect() as connection:

        result = connection.execute(query).mappings().one()

    return {
        "total_events": result["total_events"] or 0,
        "critical_events": result["critical_events"] or 0,
        "high_events": result["high_events"] or 0,
        "detected_threats": result["detected_threats"] or 0
    }