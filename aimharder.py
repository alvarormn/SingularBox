from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

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

def login(driver, base_url, usuario, contrasena, timeout=10):
    driver.get(base_url)
    # Espera el formulario de login
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.ID, "frmLogin"))
    )
    driver.find_element(By.ID, "mail").clear()
    driver.find_element(By.ID, "mail").send_keys(usuario)
    driver.find_element(By.ID, "pw").clear()
    driver.find_element(By.ID, "pw").send_keys(contrasena)
    driver.find_element(By.ID, "loginSubmit").click()
    # Heurística: espera que desaparezca el login o aparezca algo de sesión
    try:
        WebDriverWait(driver, timeout).until_not(
            EC.presence_of_element_located((By.ID, "frmLogin"))
        )
    except TimeoutException:
        pass
    return True

def seleccionar_dia(driver, dia):
    dstr = yyyymmdd(dia)
    # Opción A: click sobre el ancla visible
    try:
        link = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f"#weekDays a.wds{dstr}"))
        )
        link.click()
        return True
    except Exception:
        # Opción B: helper JS
        try:
            driver.execute_script(f"weekSelDay('{dstr}');")
            return True
        except Exception:
            return False

def seleccionar_clase(driver, nombre="CrossFit"):
    # 1) Intento directo sobre <select>
    try:
        Select(driver.find_element(By.ID, "filtroClases")).select_by_visible_text(nombre)
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
