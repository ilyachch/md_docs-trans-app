import logging
import random

from selenium.webdriver.chrome.options import Options

from md_translate.translators.randomizer.const import USER_AGENTS

logger = logging.getLogger(__name__)


class Randomizer:
    USER_AGENTS = USER_AGENTS

    def get_random_user_agent(self) -> str:
        return random.choice(self.USER_AGENTS)

    def get_random_sleep_time(self) -> float:
        return random.uniform(0.3, 1.5)

    def get_random_window_size(self) -> tuple[int, int]:
        return random.randint(800, 1200), random.randint(600, 800)

    def get_random_window_position(self) -> tuple[int, int]:
        return random.randint(0, 100), random.randint(0, 100)

    def make_options(self) -> Options:
        user_agent = self.get_random_user_agent()
        logger.info('Using user agent: %s', user_agent)
        options = Options()
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument(f'--window-size={",".join(map(str, self.get_random_window_size()))}')
        options.add_argument(f'--window-position={self.get_random_window_position()}')
        return options
