import logging
from lxml import html
import time
import selenium.webdriver.chrome.webdriver
import selenium.webdriver.chrome.service
from StealthyChromeOptions import StealthyChromeOptions
from weakref import finalize

# Configure logging to show on console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
)
logger = logging.getLogger("stealth_chrome")


class StealthyChrome(selenium.webdriver.chrome.webdriver.WebDriver):
    def __init__(self, options: StealthyChromeOptions = None):
        finalize(self, self._ensure_close, self)

        if not options:
            options = StealthyChromeOptions()

        # Use Service to let Selenium automatically download correct ChromeDriver
        service = selenium.webdriver.chrome.service.Service()
        super().__init__(service=service, options=options)
        
        # Execute script to remove webdriver traces
        self._make_stealthy()

    @classmethod
    def _ensure_close(cls, self):
        # Needs to be a classmethod so finalize can find the reference
        logger.info("Stealth chrome close")

    def _make_stealthy(self):
        """Execute JavaScript to make the browser more stealthy"""
        stealth_js = """
        // Remove webdriver property
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        
        // Mock chrome runtime
        window.chrome = {
            runtime: {
                onConnect: undefined,
                onMessage: undefined
            }
        };
        
        // Mock plugins
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5]
        });
        
        // Mock languages
        Object.defineProperty(navigator, 'languages', {
            get: () => ['en-US', 'en']
        });
        
        // Mock permissions
        const originalQuery = window.navigator.permissions.query;
        window.navigator.permissions.query = (parameters) => (
            parameters.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) :
                originalQuery(parameters)
        );
        """
        self.execute_script(stealth_js)


def my_chrome():
    # user_data_dir = "/Users/zhangxilin/Library/Application Support/Google/Chrome"
    user_data_dir = ""
    stealth_chrome_options = StealthyChromeOptions(user_data_dir=user_data_dir)
    stealth_chrome = StealthyChrome(stealth_chrome_options)
    logging.info("Stealthy chrome start getting url")
    stealth_chrome.get("https://nowsecure.nl")

    logging.info("Stealthy chrome saving page source")
    page_source = stealth_chrome.page_source
    extract_page_source(page_source)
    with open("result/page_source.html", "w") as f:
        f.write(page_source)

    logging.info("Stealthy chrome start saving screenshot")
    stealth_chrome.save_screenshot("result/screenshot.png")

    logging.info("Stealthy chrome screenshot saved")
    stealth_chrome.quit()

def vanila_chrome():
    service = selenium.webdriver.chrome.service.Service()
    driver = selenium.webdriver.chrome.webdriver.WebDriver(service=service)
    logging.info("Vanila chrome start getting url")
    driver.get("https://nowsecure.nl")
    logging.info("Vanila chrome start saving screenshot")
    driver.save_screenshot("screenshot.png")
    logging.info("Vanila chrome screenshot saved")

def extract_page_source(page_source):
    tree = html.fromstring(page_source)
    item = {}
    title = tree.xpath("//*[@id='product-page']//h-product-info-header//h1//span/text()")
    item["title"] = title[0].strip()

    price = tree.xpath("//h-price/span/text()")
    item["price"] = price[0].strip()

    color_variants = tree.xpath("//*[@id='expansion-panel-title-color-variants']/div/span[3]/div/span/div/text()")
    item["color_variants"] = color_variants[0].strip()

    print(item)

def main():
    # vanila_chrome()
    # my_chrome()
    page_source = open("result/page_source.html", "r").read()
    extract_page_source(page_source)



if __name__ == "__main__":
    main()
