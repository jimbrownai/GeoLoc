from .llm_client import ask_llm

def generate_travel_guide(place_name):
    prompt = f"""
    Provide a short but rich travel guide for {place_name}.
    Include:
    - Brief history/cultural importance
    - Best time to visit 
    - Must-see spots
    - Local food or experiences
    Keep it concise and engaging.
    """
    content = ask_llm(prompt)
    return {"place":place_name,"guide":content}
