import yaml


def lowercase(text):
    return text.lower()

def remove_stop_words(text):
    stop_words = {"a", "an", "the", "and", "or", "but"}  
    words = text.split()
    filtered = [word for word in words if word.lower() not in stop_words]
    return " ".join(filtered)

def uk_to_us(text):
    """Convert some UK terms to US terms (simple example)."""
   
    replacements = {
        "colour": "color",
        "centre": "center"
    }
    for uk, us in replacements.items():
        text = text.replace(uk, us)
    return text

def upper_case(text):
    """Convert text to uppercase."""
    return text.upper()

function_lookup = {
    "lowercase": lowercase,
    "remove_stop_words": remove_stop_words,
    "uk_to_us": uk_to_us,
    "upper_case": upper_case
}

def process_record(record, pipeline):

    for func_name in pipeline:
        func = function_lookup.get(func_name)
        if func:
            record = func(record)
        else:
            print(f"Warning: Function '{func_name}' not found in lookup!")
    return record

def main():
   
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    
   
    pipeline = config.get("pipeline", [])  
    input_record = "The colour of the centre is amazing and the style is unique."
    output_record = process_record(input_record, pipeline)
    
    
    print("starting test :")
    print(input_record)
    print("\n end test")
    print(output_record)

if __name__ == '__main__':
    main()
