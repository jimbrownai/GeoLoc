# apps/common/utils.py
def format_airport_name(raw_name: str) -> str:
    return raw_name.strip()

def get_iata_from_dataset(airport_name: str):
    # TODO: search in local dataset
    return "DXB"
