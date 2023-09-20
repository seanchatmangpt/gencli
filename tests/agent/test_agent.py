# from unittest.mock import AsyncMock, patch
#
# import pytest
#
# from gencli.agent import (  # Replace with the actual import of your Agent class
#     PROMPTS,
#     STATES,
#     Agent,
# )
#
#
# # Mock achat function
# async def mock_achat(prompt):
#     return f"Mocked result for {prompt}"
#
#
# @pytest.mark.asyncio
# async def test_agent_methods():
#     sys_msg = "System message"
#     agent = Agent(sys_msg=sys_msg)
#
#     # Use AsyncMock from unittest.mock to mock the achat function
#     with patch("gencli.agent.achat", new_callable=AsyncMock, side_effect=mock_achat):
#         # Test each agent method and check the task log
#         for state, task in zip(STATES.keys(), agent.tasks):
#             prompt = PROMPTS[state]
#
#             expected_result = f"Mocked result for {prompt}"
#             action, result = await task(prompt=prompt)
#
#             assert action == state, f"For state {state}, action was {action}"
#             assert result == expected_result, f"For state {state}, result was {result}"
#
#             log_entry = agent.chat_log[-1]
#             assert (
#                 log_entry["state"] == STATES[state]
#             ), f"For state {state}, logged state was {log_entry['state']}"
#             assert (
#                 log_entry["prompt"] == prompt
#             ), f"For state {state}, logged prompt was {log_entry['prompt']}"
#             assert (
#                 log_entry["result"] == expected_result
#             ), f"For state {state}, logged result was {log_entry['result']}"
