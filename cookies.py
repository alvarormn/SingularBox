from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def rechazar_cookies(driver, timeout=5):
    """Intenta ejecutar denyAllBtn() y si falla, hace clic en 'Denegar todas'."""
    try:
        driver.execute_script("denyAllBtn && denyAllBtn();")
        return True
    except Exception:
        pass
    # Fallback por texto
    try:
        btn = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Denegar todas')]"))
        )
        btn.click()
        return True
    except Exception:
        return False
