import json
from typing import Dict

from gencli.utils import generate_cli_code, generate_cli_spec, openai_analysis


# Fake OpenAI API for testing
def fake_openai_analysis(transcript: str) -> Dict:
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


# Test OpenAI analysis function
def test_openai_analysis():
    transcript = "We need a CLI for creating tasks."
    result = openai_analysis(transcript)
    assert "commands" in result


# Test CLI spec generation
def test_generate_cli_spec():
    api_data = {
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
    cli_spec = generate_cli_spec(api_data)
    assert "cli_spec" in cli_spec


# Test CLI code generation
def test_generate_cli_code():
    cli_spec = {
        "cli_spec": {
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
    }
    cli_code = generate_cli_code(cli_spec)
    assert "cli_spec" in json.loads(cli_code)
