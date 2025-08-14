import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from respond import parse_booking_response


def yyyymmdd(d):
    return f"{d.year}{d.month:02d}{d.day:02d}"

def get_id_class(dia):
    dstr = yyyymmdd(dia)
    url = "https://singularbox.aimharder.com/api/bookings"
    params = {
        "day": dstr,
        "familyId": "",
        "box": "4455"
    }

    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://singularbox.aimharder.com/",
        "X-Requested-With": "XMLHttpRequest",
    }

    resp = requests.get(url, params=params, headers=headers, allow_redirects=False, timeout=20)

    # Debug robusto
    ct = (resp.headers.get("content-type") or "").lower()

    data = resp.json()
    id_value = next((b["id"] for b in data["bookings"] if b["time"] == "07:00 - 08:00"), None)
    if not id_value:
        raise RuntimeError(f"No se encontró ID de clase para {dstr} a las 07:00")
    print(f"Reserva ID: {id_value}")
    return id_value

def bookClass(driver, id, element, code):
    """Realiza la reserva de una clase."""
    # 1) Inyecta un hook a $.ajax para capturar la respuesta
    driver.execute_script("""
    (function(){
      if (window.__ajaxHooked) return;
      window.__ajaxHooked = true;
      window.__lastBookResp = null;

      const origAjax = $.ajax;
      $.ajax = function(opts){
        const userSuccess = opts && opts.success;
        const userError   = opts && opts.error;

        const wrapped = Object.assign({}, opts, {
          success: function(xhr){
            try {
              var resp = (typeof xhr === 'string') ? JSON.parse(xhr) : xhr;
              window.__lastBookResp = resp;  // <-- aquí guardamos la respuesta
            } catch(e) {
              window.__lastBookResp = { parseError: String(e), raw: xhr };
            }
            if (userSuccess) return userSuccess.apply(this, arguments);
          },
          error: function(){
            window.__lastBookResp = { ajaxError: true };
            if (userError) return userError.apply(this, arguments);
          }
        });
        return origAjax.call(this, wrapped);
      };
    })();
    """)


    # 2) Llama a bookClass con el mismo elemento (HTMLAnchorElement)
    driver.execute_script("window.__lastBookResp = null; bookClass(arguments[0], arguments[1], arguments[2]);",
                        id, element, code)

    # 3) Espera a que llegue la respuesta y léela
    resp = WebDriverWait(driver, 10).until(
        lambda d: d.execute_script("return window.__lastBookResp;")
    )
    print("Respuesta de reserva:", resp)
    info = parse_booking_response(resp)
    print(info["status"], info["code"], info["state"], "-", info["detail"])
    success = info["status"] == "ok"
    return success, info["detail"]
    




