import random

from conf.conf import proxy_file_path
from logger.logger import logger


# 109.236.82.42:14407:15302321-res-country-US-session-100:ke326i6og
def decode_proxy(line: str):
    ip_address, port, username, pwd = line.split(":")
    logger.info(f"address: {ip_address}, port: {port},username: {username},pwd: {pwd}")
    return ip_address, port, username, pwd


def get_proxy():
    with open(proxy_file_path) as f:
        lines = f.readlines()
    line = random.choice(lines)
    logger.info(line)
    return decode_proxy(line)


if __name__ == "__main__":
    get_proxy()
