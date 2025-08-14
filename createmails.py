from email_utils import send_email
from calendar_utils import build_ics_event
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

def create_email(target,state, mensaje):
    try:
        start_dt = datetime.combine(target, datetime.strptime("07:00","%H:%M").time()).replace(tzinfo=ZoneInfo("Europe/Madrid"))
        end_dt = start_dt + timedelta(hours=1)
        if state:
            subject = f"Reserva CrossFit {target} 07:00 - 8:00"
            body = f"<p>Reserva realizada para <b>{target} 07:00 - 8:00</b> (CrossFit).</p>"
            ics = build_ics_event(
                start_dt, end_dt,
                summary="CrossFit 07:00-8:00",
                description="Reserva realizada automáticamente por aimharder-bot",
                location="CrossFit Singular Box, C. Ramón de Aguinaga 13, Madrid"
            )
            send_email(subject=subject, body_html=body, ics_content=ics, ics_filename={f"CrossFit_{target}_0700.ics"})
            
        else:
            subject = f"Reserva NO realizada en CrossFit {target} 07:00 - 8:00"
            body = f"<p>No se pudo realizar la reserva para <b>{target} 07:00 - 8:00</b> (CrossFit).</p><p>Motivo: {mensaje}</p>"
            send_email(subject=subject, body_html=body)
    
        print("Notificación por email enviada.")
    except Exception as e:
        print(f"Advertencia: no se pudo enviar el email/ICS: {e}")