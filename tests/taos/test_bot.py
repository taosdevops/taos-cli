from unittest import TestCase, mock
import pytest

## Need to patch slack authentication for testing;
with mock.patch("slack.WebClient") as mock_slack:
    mock_slack.auth_test.return_value = {"taosdevopsutils.slack": "BOT"}
    from taos import bot

class TestTaosBotSlackActions:

    @pytest.mark.vcr()
    def test_taosbot_responds_about_taos(self, mocker):
        about_patch = mocker.patch.object(bot.about,"get_about")
        about_text = "This is about me."
        about_patch.return_value = [about_text]

        response = bot._parse_about("about")

        expected = f"Thanks for asking about me.\n{about_text}"
        assert response == expected

    @pytest.mark.vcr()
    def test_taosbot_responds_about_taos_devops(self, mocker):
        about_patch = mocker.patch.object(bot.about,"get_service")
        about_text = "This is about my service."
        service= "devops-now"
        about_patch.return_value = [about_text]

        response = bot._parse_about("about",service)
        print(response)

        assert response == [about_text]
        about_patch.assert_called_with(service)

    @pytest.mark.vcr()
    def test_taosbot_responds_bio(self, mocker):
        response = bot._parse_bio("bio")

        bio_text = "Whos bio would you like to see?"
        assert response == bio_text


    @pytest.mark.vcr()
    def test_taosbot_responds_bio_if_not_found(self, mocker):
        bio= "devops-now"

        response = bot._parse_bio("bio",bio)
        print(response)

        bio_text ="\n".join([
                "Sorry we couldnt find the users that you posted.",
                "These are the bios that I could locate.",
                *[f"- {bio_user}" for bio_user in bot.bio_users],
            ])

        assert response == bio_text


    def test_taosbot_responds_bio_for_user(self, mocker):
        bio_patch = mocker.patch.object(bot.bio,"get_user")
        bio= "rmeyer-taos"
        bio_text = f"This is the user bio for {bio}"
        bio_patch.return_value = bio_text

        response = bot._parse_bio("bio",bio)
        print(response)

        assert response == [bio_text]
        bio_patch.assert_called_with(bio)
