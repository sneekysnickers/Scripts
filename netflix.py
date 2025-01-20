# -*- coding: utf-8 -*- 
import imaplib
import email
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# IMAP fiók beállítások
IMAP_SERVER = 'imap.gmail.com'  # Vagy a te e-mail szolgáltatód szervere
EMAIL_ACCOUNT = 'patrikhoszpodar@gmail.com'
EMAIL_PASSWORD = 'boec bgjb uvkp qevj'

# Cél e-mail küldője és tárgya
TARGET_SENDER = 'info@account.netflix.com'
TARGET_SUBJECT = 'Fontos:'

# Selenium böngésző beállítása
CHROME_DRIVER_PATH = '/usr/bin/chromedriver'  # Cseréld ki a ChromeDriver pontos helyére

def check_email_and_click():
    try:
        # IMAP kapcsolat
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        mail.select("Netflix")

        # E-mail keresése
        status, messages = mail.search(None, f'FROM "{TARGET_SENDER}" SUBJECT "{TARGET_SUBJECT}"')
        if status != "OK":
            print("Nem található megfelelő e-mail.")
            return

        # Az utolsó e-mail kinyitása
        email_ids = messages[0].split()
        if not email_ids:
            print("Nincs új e-mail.")
            return

        latest_email_id = email_ids[-1]
        status, msg_data = mail.fetch(latest_email_id, "(RFC822)")
        if status != "OK":
            print("Hiba történt az e-mail letöltésekor.")
            return

        # Az e-mail tartalmának elemzése
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/html":
                            # HTML tartalom dekódolása UTF-8 kódolással
                            html_content = part.get_payload(decode=True).decode('utf-8', 'ignore')
                            soup = BeautifulSoup(html_content, "html.parser")
                            
                            # Az "Igen, én voltam" link keresése a weboldalon
                            link = soup.find('a', string="Igen, én voltam")
                            if link and 'href' in link.attrs:
                                print(f"Megtalált link: {link['href']}")
                                click_button_on_website(link['href'])
                                delete_email(mail, latest_email_id)
                                return  # Sikeres kattintás után kilépünk a funkcióból
                            else:
                                print("Nem található az 'Igen, én voltam' link.")
                                return

        mail.logout()

    except Exception as e:
        print(f"Hiba történt: {e}")

def click_button_on_website(url):
    # Selenium Chrome opciók
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Weboldal megnyitása
        driver.get(url)
        time.sleep(6)  # Várakozás az oldal betöltésére
        
        # Kattintás a cookie elfogadása gombra az ID alapján
        try:
            cookie_accept_button = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            )
            cookie_accept_button.click()
            print("Cookie gomb elfogadva!")
        except Exception as e:
            print(f"Hiba történt a cookie gomb kattintásakor: {e}")

        # Bejelentkezés - Adatok kitöltése
        username = 'patrikhoszpodar@gmail.com'
        password = 'Hatalmasbaj45'
        driver.find_element(By.CSS_SELECTOR, '[name="userLoginId"]').send_keys(username)
        driver.find_element(By.CSS_SELECTOR, '[name="password"]').send_keys(password)

        # Bejelentkezés gomb kattintása
        login_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-uia="login-submit-button"]'))
        )
        login_button.click()
        print("Bejelentkezés sikeres.")

        # Várakozás a "Frissítés megerősítése" gombra, és kattintás
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-uia="set-primary-location-action"]'))
        )

        # Kattintás a Frissítés megerősítése gombra (ha az gomb van)
        update_button = driver.find_element(By.CSS_SELECTOR, '[data-uia="set-primary-location-action"]')
        driver.execute_script("arguments[0].click();", update_button)  # JavaScript kattintás
        print("Frissítés megerősítése gomb kattintva.")

        time.sleep(6)  # Várakozás az akció végrehajtására
    except Exception as e:
        print(f"Hiba történt a weboldalon: {e}")
    finally:
        # Böngésző bezárása
        driver.quit()


def delete_email(mail, email_id):
    try:
        # E-mail törlése
        mail.store(email_id, '+FLAGS', '\\Deleted')  # Törlés jelölése
        mail.expunge()  # Törlés véglegesítése
        print("E-mail törölve.")
    except Exception as e:
        print(f"Hiba történt az e-mail törlésekor: {e}")

if __name__ == "__main__":
    print("Email figyelés indítása...")
    while True:
        check_email_and_click()
        print("Nincs új célzott email. Újraellenőrzés 15 másodperc múlva...")
        time.sleep(15)  # 15 másodpercenként újraellenőrzés
