from typing import List, Tuple

import pytest

from app.services.address import AddressParser, Token, TokenType


class TestAddressParser:
    """AddressParser test suite."""

    @pytest.mark.parametrize(
        "address, expected_tokens", [
            (
                "Winterallee 3",
                [Token(TokenType.ALPHA, "Winterallee"), Token(TokenType.NUM, "3")]
            ),
            (
                "Musterstrasse 45",
                [Token(TokenType.ALPHA, "Musterstrasse"), Token(TokenType.NUM, "45")]
            ),
            (
                "Blaufeldweg 123B",
                [
                    Token(TokenType.ALPHA, "Blaufeldweg"),
                    Token(TokenType.NUM, "123B")
                ]
            ),
            (
                "Am Bächle 2",
                [
                    Token(TokenType.ALPHA, "Am"),
                    Token(TokenType.ALPHA, "Bächle"),
                    Token(TokenType.NUM, "2")
                ]
            ),
            (
                "Auf der Vogelwiese 23 b",
                [
                    Token(TokenType.ALPHA, "Auf"),
                    Token(TokenType.ALPHA, "der"),
                    Token(TokenType.ALPHA, "Vogelwiese"),
                    Token(TokenType.NUM, "23"),
                    Token(TokenType.ALPHA, "b"),
                ]
            ),
            (
                "4, rue de la revolution",
                [
                    Token(TokenType.NUM, "4"),
                    Token(TokenType.ALPHA, "rue"),
                    Token(TokenType.ALPHA, "de"),
                    Token(TokenType.ALPHA, "la"),
                    Token(TokenType.ALPHA, "revolution"),
                ]
            ),
            (
                "200 Broadway Av",
                [
                    Token(TokenType.NUM, "200"),
                    Token(TokenType.ALPHA, "Broadway"),
                    Token(TokenType.ALPHA, "Av"),
                ]
            ),
            (
                "Calle Aduana, 29",
                [
                    Token(TokenType.ALPHA, "Calle"),
                    Token(TokenType.ALPHA, "Aduana"),
                    Token(TokenType.NUM, "29")
                ]
            ),
            (
                "Calle 39 No 154",
                [
                    Token(TokenType.ALPHA, "Calle"),
                    Token(TokenType.NUM, "39"),
                    Token(TokenType.ALPHA, "No"),
                    Token(TokenType.NUM, "154")
                ]
            ),
            (
                "ul. Bitwy Warszawskiej 1920 15",
                [
                    Token(TokenType.ALPHA, "ul"),
                    Token(TokenType.ALPHA, "Bitwy"),
                    Token(TokenType.ALPHA, "Warszawskiej"),
                    Token(TokenType.NUM, "1920"),
                    Token(TokenType.NUM, "15"),
                ]
            ),
            (
                "ul. Bitwy Warszawskiej 1920 43/45",
                [
                    Token(TokenType.ALPHA, "ul"),
                    Token(TokenType.ALPHA, "Bitwy"),
                    Token(TokenType.ALPHA, "Warszawskiej"),
                    Token(TokenType.NUM, "1920"),
                    Token(TokenType.NUM, "43/45")
                ]
            ),
            (
                "ul. Bitwy Warszawskiej 1920 nr 43/45",
                [
                    Token(TokenType.ALPHA, "ul"),
                    Token(TokenType.ALPHA, "Bitwy"),
                    Token(TokenType.ALPHA, "Warszawskiej"),
                    Token(TokenType.NUM, "1920"),
                    Token(TokenType.ALPHA, "nr"),
                    Token(TokenType.NUM, "43/45")
                ]
            )
        ]
    )
    def test_address_tagging(self, address: str, expected_tokens: List[Token]):
        address_parser = AddressParser()
        normalized_address = address_parser.normalize(address)
        tokenized_address = address_parser.tokenize(normalized_address)
        tagged = address_parser.tag(tokenized_address)
        assert len(tagged) == len(expected_tokens)

    @pytest.mark.parametrize(
        "tokens, expected_tokens", [
            (
                [
                    Token(token_type=TokenType.ALPHA, value="Winterallee"),
                    Token(token_type=TokenType.NUM, value="3")
                ]
                ,
                [
                    Token(token_type=TokenType.ALPHA, value="Winterallee"),
                    Token(token_type=TokenType.NUM, value="3")
                ]
            ),
            (
                [
                    Token(token_type=TokenType.ALPHA, value="Am"),
                    Token(token_type=TokenType.ALPHA, value="Bächle"),
                    Token(token_type=TokenType.NUM, value="23")
                ],
                [
                    Token(token_type=TokenType.ALPHA, value="Am Bächle"),
                    Token(token_type=TokenType.NUM, value="23")
                ]
            ),
            (
                [
                    Token(token_type=TokenType.ALPHA, value="Auf"),
                    Token(token_type=TokenType.ALPHA, value="der"),
                    Token(token_type=TokenType.ALPHA, value="Vogelwiese"),
                    Token(token_type=TokenType.NUM, value="23"),
                    Token(token_type=TokenType.ALPHA, value="b")
                ],
                [
                    Token(token_type=TokenType.ALPHA, value="Auf der Vogelwiese"),
                    Token(token_type=TokenType.NUM, value="23"),
                    Token(token_type=TokenType.ALPHA, value="b")
                ]
            ),
            (
                [
                    Token(token_type=TokenType.NUM, value="4"),
                    Token(token_type=TokenType.ALPHA, value="rue"),
                    Token(token_type=TokenType.ALPHA, value="de"),
                    Token(token_type=TokenType.ALPHA, value="la"),
                    Token(token_type=TokenType.ALPHA, value="revolution")
                ],
                [
                    Token(token_type=TokenType.NUM, value="4"),
                    Token(token_type=TokenType.ALPHA, value="rue de la revolution")
                ],
            ),
            (
                [
                    Token(token_type=TokenType.NUM, value="200"),
                    Token(token_type=TokenType.ALPHA, value="Broadway"),
                    Token(token_type=TokenType.ALPHA, value="Av")
                ],
                [
                    Token(token_type=TokenType.NUM, value="200"),
                    Token(token_type=TokenType.ALPHA, value="Broadway Av")
                ]
            ),
            (
                [
                    Token(token_type=TokenType.ALPHA, value="Calle"),
                    Token(token_type=TokenType.ALPHA, value="Aduana"),
                    Token(token_type=TokenType.NUM, value="29")
                ],
                [
                    Token(token_type=TokenType.ALPHA, value="Calle Aduana"),
                    Token(token_type=TokenType.NUM, value="29")
                ]
            ),
            (
                [
                    Token(token_type=TokenType.ALPHA, value="Calle"),
                    Token(token_type=TokenType.NUM, value="39"),
                    Token(token_type=TokenType.ALPHA, value="No"),
                    Token(token_type=TokenType.NUM, value="1540")
                ],
                [
                    Token(token_type=TokenType.ALPHA, value="Calle"),
                    Token(token_type=TokenType.NUM, value="39"),
                    Token(token_type=TokenType.ALPHA, value="No"),
                    Token(token_type=TokenType.NUM, value="1540")
                ],
            ),
            (
                [
                    Token(token_type=TokenType.ALPHA, value="ul"),
                    Token(token_type=TokenType.ALPHA, value="Bitwy"),
                    Token(token_type=TokenType.ALPHA, value="Warszawskiej"),
                    Token(token_type=TokenType.NUM, value="1920"),
                    Token(token_type=TokenType.NUM, value="8")
                ],
                [
                    Token(token_type=TokenType.ALPHA, value="ul Bitwy Warszawskiej"),
                    Token(token_type=TokenType.NUM, value="1920"),
                    Token(token_type=TokenType.NUM, value="8"),
                ]
            )
        ]
    )
    def test_chunking_tagged_address(self, tokens: List[Token], expected_tokens: List[Token]):
        # result = AddressParser().chunk(tokens)
        assert AddressParser().chunk(tokens) == expected_tokens

    @pytest.mark.parametrize(
        "address, expected_result",
        [
            ("Winterallee 3", {"street": "Winterallee", "house_number": "3"}),
            ("Musterstrasse 45", {"street": "Musterstrasse", "house_number": "45"}),
            ("Blaufeldweg 123B", {"street": "Blaufeldweg", "house_number": "123B"}),
            ("Am Bächle 23", {"street": "Am Bächle", "house_number": "23"}),
            ("Auf der Vogelwiese 23 b", {"street": "Auf der Vogelwiese", "house_number": "23 b"}),
            ("4, rue de la revolution", {"street": "rue de la revolution", "house_number": "4"}),
            ("200 Broadway Av", {"street": "Broadway Av", "house_number": "200"}),
            ("Calle Aduana, 29", {"street": "Calle Aduana", "house_number": "29"}),
            ("Auf der Vogelwiese 23 b", {"street": "Auf der Vogelwiese", "house_number": "23 b"}),
            ("Calle 39 No 1540", {"street": "Calle 39", "house_number": "No 1540"}),
            # more complicated Polish address formats
            (
                "ul Bitwy Warszawskiej 1920 8",
                {"street": "ul Bitwy Warszawskiej 1920", "house_number": "8"}
            ),
            (
                    "ul Bitwy Warszawskiej 1920 8/10",
                    {"street": "ul Bitwy Warszawskiej 1920", "house_number": "8/10"}
            ),
            # and let's try with first Czech in line: obviously it turned out to fail
            # that's the best proof that is not the best solution to maintain when address formats
            # are considered. More details can be found in
            # ("5. května 798/62", {"street": "5. května", "house_number": "798/62"},),
        ]
    )
    def test_parse(self, address: str, expected_result: Tuple[str, int]):
        """Test parsing result."""
        assert AddressParser().parse(address) == expected_result
