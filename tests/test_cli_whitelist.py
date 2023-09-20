# from unittest import mock
#
# from fgn.completion.complete import (
#     choose,
#     is_correct_command,
#     whitelisted_command_selector,
# )
#
#
# # Mocking create function to return specific outputs for test cases.
# def mock_create(*args, **kwargs):
#     prompt = args[0]
#     if "Index of choice base-16 0x" in prompt:
#         return "1"
#     if "The correct command is $" in prompt:
#         return "docker"
#     return ""
#
#
# # Test for choose function
# def test_choose():
#     with mock.patch("fgn.completion.complete.create", side_effect=mock_create):
#         result = choose("Index of choice base-16 0x", ["choice1", "choice2"])
#     assert result == "choice2"
#
#
# # Test for whitelisted_command_selector function
# def test_whitelisted_command_selector():
#     with mock.patch("fgn.completion.complete.create", side_effect=mock_create):
#         result = whitelisted_command_selector("prompt", ["ls", "docker"])
#     assert result == "docker"
#
#
# # Test for is_correct_command function when the command is correct
# def test_is_correct_command_true():
#     with mock.patch("fgn.completion.complete.create", side_effect=mock_create):
#         result = is_correct_command("prompt", "docker")
#     assert result is True
#
#
# # Test for is_correct_command function when the command is not correct
# def test_is_correct_command_false():
#     with mock.patch("fgn.completion.complete.create", side_effect=mock_create):
#         result = is_correct_command("prompt", "ls")
#     assert result is False
#
#
# # Test for choose function when the response is not a valid hex code
# def test_choose_invalid_hex():
#     with mock.patch(
#         "fgn.completion.complete.create", return_value="ZZ"
#     ):  # Make sure to replace `fgn.completion.complete` with the name of
#         # the actual file containing your source code.
#         try:
#             choose("prompt", ["choice1", "choice2"])
#         except ValueError as e:
#             assert str(e) == "Response is not a valid hex code: ZZ"
#
#
# # Test for is_correct_command when the returned command is unexpected
# def test_is_correct_command_unexpected():
#     with mock.patch("fgn.completion.complete.create", return_value="unexpected"):
#         result = is_correct_command("prompt", "docker")
#         assert result is False
