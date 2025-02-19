# Dynamic Text Processing Pipeline

This project demonstrates a dynamic text processing pipeline using a YAML configuration file to determine the sequence of functions to apply on each record.

## Features

- **YAML Configuration:** Easily customize your processing steps by editing the `config.yaml` file.
- **Function Lookup:** Dynamically map function names (specified in YAML) to actual Python functions without using `if`-`else` statements.

## example of yaml file 

```

pipeline:
  - lowercase
  - remove_stop_words
  - uk_to_us
  - upper_case


```
***customize as you want***


## How to Use

1. **Install Dependencies:**
   ```bash
   pip install pyyaml

2. **How to run the code**

***cd into the dynamic***

```
python main.py
1```