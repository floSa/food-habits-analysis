from playwright.sync_api import sync_playwright
import time
import os

OUTPUT_DIR = "docs/screenshots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

BASE_URL = "http://localhost:8507"

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 1024})
        page = context.new_page()

        print(f"Navigating to {BASE_URL}...")
        try:
            page.goto(BASE_URL, timeout=10000)
            page.wait_for_load_state("networkidle")
            time.sleep(3) # Wait for Streamlit to fully render
            
            # 1. Home Page
            print("Capturing Home...")
            page.screenshot(path=f"{OUTPUT_DIR}/0_home.png", full_page=True)

            # 2. Population Page
            print("Navigating to Population...")
            # Streamlit sidebar navigation might be tricky with selectors, usually they are links or buttons.
            # We can try to navigate via URL if Streamlit MPA is set up, but sidebar clicks are safer.
            # Sidebar items are usually 'ul[data-testid="stSidebarNavItems"] > li > div > a'
            
            # Let's try direct clickable items in sidebar
            page.get_by_text("Population").click()
            time.sleep(3)
            page.screenshot(path=f"{OUTPUT_DIR}/1_population.png", full_page=True)
            
            # Check for Debug Expander content?
            # expander = page.get_by_text("Debug : Vérification des Données")
            # if expander.is_visible():
            #    expander.click()
            #    time.sleep(1)
            #    page.screenshot(path=f"{OUTPUT_DIR}/1_population_debug.png")

            # 3. Habitudes Page
            print("Navigating to Habitudes...")
            page.get_by_text("Habitudes").click()
            time.sleep(3)
            page.screenshot(path=f"{OUTPUT_DIR}/2_habitudes.png", full_page=True)

            # 4. Sociologie
            print("Navigating to Sociologie...")
            page.get_by_text("Sociologie").click()
            time.sleep(5) # MCA calculation might take time
            page.screenshot(path=f"{OUTPUT_DIR}/3_sociologie.png", full_page=True)

            # 5. Marketing
            print("Navigating to Marketing...")
            page.get_by_text("Marketing").click()
            time.sleep(2)
            page.screenshot(path=f"{OUTPUT_DIR}/4_marketing.png", full_page=True)

            print("All screenshots captured!")

        except Exception as e:
            print(f"Error during navigation: {e}")
            page.screenshot(path=f"{OUTPUT_DIR}/error_state.png")
            
        finally:
            browser.close()

if __name__ == "__main__":
    run()
