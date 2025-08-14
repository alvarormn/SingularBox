from zoneinfo import ZoneInfo
import uuid

def build_ics_event(
    start_dt, end_dt, summary, description="", location="", uid=None, tz="Europe/Madrid"
):
    tzinfo = ZoneInfo(tz)
    start_dt = start_dt.astimezone(tzinfo)
    end_dt = end_dt.astimezone(tzinfo)
    uid = uid or f"{uuid.uuid4()}@aimharder-bot"

    def fmt(dt):
        return dt.strftime("%Y%m%dT%H%M%S")

    ics = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//aimharder-bot//EN
CALSCALE:GREGORIAN
METHOD:PUBLISH
BEGIN:VEVENT
UID:{uid}
SUMMARY:{summary}
DESCRIPTION:{description}
DTSTART;TZID={tz}:{fmt(start_dt)}
DTEND;TZID={tz}:{fmt(end_dt)}
LOCATION:{location}
END:VEVENT
END:VCALENDAR
"""
    return ics
