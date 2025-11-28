"""
Component tests for EmailAgent
Tests with mocked SMTP server and email template.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock, call
import smtplib
from agents.email_sender import EmailAgent


@pytest.mark.unit
class TestEmailAgentWithMockedSMTP:
    """Test EmailAgent with mocked SMTP server."""
    
    @pytest.mark.asyncio
    async def test_send_email_success(self, email_agent, sample_articles):
        """Test successful email sending with mocked SMTP."""
        with patch('agents.email_sender.smtplib.SMTP') as mock_smtp:
            mock_server = MagicMock()
            mock_smtp.return_value.__enter__.return_value = mock_server
            
            result = await email_agent.send_email(
                recipients=["test@example.com"],
                subject="Test Newsletter",
                summary="Test summary content",
                articles=sample_articles
            )
            
            assert result is True
            mock_smtp.assert_called_once_with("smtp.gmail.com", 587)
            mock_server.starttls.assert_called_once()
            mock_server.login.assert_called_once_with("test@gmail.com", "test_password")
            mock_server.send_message.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_send_email_multiple_recipients(self, email_agent, sample_articles):
        """Test sending email to multiple recipients."""
        with patch('agents.email_sender.smtplib.SMTP') as mock_smtp:
            mock_server = MagicMock()
            mock_smtp.return_value.__enter__.return_value = mock_server
            
            recipients = ["user1@example.com", "user2@example.com", "user3@example.com"]
            result = await email_agent.send_email(
                recipients=recipients,
                subject="Test",
                summary="Test",
                articles=sample_articles
            )
            
            assert result is True
            # Verify the message was sent
            mock_server.send_message.assert_called_once()
            
            # Check that all recipients are in the 'To' field
            sent_msg = mock_server.send_message.call_args[0][0]
            assert sent_msg['To'] == "user1@example.com, user2@example.com, user3@example.com"
    
    @pytest.mark.asyncio
    async def test_send_email_authentication_error(self, email_agent, sample_articles):
        """Test handling of SMTP authentication errors."""
        with patch('agents.email_sender.smtplib.SMTP') as mock_smtp:
            mock_server = MagicMock()
            mock_server.login.side_effect = smtplib.SMTPAuthenticationError(535, b'Authentication failed')
            mock_smtp.return_value.__enter__.return_value = mock_server
            
            result = await email_agent.send_email(
                recipients=["test@example.com"],
                subject="Test",
                summary="Test",
                articles=sample_articles
            )
            
            assert result is False
    
    @pytest.mark.asyncio
    async def test_send_email_smtp_exception(self, email_agent, sample_articles):
        """Test handling of general SMTP exceptions."""
        with patch('agents.email_sender.smtplib.SMTP') as mock_smtp:
            mock_server = MagicMock()
            mock_server.send_message.side_effect = smtplib.SMTPException("Connection failed")
            mock_smtp.return_value.__enter__.return_value = mock_server
            
            result = await email_agent.send_email(
                recipients=["test@example.com"],
                subject="Test",
                summary="Test",
                articles=sample_articles
            )
            
            assert result is False
    
    @pytest.mark.asyncio
    async def test_send_email_generic_exception(self, email_agent, sample_articles):
        """Test handling of unexpected exceptions."""
        with patch('agents.email_sender.smtplib.SMTP') as mock_smtp:
            mock_smtp.side_effect = Exception("Unexpected error")
            
            result = await email_agent.send_email(
                recipients=["test@example.com"],
                subject="Test",
                summary="Test",
                articles=sample_articles
            )
            
            assert result is False


@pytest.mark.unit
class TestEmailAgentHTMLGeneration:
    """Test EmailAgent HTML email generation."""
    
    @pytest.mark.asyncio
    async def test_email_contains_html_content(self, email_agent, sample_articles):
        """Test that generated email contains proper HTML structure."""
        with patch('agents.email_sender.smtplib.SMTP') as mock_smtp:
            mock_server = MagicMock()
            mock_smtp.return_value.__enter__.return_value = mock_server
            
            summary = "Test AI Summary Content"
            await email_agent.send_email(
                recipients=["test@example.com"],
                subject="Test",
                summary=summary,
                articles=sample_articles
            )
            
            # Get the sent message
            sent_msg = mock_server.send_message.call_args[0][0]
            
            # Extract HTML content from the message
            html_content = None
            for part in sent_msg.walk():
                if part.get_content_type() == 'text/html':
                    html_content = part.get_payload(decode=True).decode('utf-8')
                    break
            
            assert html_content is not None
            assert "<!DOCTYPE html>" in html_content
            assert "KeepMePosted" in html_content
            assert summary in html_content
    
    @pytest.mark.asyncio
    async def test_email_includes_articles(self, email_agent, sample_articles):
        """Test that email includes article information."""
        with patch('agents.email_sender.smtplib.SMTP') as mock_smtp:
            mock_server = MagicMock()
            mock_smtp.return_value.__enter__.return_value = mock_server
            
            await email_agent.send_email(
                recipients=["test@example.com"],
                subject="Test",
                summary="Summary",
                articles=sample_articles
            )
            
            # Get HTML content
            sent_msg = mock_server.send_message.call_args[0][0]
            html_content = None
            for part in sent_msg.walk():
                if part.get_content_type() == 'text/html':
                    html_content = part.get_payload(decode=True).decode('utf-8')
                    break
            
            # Check that article titles are in the HTML
            assert sample_articles[0]['title'] in html_content
            assert sample_articles[0]['link'] in html_content
    
    @pytest.mark.asyncio
    async def test_email_message_structure(self, email_agent, sample_articles):
        """Test that email message has correct structure and headers."""
        with patch('agents.email_sender.smtplib.SMTP') as mock_smtp:
            mock_server = MagicMock()
            mock_smtp.return_value.__enter__.return_value = mock_server
            
            subject = "Test Newsletter Subject"
            recipients = ["test1@example.com", "test2@example.com"]
            
            await email_agent.send_email(
                recipients=recipients,
                subject=subject,
                summary="Test",
                articles=sample_articles
            )
            
            sent_msg = mock_server.send_message.call_args[0][0]
            
            # Check headers
            assert sent_msg['Subject'] == subject
            assert sent_msg['From'] == "test@gmail.com"
            assert sent_msg['To'] == "test1@example.com, test2@example.com"
            
            # Check message is multipart
            assert sent_msg.is_multipart()


@pytest.mark.unit
class TestEmailAgentExecuteMethod:
    """Test EmailAgent execute() convenience method."""
    
    @pytest.mark.asyncio
    async def test_execute_calls_send_email(self, email_agent, sample_articles):
        """Test that execute() properly calls send_email()."""
        with patch('agents.email_sender.smtplib.SMTP') as mock_smtp:
            mock_server = MagicMock()
            mock_smtp.return_value.__enter__.return_value = mock_server
            
            recipients = ["test@example.com"]
            summary = "Test summary"
            
            result = await email_agent.execute(summary, sample_articles, recipients)
            
            assert result is True
            mock_server.send_message.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_execute_with_empty_articles(self, email_agent):
        """Test execute() with empty articles list."""
        with patch('agents.email_sender.smtplib.SMTP') as mock_smtp:
            mock_server = MagicMock()
            mock_smtp.return_value.__enter__.return_value = mock_server
            
            result = await email_agent.execute(
                summary="Test summary",
                articles=[],
                recipients=["test@example.com"]
            )
            
            # Should still succeed with empty articles
            assert result is True
            mock_server.send_message.assert_called_once()


@pytest.mark.unit
class TestEmailAgentEdgeCases:
    """Test EmailAgent edge cases and error conditions."""
    
    @pytest.mark.asyncio
    async def test_very_long_summary(self, email_agent, sample_articles):
        """Test handling of very long summary text."""
        with patch('agents.email_sender.smtplib.SMTP') as mock_smtp:
            mock_server = MagicMock()
            mock_smtp.return_value.__enter__.return_value = mock_server
            
            # Create a very long summary
            long_summary = "Test content. " * 1000  # ~14KB of text
            
            result = await email_agent.send_email(
                recipients=["test@example.com"],
                subject="Test",
                summary=long_summary,
                articles=sample_articles
            )
            
            assert result is True
    
    @pytest.mark.asyncio
    async def test_special_characters_in_subject(self, email_agent, sample_articles):
        """Test handling of special characters in email subject."""
        with patch('agents.email_sender.smtplib.SMTP') as mock_smtp:
            mock_server = MagicMock()
            mock_smtp.return_value.__enter__.return_value = mock_server
            
            subject = "Test 📧 Newsletter 🚀 with émojis & spëcial çhars"
            
            result = await email_agent.send_email(
                recipients=["test@example.com"],
                subject=subject,
                summary="Test",
                articles=sample_articles
            )
            
            assert result is True
            sent_msg = mock_server.send_message.call_args[0][0]
            assert sent_msg['Subject'] == subject
    
    @pytest.mark.asyncio
    async def test_many_articles(self, email_agent):
        """Test handling of many articles (should only include top 10)."""
        from datetime import datetime, timezone, timedelta
        
        # Create 20 articles
        many_articles = [
            {
                'source': f'Source{i}',
                'title': f'Article {i}',
                'link': f'https://example.com/article{i}',
                'published': datetime.now(timezone.utc) - timedelta(hours=i),
                'summary': f'Summary {i}'
            }
            for i in range(20)
        ]
        
        with patch('agents.email_sender.smtplib.SMTP') as mock_smtp:
            mock_server = MagicMock()
            mock_smtp.return_value.__enter__.return_value = mock_server
            
            result = await email_agent.send_email(
                recipients=["test@example.com"],
                subject="Test",
                summary="Test",
                articles=many_articles
            )
            
            assert result is True
            
            # Check that HTML was generated (template limits to 10 articles)
            sent_msg = mock_server.send_message.call_args[0][0]
            html_content = None
            for part in sent_msg.walk():
                if part.get_content_type() == 'text/html':
                    html_content = part.get_payload(decode=True).decode('utf-8')
                    break
            
            # First 10 should be present
            assert 'Article 0' in html_content
            assert 'Article 9' in html_content
            # Articles beyond 10 should not be in email (template limits to 10)
            assert 'Article 10' not in html_content

