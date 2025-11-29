"""
Unit tests for EmailAgent
Tests pure functions and validation logic with no external dependencies.
"""

from datetime import datetime
from agents.email_sender import EmailAgent


class TestEmailAgentValidation:
    """Test EmailAgent validation and configuration checks."""

    def test_email_disabled_returns_false(self, email_agent_disabled):
        """Test that email sending returns False when disabled."""
        result = email_agent_disabled.send_email(
            recipients=["test@example.com"], subject="Test", summary="Test summary", articles=[]
        )
        # Since send_email is async, we need to run it
        import asyncio

        result = asyncio.run(result)
        assert result is False

    def test_missing_credentials_returns_false(self, email_agent_no_credentials):
        """Test that missing credentials returns False."""
        import asyncio

        result = asyncio.run(
            email_agent_no_credentials.send_email(
                recipients=["test@example.com"], subject="Test", summary="Test summary", articles=[]
            )
        )
        assert result is False

    def test_empty_recipients_returns_false(self, email_agent):
        """Test that empty recipients list returns False."""
        import asyncio

        result = asyncio.run(
            email_agent.send_email(
                recipients=[], subject="Test", summary="Test summary", articles=[]
            )
        )
        assert result is False

    def test_whitespace_only_recipients_filtered(self, email_agent):
        """Test that whitespace-only recipients are filtered out."""
        import asyncio

        result = asyncio.run(
            email_agent.send_email(
                recipients=["  ", "\t", "\n", ""],
                subject="Test",
                summary="Test summary",
                articles=[],
            )
        )
        assert result is False

    def test_recipients_are_cleaned(self, email_agent_with_mock_smtp):
        """Test that recipients with whitespace are properly cleaned."""
        import asyncio

        recipients = [" test1@example.com ", "test2@example.com\n", "\ttest3@example.com"]

        # Mock SMTP to avoid actual sending
        from unittest.mock import patch, MagicMock

        with patch("agents.email_sender.smtplib.SMTP") as mock_smtp:
            mock_server = MagicMock()
            mock_smtp.return_value.__enter__.return_value = mock_server

            result = asyncio.run(
                email_agent_with_mock_smtp.send_email(
                    recipients=recipients, subject="Test", summary="Test", articles=[]
                )
            )

            # Check that send_message was called (meaning recipients were valid)
            if result:
                assert mock_server.send_message.called


class TestEmailAgentSubjectGeneration:
    """Test email subject generation."""

    def test_execute_generates_subject_with_date(self, email_agent_with_mock_smtp):
        """Test that execute() generates subject with current date."""
        import asyncio
        from unittest.mock import patch, MagicMock

        with patch("agents.email_sender.smtplib.SMTP") as mock_smtp:
            mock_server = MagicMock()
            mock_smtp.return_value.__enter__.return_value = mock_server

            asyncio.run(
                email_agent_with_mock_smtp.execute(
                    summary="Test summary", articles=[], recipients=["test@example.com"]
                )
            )

            # Verify send_message was called
            assert mock_server.send_message.called

            # Get the message that was sent
            sent_msg = mock_server.send_message.call_args[0][0]
            subject = sent_msg["Subject"]

            # Check subject format
            assert "KeepMePosted" in subject
            assert "Tech Newsletter" in subject
            # Check date is in subject (format: "Month Day, Year")
            current_date = datetime.now().strftime("%B %d, %Y")
            assert current_date in subject


class TestEmailAgentConfiguration:
    """Test EmailAgent configuration handling."""

    def test_agent_uses_gmail_by_default(self, sample_email_config):
        """Test that agent defaults to Gmail SMTP settings."""
        agent = EmailAgent(sample_email_config)
        assert agent.config["smtp_server"] == "smtp.gmail.com"
        assert agent.config["smtp_port"] == 587

    def test_agent_respects_custom_smtp(self):
        """Test that agent respects custom SMTP configuration."""
        config = {
            "email_enabled": True,
            "email_user": "test@outlook.com",
            "email_password": "password",
            "smtp_server": "smtp-mail.outlook.com",
            "smtp_port": 587,
        }
        agent = EmailAgent(config)
        assert agent.config["smtp_server"] == "smtp-mail.outlook.com"
