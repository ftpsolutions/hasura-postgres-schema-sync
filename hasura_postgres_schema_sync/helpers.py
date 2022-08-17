import datetime
import time

from typing import Callable, Any, Optional


def call_until_truthy_or_timeout(
    method: Callable, timeout: float, message: Optional[str] = None
) -> Any:
    message = message or f"{method} failed to return a truthy value"

    expiry = datetime.datetime.now() + datetime.timedelta(seconds=timeout)

    while datetime.datetime.now() < expiry:
        try:
            return_value = method()
            if return_value:
                return return_value
        except Exception:
            pass

        time.sleep(1)

    raise TimeoutError(f"{message} after {timeout} seconds")
