from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


from config import AIMHARDER_URL, USUARIO, CONTRASENA
from cookies import rechazar_cookies
from call import (
    get_id_class,
    bookClass
)
from utils_selenium import (wait_ready, first_present, find_in_any_frame, clickable, debug_dump )
from createmails import create_email
from aimharder import (
    siguiente_dia_objetivo,
    seleccionar_dia,
    seleccionar_clase,
    reservar,
    login,
)

def start_driver(headless=True):
    opts = Options()
    for a in ["--headless=new", "--no-sandbox", "--disable-dev-shm-usage", "--window-size=1366,900"]:
        opts.add_argument(a)
    opts.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
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
        driver.get('https://singularbox.aimharder.com/schedule?cl')
        wait_ready(driver)
        rechazar_cookies(driver)
        
        if not seleccionar_dia(driver, target):
            raise RuntimeError(f"No pude seleccionar el día objetivo {target}")
        else:
            print(f"Día objetivo {target} seleccionado ✔")
        
        id_class = get_id_class(target)
        boton = driver.find_element(By.XPATH, f'//a[contains(@onclick, "bookClass({id_class}, this, 0)")]')

        ok, mensaje = bookClass(driver, id_class, boton, 0)

        if not ok:
            print(f"No se pudo reservar la clase para {target} 07:00 CrossFit ✖")
            print(f"Mensaje: {mensaje}")
            create_email(target,ok,mensaje)
            driver.quit()
        else: 
            if ok:
                print(f"Reserva con exito para {target} 07:00 - 08:00 CrossFit ✔")
                create_email(target,ok,mensaje)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
