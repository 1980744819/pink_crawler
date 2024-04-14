import time
import zipfile

from selenium import webdriver

# from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import undetected_chromedriver as uc

# import undetected_chromedriver.v2 as uc


from logger.logger import logger


def proxies(username, password, endpoint, port):
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Proxies",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
              singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
              },
              bypassList: ["localhost"]
            }
          };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (
        endpoint,
        port,
        username,
        password,
    )

    extension = "proxies_extension.zip"

    with zipfile.ZipFile(extension, "w") as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    return extension


def get_chromedriver(executable_path, proxy_username, proxy_password, proxy_ip, proxy_port):
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (
        proxy_ip,
        proxy_port,
        proxy_username,
        proxy_password,
    )
    chrome_options = webdriver.ChromeOptions()
    pluginfile = "proxy_auth_plugin.zip"
    with zipfile.ZipFile(pluginfile, "w") as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)
    chrome_options.add_extension(pluginfile)
    webdriver_service = Service(executable_path=executable_path)
    driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
    return driver


def create_driver(executable_path):
    chrome_options = uc.ChromeOptions()
    chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    # chrome_options.add_argument("--disable-extensions")
    # chrome_options.add_argument("--disable-gpu")
    # # options.add_argument("--no-sandbox") # linux only
    # chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # chrome_options.add_experimental_option("useAutomationExtension", False)
    # chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    # 如果你的 WebDriver 不在系统 PATH 中，需要指定 WebDriver 的路径
    webdriver_service = Service(executable_path=executable_path)

    # 创建 WebDriver 实例
    driver = uc.Chrome(service=webdriver_service, options=chrome_options)
    with open("stealth.min.js") as f:
        js = f.read()
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": js})
    # driver.execute_cdp_cmd("Network.enable", {})
    # driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "browserClientA"}})
    # driver.execute_cdp_cmd(
    #     "Page.addScriptToEvaluateOnNewDocument",
    #     {
    #         "source": """
    #         Object.defineProperty(navigator, 'webdriver', {
    #             get: () => undefined
    #         })
    #     """
    #     },
    # )

    return driver


def create_driver_proxy(executable_path, proxy_username, proxy_password, proxy_ip, proxy_port):
# def create_driver_proxy(proxy_username, proxy_password, proxy_ip, proxy_port):
    # 创建 Chrome WebDriver 实例
    chrome_options = uc.ChromeOptions()
    # chrome_options.add_argument('--headless')  # 无头模式
    # chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速
    # chrome_options.add_argument('--no-sandbox')
    chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    proxies_extension = proxies(proxy_username, proxy_password, proxy_ip, proxy_port)
    chrome_options.add_extension(proxies_extension)

    # proxy_address = f"{proxy_username}:{proxy_password}@{proxy_ip}:{proxy_port}"
    # 设置代理
    # chrome_options.add_argument(f"--proxy-server={proxy_address}")

    # 如果你的 WebDriver 不在系统 PATH 中，需要指定 WebDriver 的路径
    webdriver_service = Service(executable_path=executable_path)

    # 创建 WebDriver 实例
    driver = uc.Chrome(service=webdriver_service, options=chrome_options)
    # driver = uc.Chrome(options=chrome_options)
    # with open("stealth.min.js") as f:
    #     js = f.read()
    # driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": js})

    return driver


if __name__ == "__main__":
    driver = create_driver_proxy(
        executable_path="static/chromedriver-mac-arm64/chromedriver",
        proxy_username="15302334-res-country-US-session-114",
        proxy_password="1knxihowrq",
        proxy_ip="175.110.113.33",
        proxy_port="12993",
    )
    # driver = create_driver(
    #     executable_path="static/chromedriver-mac-arm64/chromedriver",
    # )
    # driver = get_chromedriver(
    #     executable_path="static/chromedriver-mac-arm64/chromedriver",
    #     proxy_username="15302334-res-country-US-session-114",
    #     proxy_password="1knxihowrq",
    #     proxy_ip="175.110.113.33",
    #     proxy_port="12993",
    # )
    # driver.get("https://www.pinksale.finance")
    driver.get("https://bot.sannysoft.com/")
    driver.implicitly_wait(60)
    logger.info(f"页面标题: {driver.title}")
    # Bp9ksh7EyrNX61GYfqXLB7wFhwg3BNJztgqEtKBwQBaA
    # 0xe389E22c6CF385C4546696d76FCd4E658d7Db28D
    time.sleep(60)
    driver.quit()
