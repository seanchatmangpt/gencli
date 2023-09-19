import json
from unittest.mock import MagicMock, patch

import openai
import pytest
from munch import Munch


# Function to communicate with OpenAI API for transcript analysis
def analyze_transcript_with_openai(transcript: str) -> dict:
    model_engine = "text-davinci-002"
    response = openai.Completion.create(
        engine=model_engine, prompt=transcript, max_tokens=100
    )
    return response.choices[0].text


# Test function to verify that the real API would be called
def test_real_openai_api_call():
    openai.Completion.create = MagicMock()
    analyze_transcript_with_openai("test transcript")
    openai.Completion.create.assert_called_once()


# Mock for OpenAI API
def mock_analyze_transcript_with_openai(*args, **kwargs) -> dict:
    return Munch({"choices": [Munch({"text": "Mocked transcript analysis."})]})


# Test function to ensure that the mock replaces the real API call and is verified
@pytest.mark.parametrize(
    "transcript, expected", [("test transcript", "Mocked transcript analysis.")]
)
def test_mock_openai_api_call(transcript, expected):
    with patch(
        "openai.Completion.create", side_effect=mock_analyze_transcript_with_openai
    ):
        result = analyze_transcript_with_openai(transcript)
        assert result == expected


# Function to handle different types of commands and options
def handle_commands_and_options(response: str) -> dict:
    try:
        analyzed_commands = json.loads(response)
        return {
            "create_task": handle_create_task_command(
                analyzed_commands.get("create_task", {})
            ),
            "delete_task": handle_delete_task_command(
                analyzed_commands.get("delete_task", {})
            ),
            # Add more command handlers here
        }
    except json.JSONDecodeError as e:
        raise ValueError("Invalid JSON received from OpenAI") from e


def handle_create_task_command(options: dict) -> dict:
    title = options.get("title")
    description = options.get("description")
    if title and description:
        return {
            "action": "create_task",
            "params": {"title": title, "description": description},
        }
    else:
        return {"action": "create_task", "params": {}}


def handle_delete_task_command(options: dict) -> dict:
    task_id = options.get("task_id")
    if task_id:
        return {"action": "delete_task", "params": {"task_id": task_id}}
    else:
        return {"action": "delete_task", "params": {}}


# Function to validate and handle errors for OpenAI responses
def validate_openai_response(response: str) -> bool:
    if not response:
        raise ValueError("Empty response from OpenAI")
    try:
        analyzed_commands = json.loads(response)
        if (
            "create_task" not in analyzed_commands
            or "delete_task" not in analyzed_commands
        ):
            raise ValueError("Invalid commands in OpenAI response")
        return True
    except json.JSONDecodeError as e:
        raise ValueError("Invalid JSON received from OpenAI") from e


# Test for new functionalities
def test_handle_commands_and_options_and_validation():
    valid_response = json.dumps(
        {
            "create_task": {"title": "Task 1", "description": "Description 1"},
            "delete_task": {"task_id": 1},
        }
    )
    invalid_response = "invalid_json"

    # Testing command and option handling
    handled_commands = handle_commands_and_options(valid_response)
    assert handled_commands["create_task"]["params"]["title"] == "Task 1"
    assert handled_commands["delete_task"]["params"]["task_id"] == 1

    # Testing OpenAI response validation
    assert validate_openai_response(valid_response) is True

    with pytest.raises(ValueError, match="Invalid JSON received from OpenAI"):
        validate_openai_response(invalid_response)
