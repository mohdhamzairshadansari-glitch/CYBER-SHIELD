from fastapi import FastAPI, HTTPException
from backend.core.threat_intelligence import check_ip_reputation
from backend.database.mysql import SessionLocal
from backend.models.threat_db import ThreatDB
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


        # -----------------------------
        # Behavioral Analysis
        # -----------------------------

        behavior = analyze_behavior(event)


        # -----------------------------
        # Threat Intelligence
        # -----------------------------

        reputation = check_ip_reputation(
            event.source_ip
        )


        # -----------------------------
        # Combine Risk Scores
        # -----------------------------

        final_risk_score = min(
            100,
            analysis["risk_score"]
            + behavior["risk_boost"]
            + reputation["reputation"]
        )


        # -----------------------------
        # Determine Threat Type
        # -----------------------------

        if behavior["behavior_detected"]:

            final_threat_type = behavior["threat_type"]

        elif reputation["known"]:

            final_threat_type = reputation["threat_type"]

        else:

            final_threat_type = analysis["threat_type"]


        # -----------------------------
        # Store Event
        # -----------------------------

        event_id = save_event(
            event,
            risk_score=final_risk_score,
            threat_type=final_threat_type
        )


        # -----------------------------
        # Build Real-Time Message
        # -----------------------------

        alert = {

            "event_id": event_id,

            "timestamp": event.timestamp.isoformat(),

            "source_ip": event.source_ip,

            "event_type": event.event_type,

            "severity": event.severity,

            "risk_score": final_risk_score,

            "threat_type": final_threat_type,

            "behavior_detected": (
                behavior["behavior_detected"]
            ),

            "behavior_reason": (
                behavior["reason"]
            ),

            "ip_reputation": (
                reputation["reputation"]
            ),

            "ip_known_malicious": (
                reputation["known"]
            ),

            "message": event.message
        }


        # -----------------------------
        # Broadcast to Dashboards
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
@app.get("/threats")
def get_threats():

    db = SessionLocal()

    try:

        threats = (
            db.query(ThreatDB)
            .order_by(ThreatDB.id.desc())
            .limit(100)
            .all()
        )

        return [
            {
                "id": threat.id,
                "event_id": threat.event_id,
                "threat_type": threat.threat_type,
                "risk_score": threat.risk_score,
                "status": threat.status
            }
            for threat in threats
        ]

    finally:

        db.close()
@app.put("/threats/{threat_id}/acknowledge")
def acknowledge_threat(threat_id: int):

    db = SessionLocal()

    try:

        threat = (
            db.query(ThreatDB)
            .filter(ThreatDB.id == threat_id)
            .first()
        )

        if not threat:

            raise HTTPException(
                status_code=404,
                detail="Threat not found"
            )

        threat.status = "ACKNOWLEDGED"

        db.commit()

        db.refresh(threat)

        return {
            "message": "Threat acknowledged",
            "id": threat.id,
            "status": threat.status
        }

    finally:

        db.close()
@app.put("/threats/{threat_id}/resolve")
def resolve_threat(threat_id: int):

    db = SessionLocal()

    try:

        threat = (
            db.query(ThreatDB)
            .filter(ThreatDB.id == threat_id)
            .first()
        )

        if not threat:

            raise HTTPException(
                status_code=404,
                detail="Threat not found"
            )

        threat.status = "RESOLVED"

        db.commit()

        db.refresh(threat)

        return {
            "message": "Threat resolved",
            "id": threat.id,
            "status": threat.status
        }

    finally:

        db.close()