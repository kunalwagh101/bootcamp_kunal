from pathlib import Path
import re
import requests


def find_file(inputfile):
    path  = Path.cwd()/inputfile
    if path.exists() :
        return path
    path = Path.cwd().parent/inputfile
    if path.exists() :
        return path
    return None



def upper_case(input_file: str, outfile: str = None):
    exts = (".doc", ".txt", ".word")
  
    if any(input_file.endswith(ext) for ext in exts):
        outfile = outfile or f"{input_file}.processed"
        input_file = find_file(input_file)
        with open(input_file, "r", encoding="utf-8") as inf, \
             open(outfile, "w", encoding="utf-8") as outf:
            outf.write(inf.read().upper())
    else:
        
        outfile = outfile or "outfile.processed"
        with open(outfile, "w", encoding="utf-8") as f:
            f.write(input_file.upper())

STOP_WORDS = {"a", "an", "the", "and", "or"}

def remove_stop_words(text: str) -> str:
    text = text.lower()
    words = text.split()
    filtered_words = [word for word in words if word not in STOP_WORDS]
    return " ".join(filtered_words)

def capitalize(text: str) -> str:
    return text.title()

def fetch_geo_ip(ip_number: str) -> str:
    try:
        url = f"https://ipinfo.io/{ip_number}/geo"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        city = data.get("city", "Unknown")
        region = data.get("region", "Unknown")
        country = data.get("country", "Unknown")
        return f"{city}, {region}, {country}"
    except requests.RequestException:
        return "Error fetching geo data"

def lower_case(text: str) -> str:
    return text.lower()

def uk_to_us(text: str) -> str:
    return re.sub(r"(\w*)sation\b", r"\1zation", text)


if __name__ == "__main__" :
    upper_case("input.txt")


