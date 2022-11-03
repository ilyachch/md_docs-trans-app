import random
from typing import Tuple
from selenium.webdriver.chrome.options import Options

from .const import PROXY, USER_AGENTS


import logging
logger = logging.getLogger(__name__)

class Randomizer:
    USER_AGENTS = USER_AGENTS
    PROXIES = PROXY

    def get_random_user_agent(self) -> str:
        return random.choice(self.USER_AGENTS)

    def get_random_sleep_time(self) -> float:
        return random.uniform(0.3, 1.5)

    def get_random_window_size(self) -> Tuple[int, int]:
        return random.randint(800, 1200), random.randint(600, 800)

    def get_random_window_position(self) -> Tuple[int, int]:
        return random.randint(0, 100), random.randint(0, 100)

    # def get_random_device_metrics(self) -> Tuple[int, int, float]:
    #     return random.randint(300, 500), random.randint(300, 500), random.uniform(1, 2)

    def get_random_proxy(self) -> str:
        return random.choice(self.PROXIES)

    def make_options(self) -> Options:
        user_agent = self.get_random_user_agent()
        proxy = self.get_random_proxy()
        logger.info(f'Using user agent: %s', user_agent)
        logger.info(f'Using proxy: %s', proxy)
        options = Options()
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument(f'--window-size={",".join(map(str, self.get_random_window_size()))}')
        options.add_argument(f'--window-position={self.get_random_window_position()}')
        options.add_argument(f'--proxy-server={proxy}')
        return options

