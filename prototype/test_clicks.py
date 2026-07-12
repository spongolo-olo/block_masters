import asyncio
import os
from playwright.sync_api import sync_playwright

def run_click_test():
    print("Starting click simulation test...")
    logs = []
    errors = []

    with sync_playwright() as p:
        # Launch headless browser
        browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-setuid-sandbox"])
        page = browser.new_page(viewport={"width": 1280, "height": 720})

        # Subscribe to console and error events
        page.on("console", lambda msg: logs.append(f"[{msg.type.upper()}] {msg.text}"))
        page.on("pageerror", lambda err: errors.append(f"EXCEPTION: {err.message}"))

        # Navigate to prototype
        page.goto("http://localhost:8004/", wait_until="networkidle")
        page.wait_for_timeout(2000)

        # Clear logs to focus on our action clicks
        logs.clear()

        # Click at (640, 310) which we know hits the square face (0, 2, 0)
        center_x = 640
        center_y = 310
        
        print(f"Clicking square face at ({center_x}, {center_y})...")
        page.mouse.move(center_x, center_y)
        page.mouse.down()
        page.mouse.up()
        page.wait_for_timeout(2000) # Give it 2 seconds to make the API call and log

        browser.close()

    print("\n=== ALL CONSOLE LOGS FROM SQUARE CLICK ===")
    for log in logs:
        print(log)
    
    print("\n=== JAVASCRIPT ERRORS ===")
    for err in errors:
        print(err)

if __name__ == "__main__":
    run_click_test()
