import time
import hashlib
from .core import OTP
from .rfc4226 import generate_hotp


class TOTP(OTP):
    TYPE = "TOTP"

    def __init__(self, secret: bytes, digit: int = 6, algorithm: str = "SHA1", period: int = 30):
        super().__init__(secret, digit, algorithm)
        self.period = period

    def generate(self, timestamp: int = None) -> int:
        """Generate a TOTP code.

        :param timestamp: Create TOTP at this given timestamp, default is now.
        """
        return generate_totp(self.secret, self.period, timestamp, self.digit, self.algorithm)

    def verify(self, code: int, timestamp: int = None) -> bool:
        """Valid a TOTP code for the given timestamp.

        :param code: A number to be verified.
        :param timestamp: Validate TOTP at this given timestamp, default is now.
        """
        if len(str(code)) > self.digit:
            return False
        return hashlib.compare_digest(bytes(self.generate(timestamp)), bytes(code))

    def to_uri(self, label: str, issuer: str) -> str:
        """Generate the otpauth protocal string for TOTP.

        :param label: Label of the identifier.
        :param issuer: The company, the organization or something else.
        """
        uri = f"otpauth://totp/{label}?secret={self.b32_secret}&issuer={issuer}&algorithm={self.algorithm}&digits={self.digit}"
        return uri + f"&period={self.period}"


def generate_totp(secret: bytes, period: int=30, timestamp: int=None, digit: int = 6, algorithm: str = "SHA1"):
    """Generate a TOTP code.

    A TOTP code is an extension of TOTP algorithm.

    :param secret: A secret token for the authentication.
    :param period: A period that a TOTP code is valid in seconds
    :param timestamp: Create TOTP at this given timestamp, default is now.
    """
    if timestamp is None:
        timestamp = time.time()
    counter = int(timestamp) // period
    return generate_hotp(secret, counter, digit, algorithm)