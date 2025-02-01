"""
Process a JSON file to count nobel laureates by country of origin and save the result.

JSON file is in the format where laureates is a list of dictionaries with keys "id" and "bornCountryCode".

{
    "people": [
        {
            "craft": "ISS",
            "name": "Oleg Kononenko"
        },
        {
            "craft": "ISS",
            "name": "Nikolai Chub"
        }
    ],
    "number": 2,
    "message": "success"
}

"""

#####################################
# Import Modules
#####################################

# Import from Python Standard Library
import pathlib
import json

# Import from local project modules
from utils_logger import logger

#####################################
# Declare Global Variables
#####################################

fetched_folder_name: str = "actual_data"
processed_folder_name: str = "actual_processed"

#####################################
# Define Functions
#####################################

def count_laureates_by_country(file_path: pathlib.Path) -> dict:
    """Count the number of laureates from each country from a JSON file."""
    try:
        with file_path.open('r') as file:
            # Use the json module load() function 
            # to read data file into a Python dictionary
            laureates_dictionary = json.load(file)  
            # initialize an empty dictionary to store the counts
            country_counts_dictionary = {}
            # laureates is a list of dictionaries in the JSON file
            laureates_list: list = laureates_dictionary.get("laureates", [])
            for country_dictionary in laureates_list:  
                country = country_dictionary.get("bornCountryCode", "Unknown")
                country_counts_dictionary[country] = country_counts_dictionary.get(country, 0) + 1
            return country_counts_dictionary
    except Exception as e:
        logger.error(f"Error reading or processing JSON file: {e}")
        return {}

def process_json_file():
    """Read a JSON file, count laureates by country, and save the result."""
    input_file: pathlib.Path = pathlib.Path(fetched_folder_name, "laureates.json")
    output_file: pathlib.Path = pathlib.Path(processed_folder_name, "json_laureates_by_country.txt")
    
    country_counts = count_laureates_by_country(input_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with output_file.open('w') as file:
        file.write("Laureates by country:\n")
        for country, count in country_counts.items():
            file.write(f"{country}: {count}\n")
    
    logger.info(f"Processed JSON file: {input_file}, Results saved to: {output_file}")

#####################################
# Main Execution
#####################################

if __name__ == "__main__":
    logger.info("Starting JSON processing...")
    process_json_file()
    logger.info("JSON processing complete.")