import json


# Function to simulate OpenAI API
def fake_openai_analysis(transcript: str) -> dict:
    return {
        "commands": [
            {
                "name": "create_task",
                "options": [
                    {"name": "title", "type": "str"},
                    {"name": "description", "type": "str"},
                ],
            }
        ]
    }


# Fake requests.post function for testing
def fake_post(url: str, data: dict) -> dict:
    return {"status": 200, "data": fake_openai_analysis(data["transcript"])}


# Function to perform OpenAI API call
def openai_analysis(transcript: str) -> dict:
    # Simulating an API request to OpenAI
    response = fake_post("http://api.openai.com/analysis", {"transcript": transcript})
    if response["status"] == 200:
        return response["data"]
    else:
        raise Exception("API call failed")


# Function to generate CLI spec from OpenAI analysis
def generate_cli_spec(api_data: dict) -> dict:
    # Create a CLI spec based on the OpenAI analysis
    return {"cli_spec": api_data}


# Function to generate CLI code based on the CLI spec
def generate_cli_code(cli_spec: dict) -> str:
    # Generate code based on the CLI spec
    return json.dumps(cli_spec, indent=4)
