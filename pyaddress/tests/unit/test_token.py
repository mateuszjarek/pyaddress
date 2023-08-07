import pytest

from app.services.address import Token, TokenType


class TestToken:

    @pytest.mark.parametrize(
        "token, expected",
        [
            (Token(TokenType.ALPHA, "Prosta"), 'Token(ALPHA, "Prosta")'),
            (Token(TokenType.NUM, "43"), 'Token(NUM, "43")')
        ]
    )
    def test_str(self, token, expected):
        assert str(token) == expected
