"""
Simple retry decorators for external API calls.
"""

from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type


def retry_on_network_error(max_attempts=2, min_wait=2, max_wait=10):
    """
    Retry decorator for network-related errors.

    Args:
        max_attempts: Maximum number of retry attempts
        min_wait: Minimum wait time in seconds
        max_wait: Maximum wait time in seconds

    Usage:
        @retry_on_network_error()
        def fetch_data():
            return requests.get(url)
    """
    return retry(
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential(multiplier=1, min=min_wait, max=max_wait),
        retry=retry_if_exception_type((ConnectionError, TimeoutError)),
    )


def retry_on_api_error(max_attempts=3, min_wait=4, max_wait=30):
    """
    Retry decorator for API calls (longer backoff).

    Args:
        max_attempts: Maximum number of retry attempts
        min_wait: Minimum wait time in seconds
        max_wait: Maximum wait time in seconds

    Usage:
        @retry_on_api_error()
        async def call_api():
            return await api.generate()
    """
    return retry(
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential(multiplier=1, min=min_wait, max=max_wait),
        retry=retry_if_exception_type((ConnectionError, TimeoutError)),
    )
