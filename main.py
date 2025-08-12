from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from config import AIMHARDER_URL, USUARIO, CONTRASENA
from cookies import rechazar_cookies
from aimharder import (
    siguiente_dia_objetivo,
    seleccionar_dia,
    seleccionar_clase,
    reservar,
    login,
)

def start_driver(headless=True):
    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1200,1000")
    return webdriver.Chrome(options=opts)

def main():
    target = siguiente_dia_objetivo()
    print(f"Objetivo: {target}")
    if not target:
        print("Hoy es fin de semana. No se ejecuta.")
        return

    driver = start_driver(headless=True)
    try:
        login(driver, AIMHARDER_URL, USUARIO, CONTRASENA)
        #rechazar_cookies(driver)
        driver.get('https://singularbox.aimharder.com/schedule?cl')
        if not seleccionar_dia(driver, target):
            raise RuntimeError(f"No pude seleccionar el día objetivo {target}")
        else:
            print(f"Día objetivo {target} seleccionado ✔")

        if not seleccionar_clase(driver, "CrossFit"):
            raise RuntimeError("No pude fijar el filtro de clase en 'CrossFit'")

        if reservar(driver, hora="07:00", nombre="CrossFit"):
            print(f"Reserva intentada para {target} 07:00 CrossFit ✔")
        else:
            print(f"No se pudo reservar {target} 07:00 CrossFit ✖")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
