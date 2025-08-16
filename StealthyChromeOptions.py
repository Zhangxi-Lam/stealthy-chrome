from selenium.webdriver.chrome.options import ChromiumOptions


class StealthyChromeOptions(ChromiumOptions):
    def __init__(self, user_data_dir: str = None, language: str = None):
        super().__init__()
        # Basic window settings
        self.add_argument("--headless")
        self.add_argument("--window-size=1920,1080")
        
        # Disable automation indicators
        self.add_argument("--no-default-browser-check")
        self.add_argument("--no-first-run")
        self.add_argument("--no-sandbox")
        self.add_argument("--disable-infobars")
        self.add_argument("--disable-extensions")
        self.add_argument("--disable-blink-features=AutomationControlled")
        
        # Remove automation flags
        self.add_experimental_option("useAutomationExtension", False)
        self.add_experimental_option("excludeSwitches", ["enable-automation"])
        
        # Make browser look more human
        self.add_argument("--disable-dev-shm-usage")
        self.add_argument("--disable-gpu")
        self.add_argument("--remote-debugging-port=0")  # Disable remote debugging
        
        # User agent and language
        language = language or "en-US,en;q=0.9"
        self.add_argument(f"--lang={language}")
        self.add_argument("--accept-lang=en-US,en;q=0.9")
        
        # Additional stealth headers
        self.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2,  # Block notifications
            "profile.managed_default_content_settings.images": 1,  # Load images
        })
        
        if user_data_dir and user_data_dir.strip():
            self.add_argument(f"--user-data-dir={user_data_dir}")

        # Set debugger address
        # debug_host = "127.0.0.1"
        # debug_port = selenium.webdriver.common.service.utils.free_port()
        # self.debugger_address = f"{debug_host}:{debug_port}"
        # self.add_argument("--remote-debugging-host=%s" % debug_host)
        # self.add_argument("--remote-debugging-port=%s" % debug_port)



