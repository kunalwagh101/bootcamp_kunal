from  many_hellos._config_loder import load_config

import logging
logger = logging.getLogger(__name__)

def say_hello(name: str) :
    logger.debug("say_hello called with name: %s", name)
    config = load_config()
    logger.debug("Config loaded: %s", config)
    num_times = config.get("num_times", 1)
    logger.debug("Returning result: %s", num_times)

    return "\n".join([f" Hello, {name}!" for _ in range(num_times+1)])


# if __name__ == "__main__" :
#     print("say_hello = " , say_hello("kunal"))