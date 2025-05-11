from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

# Cartella dove salvare i .lrc
output_folder = "lyrics"
os.makedirs(output_folder, exist_ok=True)

# Impostazioni per disabilitare JavaScript
options = Options()
#options.add_argument("--headless")  # Modalità headless (facoltativa)
options.add_argument("--window-size=1920,1080")  # Imposta una dimensione della finestra
options.add_experimental_option("prefs", {
    "profile.managed_default_content_settings.javascript": 2  # Disabilita JavaScript
})

# PERCORSO a chromedriver.exe
driver_path = "driver/chromedriver.exe"  # <--- Cambia questo percorso

# Creazione del servizio e driver
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

def download_lrc(url, title):
    driver.get(url)
    try:
        # Attendi che il bottone di download sia visibile e cliccalo
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "lrc_file_download"))
        )
        download_button = driver.find_element(By.ID, "lrc_file_download")
        download_button.click()  # Simula il click sul bottone di download
        time.sleep(3)  # Aspetta che il download inizi

        # Recupera il testo del file .lrc
        pre = driver.find_element(By.CSS_SELECTOR, "pre.lrc")
        lrc_text = pre.text
        filename = os.path.join(output_folder, f"{title}.lrc")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(lrc_text)
        print(f"[✓] Salvato: {title}")
    except Exception as e:
        print(f"[!] Errore durante il download del file per {title}: {e}")

def scrape_lyricsify(pages=5):
    for page in range(1, pages + 1):
        print(f"\n--- Pagina {page} ---")
        driver.get(f"https://www.lyricsify.com/search?q=caparezza&page={page}")
        time.sleep(2)  # Aspetta che la pagina carichi

        # Verifica se i risultati sono visibili (se la pagina è stata caricata correttamente)
        try:
            links = driver.find_elements(By.CSS_SELECTOR, "a.title.font-bold")
            if not links:
                print("Nessun risultato trovato. Fine.")
                break
            for link in links:
                href = link.get_attribute("href")
                title = link.text.strip().replace("/", "-")
                download_lrc(href, title)
                time.sleep(1)  # Pausa tra i download per evitare il blocco
        except Exception as e:
            print(f"[!] Errore durante il recupero dei dati: {e}")

scrape_lyricsify(pages=5)

# Chiudi il driver alla fine
driver.quit()
