import argparse
import os
import time
import random

from selenium.webdriver.common.by import By

from logger.logger import logger
from conf.conf import target_url, static_dir
from driver import create_driver_proxy, create_driver
from proxy import get_proxy

# from selenium.webdriver.common.keys import Keys


def delay():
    delay = random.randint(3, 10)
    logger.info(f"delay: {delay} second(s)")
    time.sleep(delay)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "data", type=str, help="输入要搜索的内容", default="Bp9ksh7EyrNX61GYfqXLB7wFhwg3BNJztgqEtKBwQBaA"
    )
    args = parser.parse_args()
    logger.info(f"search data: {args.data}")

    ip_address, port, username, pwd = get_proxy()
    driver = create_driver_proxy(
        executable_path=os.path.join(static_dir, "chromedriver-mac-arm64/chromedriver"),
        proxy_username=username,
        proxy_password=pwd,
        proxy_ip=ip_address,
        proxy_port=port,
    )
    # driver = create_driver(
    #     executable_path=os.path.join(static_dir, "chromedriver-mac-arm64/chromedriver"),
    # )
    driver.get(target_url)
    driver.implicitly_wait(60)
    logger.info(f"页面标题: {driver.title}")
    driver.find_element(
        By.XPATH, "//input[@placeholder='Type token symbol, address to find your launchpad']"
    ).send_keys(args.data)
    time.sleep(5)
    view_btn = driver.find_element(By.XPATH, "//button[span[text()='View']]")
    delay()
    view_btn.click()

    all_handles = driver.window_handles

    # 切换到新标签页
    new_handle = all_handles[-1]
    driver.switch_to.window(new_handle)

    # driver.get("https://www.pinksale.finance")
    # driver.get("https://www.pinksale.finance/solana/launchpad/Bp9ksh7EyrNX61GYfqXLB7wFhwg3BNJztgqEtKBwQBaA")
    driver.implicitly_wait(60)
    for a in driver.find_elements(
        By.XPATH, "//*[@id='__next']/div/div[3]/main/div/div/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[3]/a"
    ):
        # logger.info(a.get_attribute("outerHTML"))
        href = a.get_attribute("href")
        logger.info(f"href: {href}")
        a.click()
        delay()
    time.sleep(60)
