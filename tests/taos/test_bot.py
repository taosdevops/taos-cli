from taos import bot
from unittest import TestCase

class TestTaosBotParsing(TestCase):
    def test_taosbot_parses_command_string_with_param(self):
        command_string = "taos bot test --foo bar --baz quz"
        # command, parameter = bot._parse_command_string()
        # _parse_command_string
        self.assertEqual(
            bot._parse_command_string(command_string),
            ("taos bot test", {"foo":"bar","baz":"quz"})
        )

    def test_taosbot_parses_command_string_without_param(self):
        command_string = "taos bot test"
        self.assertEqual(
            bot._parse_command_string(command_string),
            ("taos bot test", {})
        )

class TestTaosBotSlackActions(TestCase):
    pass
