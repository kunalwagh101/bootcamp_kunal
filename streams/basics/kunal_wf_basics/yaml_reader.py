
import yaml



def read_config(config_file: str) -> dict:

    with open(config_file, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config

if __name__ == "__main__" :
    read_config("")