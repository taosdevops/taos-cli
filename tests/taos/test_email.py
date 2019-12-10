from taos.email import send_message
from unittest import TestCase, mock

class TestEmail(TestCase):

    @mock.patch("taos.email.SendGridAPIClient")
    @mock.patch("taos.email.Mail")
    def test_send_message_sends_message(self, mock_mail, mock_sg_api):
        send_message("foo","bar","baz")
        mock_sg_api.return_value.send.assert_called()

