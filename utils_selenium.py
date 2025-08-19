from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import textwrap

def wait_ready(driver, timeout=15):
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

def first_present(driver, locators, timeout=10):
    """Espera el primero que aparezca de una lista de localizadores."""
    end = time.time() + timeout
    last_err = None
    while time.time() < end:
        for by, sel in locators:
            els = driver.find_elements(by, sel)
            if els:
                return (by, sel, els[0])
        time.sleep(0.2)
    raise TimeoutException(f"No apareció ninguno de: {locators}") from last_err

def find_in_any_frame(driver, by, selector, timeout=5):
    """Busca un elemento en la página principal y, si no, recorre iframes."""
    # default content
    try:
        el = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, selector))
        )
        return el, None  # no frame
    except TimeoutException:
        pass

    # probar iframes
    frames = driver.find_elements(By.TAG_NAME, "iframe")
    for idx, fr in enumerate(frames):
        driver.switch_to.frame(fr)
        try:
            el = WebDriverWait(driver, 1.5).until(
                EC.presence_of_element_located((by, selector))
            )
            return el, idx
        except TimeoutException:
            driver.switch_to.default_content()
            continue
    # volver siempre a default
    driver.switch_to.default_content()
    raise TimeoutException(f"No se encontró {selector} ni en página ni en iframes")

def clickable(driver, by, selector, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, selector))
    )

def debug_dump(driver, prefix="login"):
    path_png = f"/app/{prefix}_timeout.png"
    driver.save_screenshot(path_png)
    html = driver.page_source
    # loggea solo los primeros 3000 chars para no inundar logs
    print(f"[DEBUG] URL: {driver.current_url}")
    print(f"[DEBUG] Screenshot guardado en: {path_png}")
    print("[DEBUG] HTML (parcial):")
    print(textwrap.shorten(html, width=3000, placeholder="... [truncado] ..."))