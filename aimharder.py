from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os, time, pathlib

from utils_selenium import (wait_ready, first_present, find_in_any_frame, clickable, debug_dump )

from cookies import rechazar_cookies    

TZ = ZoneInfo("Europe/Madrid")

def yyyymmdd(d):
    return f"{d.year}{d.month:02d}{d.day:02d}"

def siguiente_dia_objetivo(ahora=None):
    now = (ahora or datetime.now(TZ))
    # si es finde, no ejecutar
    if now.weekday() >= 5:
        return None
    target = (now + timedelta(days=3)).date()
    while target.weekday() >= 5:
        target += timedelta(days=1)
    return target


def _dump_diag(driver, reason="login_timeout"):
    out_dir = pathlib.Path(os.getenv("ARTIFACT_DIR", "/tmp")) / f"diag_{int(time.time())}_{reason}"
    out_dir.mkdir(parents=True, exist_ok=True)
    try:
        out_dir.joinpath("current_url.txt").write_text(driver.current_url)
        out_dir.joinpath("source.html").write_text(driver.page_source)
        driver.get_screenshot_as_file(str(out_dir / "snap.png"))
    except Exception:
        pass
    return out_dir

def login(driver, base_url, user, pwd, timeout=15):
    driver.get(base_url)
    wait_ready(driver, timeout=timeout)
    print("Logearse...")

    try:
        rechazar_cookies(driver)
    except Exception as e:
        print(f"[WARN] rechazar_cookies falló: {e}. Continuamos.")


def seleccionar_dia(driver, dia):
    print(f"Seleccionando día: {dia}")
    dstr = yyyymmdd(dia)
    print(f"Seleccionando día: '{dstr}'")

    

    try:
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return (typeof weekSelDay === 'function');")
        )
        driver.execute_script(f"weekSelDay('{dstr}');")
        return True
    except Exception as e:
        import traceback
        print("[ERROR] Fallo al ejecutar JS:")
        print(e)  # mensaje corto
        traceback.print_exc()  # stacktrace completo en consola
        return False


def seleccionar_clase(driver, nombre="CrossFit"):
    # 1) Intento directo sobre <select>
    try:
        Select(driver.find_element(By.ID, "filtroClases")).select_by_visible_text(nombre)
        print(f"Clase '{nombre}' seleccionada directamente.")
        return True
    except Exception:
        pass
    # 2) Select2: abrir y buscar
    try:
        driver.find_element(By.CSS_SELECTOR, ".select2-selection").click()
        sb = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "select2-search__field"))
        )
        sb.clear(); sb.send_keys(nombre + "\n")
        print(f"Clase '{nombre}' seleccionada mediante búsqueda.")
        return True
    except Exception:
        return False

def reservar(driver, hora="07:00", nombre="CrossFit", timeout=8):
    # Espera a que aparezca el contenedor de clases del día (ID orientativo)
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, "clasesDiaSel"))
        )
    except TimeoutException:
        # fallback: esperar cualquier bloque con la clase de item de clase
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".bloqueClase"))
        )

    # XPaths tolerantes: busca bloques que contengan hora y nombre y botón Reservar
    xpath = (
        "//div[contains(@class,'bloqueClase')]"
        "[.//span[contains(@class,'rvHora') and normalize-space()=$hora]]"
        "[.//span[contains(@class,'rvNombreCl') and contains(., $nombre)]]"
        "//a[contains(@class,'genButton') and contains(.,'Reservar')]"
    )

    # Selenium no soporta variables en XPath nativas; generamos cadena:
    xpath = xpath.replace("$hora", f"'{hora}'").replace("$nombre", f"'{nombre}'")

    boton = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )
    boton.click()
    return True
