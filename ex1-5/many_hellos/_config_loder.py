import os
from pathlib import Path
import yaml
import logging


logger = logging.getLogger(__name__)

def load_config():
    candidate_paths = []

    candidate_paths.append(Path.cwd() / "_config.yaml")
    logger.debug("_config.yml file found in the current folder ")

    main_file_path  =  Path(__file__).resolve().parent.parent.joinpath("_config.yaml")


    if main_file_path.exists() :
        candidate_paths.append(main_file_path)



    env_paths = os.environ.get("CONFIG_PATH") or os.environ.get("ATK_CONFIG_PATH")
    logger.debug("Environment config paths: %s, main_file_path: %s", env_paths, main_file_path)

    if env_paths:
        for p in env_paths.split(":"):
            candidate_paths.append(Path(p) / "_config.yaml")
    
  
    default_config = Path(__file__).parent / "_default_config.yaml"
    candidate_paths.append(default_config)
    
    for path in candidate_paths:
        if path.exists():
            with open(path, "r") as file:
                return yaml.safe_load(file)
    
    logger.warning("No configuration file found, using default config")
    return {"num_times": 1}


if __name__ == "__main__" :
    load_config()
