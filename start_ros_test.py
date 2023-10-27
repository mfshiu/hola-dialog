from datetime import datetime as dt
import signal

from abdi_config import AbdiConfig
import app_config
import helper
from holon.HolonicAgent import HolonicAgent


logger = helper.get_logger()


class RosTest(HolonicAgent):
    def __init__(self, cfg):
        super().__init__(cfg)

        logger.debug(f"Init RosTest done.")


    def _on_connect(self):
        logger.debug(f"Connect to broker done.")
        super()._on_connect()


    def _on_topic(self, topic, data):
        super()._on_topic(topic, data)


    def _run_interval(self):
        logger.info(f"interval: {dt.now()}")



if __name__ == '__main__':

    logger.info(f'***** Start *****')

    def signal_handler(signal, frame):
        logger.warning("System was interrupted.")
    signal.signal(signal.SIGINT, signal_handler)

    RosTest(AbdiConfig(options={
        "broker_type": app_config.broker_type,

        "input_dir": app_config.input_dir,
        "output_dir": app_config.output_dir,
        "playht_user_id": app_config.playht_user_id,
        "playht_secret_key": app_config.playht_secret_key,
    })).start()
