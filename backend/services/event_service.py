from backend.database.mysql import SessionLocal
from backend.database.mongodb import raw_events

from backend.models.security_event_db import SecurityEventDB
from backend.models.threat_db import ThreatDB


def save_event(
    event,
    risk_score=0,
    threat_type=None
):

    db = SessionLocal()

    try:

        # ==================================================
        # SAVE EVENT TO MYSQL
        # ==================================================

        mysql_event = SecurityEventDB(
            timestamp=event.timestamp,
            source_ip=event.source_ip,
            destination_ip=event.destination_ip,
            event_type=event.event_type,
            severity=event.severity,
            username=event.username,
            message=event.message,
            risk_score=risk_score
        )

        db.add(mysql_event)

        db.commit()

        db.refresh(mysql_event)


        # ==================================================
        # SAVE THREAT TO MYSQL
        # ==================================================

        if threat_type and risk_score >= 60:

            threat = ThreatDB(
                event_id=mysql_event.id,
                threat_type=threat_type,
                risk_score=risk_score,
                status="OPEN"
            )

            db.add(threat)

            db.commit()


        # ==================================================
        # SAVE RAW EVENT TO MONGODB
        # ==================================================

        mongo_event = event.model_dump(
            mode="json"
        )

        mongo_event["mysql_event_id"] = (
            mysql_event.id
        )

        raw_events.insert_one(
            mongo_event
        )


        # ==================================================
        # RETURN MYSQL EVENT ID
        # ==================================================

        return mysql_event.id


    except Exception:

        db.rollback()

        raise


    finally:

        db.close()