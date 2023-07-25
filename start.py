import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# import logging
import signal

import guide_config
from guide_main import GuideMain
import helper
from holon import config


if __name__ == '__main__':
    logger = helper.init_logging(log_dir=guide_config.log_dir, log_level=guide_config.log_level)
    logger.info(f'***** GuideMain start *****')

    def signal_handler(signal, frame):
        print("signal_handler")
    signal.signal(signal.SIGINT, signal_handler)

    cfg = config()
    cfg.mqtt_address = guide_config.mqtt_address
    cfg.mqtt_port = guide_config.mqtt_port
    cfg.mqtt_keepalive = guide_config.mqtt_keepalive
    cfg.mqtt_username = guide_config.mqtt_username
    cfg.mqtt_password = guide_config.mqtt_password
    os.environ["OPENAI_API_KEY"] = guide_config.openai_api_key

    a = GuideMain(cfg)
    a.start()
