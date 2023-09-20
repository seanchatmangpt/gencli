import logging
from unittest.mock import MagicMock, patch

import pytest
from openai import ChatCompletion, Completion


# Test to demonstrate logging
def test_logging_example(caplog):
    with caplog.at_level(logging.INFO):
        logging.info("This is an info log")
        assert "This is an info log" in caplog.text


@pytest.fixture(scope="function")
def mock_openai_create(monkeypatch, request):
    side_effect_func = request.param if hasattr(request, "param") else None

    def mock_completion_create(*args, **kwargs):
        if side_effect_func:
            return side_effect_func("Completion")
        return {"choices": [{"text": "Mocked Completion"}]}

    def mock_chatcompletion_create(*args, **kwargs):
        if side_effect_func:
            return side_effect_func("ChatCompletion")
        return {"choices": [{"text": "Mocked ChatCompletion"}]}

    monkeypatch.setattr(Completion, "create", mock_completion_create)
    monkeypatch.setattr(ChatCompletion, "create", mock_chatcompletion_create)


# Parameterized test for mocking Completion.create and ChatCompletion.create
@pytest.mark.parametrize(
    "mock_openai_create,expected",
    [
        (
            lambda x: {
                "choices": [{"text": f"Mocked {x} with parameterized side effect"}]
            },
            "with parameterized side effect",
        ),
        (None, None),
    ],
    indirect=["mock_openai_create"],
)
def test_openai_mocking(mock_openai_create, expected):
    completion_result = Completion.create()
    chatcompletion_result = ChatCompletion.create()

    if expected:
        assert expected in completion_result["choices"][0]["text"]
        assert expected in chatcompletion_result["choices"][0]["text"]
    else:
        assert "Mocked Completion" == completion_result["choices"][0]["text"]
        assert "Mocked ChatCompletion" == chatcompletion_result["choices"][0]["text"]


# Test to demonstrate assertions
def test_assertions():
    assert (2 + 2) == 4
    assert isinstance([1, 2, 3], list)


# Test to demonstrate timeout
@pytest.mark.timeout(5)
def test_timeout():
    assert 1 == 1  # This test should finish well within 5 seconds


# Test to demonstrate expected exceptions
def test_expected_exception():
    with pytest.raises(ValueError):
        raise ValueError("This is a forced error")


# Test to demonstrate fixtures
@pytest.fixture(scope="function")
def simple_fixture():
    return "Hello, I am a fixture"


def test_with_fixture(simple_fixture):
    assert simple_fixture == "Hello, I am a fixture"


# Test to demonstrate mocking
def test_mocking():
    with patch("builtins.open", MagicMock()) as mock_open:
        with open("fake_file.txt", "r") as f:
            print(f)
        mock_open.assert_called_with("fake_file.txt", "r")


# Test to demonstrate function arguments
def test_function_args(simple_fixture):
    assert simple_fixture == "Hello, I am a fixture"
