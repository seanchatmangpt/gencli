from unittest.mock import AsyncMock, patch

import pytest
from munch import Munch


# Function that uses the OpenAI APIs
def use_openai_apis():
    from openai import ChatCompletion, Completion

    print(
        Completion.create(
            engine="text-davinci-002", prompt="Hello, world!", max_tokens=5
        )
    )
    print(
        ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Who won the world series in 2020?"},
            ],
        )
    )


# First test to assert that all of the patching works
def test_patching_works():
    with patch("openai.Completion.create") as mock_completion_create, patch(
        "openai.ChatCompletion.create"
    ) as mock_chat_completion_create:
        # Set Mock responses
        mock_completion_create.return_value = Munch(
            {"choices": [Munch({"text": "Mocked Completion"})]}
        )
        mock_chat_completion_create.return_value = Munch(
            {"choices": [Munch({"text": "Mocked ChatCompletion"})]}
        )

        # Call the function that uses the OpenAI APIs
        use_openai_apis()

        # Verify that the mocks were called
        mock_completion_create.assert_called_once_with(
            engine="text-davinci-002", prompt="Hello, world!", max_tokens=5
        )
        mock_chat_completion_create.assert_called_once_with(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Who won the world series in 2020?"},
            ],
        )


# Second test to demonstrate setting side effects conditionally per test
def test_side_effect_patching():
    def mock_completion_side_effect(*args, **kwargs):
        if kwargs["prompt"] == "Hello, world!":
            return Munch(
                {"choices": [Munch({"text": "Mocked Completion for Hello, world!"})]}
            )
        else:
            return Munch({"choices": [Munch({"text": "Different Mocked Completion"})]})

    def mock_chat_completion_side_effect(*args, **kwargs):
        if kwargs["messages"][0]["content"] == "You are a helpful assistant.":
            return Munch(
                {
                    "choices": [
                        Munch({"text": "Mocked ChatCompletion for helpful assistant"})
                    ]
                }
            )
        else:
            return Munch(
                {"choices": [Munch({"text": "Different Mocked ChatCompletion"})]}
            )

    with patch("openai.Completion.create") as mock_completion_create, patch(
        "openai.ChatCompletion.create"
    ) as mock_chat_completion_create:
        mock_completion_create.side_effect = mock_completion_side_effect
        mock_chat_completion_create.side_effect = mock_chat_completion_side_effect

        # Call the function to test
        from openai import ChatCompletion, Completion

        response1 = Completion.create(
            engine="text-davinci-002", prompt="Hello, world!", max_tokens=5
        )
        response2 = ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Who won the world series in 2020?"},
            ],
        )

        # Assertions
        assert response1.choices[0].text == "Mocked Completion for Hello, world!"
        assert (
            response2.choices[0].text == "Mocked ChatCompletion for helpful assistant"
        )

        # Let's verify with different arguments
        response3 = Completion.create(
            engine="text-davinci-002", prompt="Different prompt", max_tokens=5
        )
        response4 = ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are not so helpful."},
                {"role": "user", "content": "Who won the world series in 2020?"},
            ],
        )

        # Assertions
        assert response3.choices[0].text == "Different Mocked Completion"
        assert response4.choices[0].text == "Different Mocked ChatCompletion"


# Mock function for Completion.acreate
async def mock_acreate_completion(*args, **kwargs):
    return {"choices": [{"text": "Mocked Async Completion"}]}


# Mock function for ChatCompletion.acreate
async def mock_acreate_chat_completion(*args, **kwargs):
    return {"choices": [{"text": "Mocked Async Chat Completion"}]}


# The test for patching the acreate of both Completion and ChatCompletion classes
@pytest.mark.asyncio
async def test_patch_acreate_methods():
    # Assuming Completion and ChatCompletion classes are
    # imported correctly in your test file
    from openai import ChatCompletion, Completion

    with patch(
        "openai.Completion.acreate",
        new_callable=AsyncMock,
        side_effect=mock_acreate_completion,
    ), patch(
        "openai.ChatCompletion.acreate",
        new_callable=AsyncMock,
        side_effect=mock_acreate_chat_completion,
    ):
        # Async call to the acreate method of Completion
        completion_response = await Completion.acreate(
            prompt="test prompt", engine="text-davinci-002"
        )
        assert completion_response["choices"][0]["text"] == "Mocked Async Completion"

        # Async call to the acreate method of ChatCompletion
        chat_completion_response = await ChatCompletion.acreate(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Who won the world series in 2020?"},
            ]
        )
        assert (
            chat_completion_response["choices"][0]["text"]
            == "Mocked Async Chat Completion"
        )


# Sample Mock functions
async def mock_acreate_completion_variant1(*args, **kwargs):
    return {"choices": [{"text": "Mocked Async Completion Variant 1"}]}


async def mock_acreate_completion_variant2(*args, **kwargs):
    return {"choices": [{"text": "Mocked Async Completion Variant 2"}]}


async def mock_acreate_chat_completion_variant1(*args, **kwargs):
    return {"choices": [{"text": "Mocked Async Chat Completion Variant 1"}]}


async def mock_acreate_chat_completion_variant2(*args, **kwargs):
    return {"choices": [{"text": "Mocked Async Chat Completion Variant 2"}]}


# Test function that accepts the mock function as a parameter
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "mock_completion, mock_chat, expected_completion_text, expected_chat_text",
    [
        (
            mock_acreate_completion_variant1,
            mock_acreate_chat_completion_variant1,
            "Mocked Async Completion Variant 1",
            "Mocked Async Chat Completion Variant 1",
        ),
        (
            mock_acreate_completion_variant2,
            mock_acreate_chat_completion_variant2,
            "Mocked Async Completion Variant 2",
            "Mocked Async Chat Completion Variant 2",
        ),
    ],
)
async def test_dynamic_patch_acreate_methods(
    mock_completion, mock_chat, expected_completion_text, expected_chat_text
):
    from openai import ChatCompletion, Completion

    with patch(
        "openai.Completion.acreate", new_callable=AsyncMock, side_effect=mock_completion
    ) as mocked_acreate_completion, patch(
        "openai.ChatCompletion.acreate", new_callable=AsyncMock, side_effect=mock_chat
    ) as mocked_acreate_chat_completion:
        # Assuming Completion and ChatCompletion classes are imported
        # correctly in your test file
        print(mocked_acreate_completion)
        print(mocked_acreate_chat_completion)

        # Async call to the acreate method of Completion
        completion_response = await Completion.acreate(
            prompt="test prompt", engine="text-davinci-002"
        )
        assert completion_response["choices"][0]["text"] == expected_completion_text

        # Async call to the acreate method of ChatCompletion
        chat_completion_response = await ChatCompletion.acreate(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Who won the world series in 2020?"},
            ]
        )
        assert chat_completion_response["choices"][0]["text"] == expected_chat_text
