"""
Title: address.py
Author: Mateusz Jarek <mateuszjarek.mj@gmail.com>

Description:

    Address management service for processing multinational addresses (e.g. extracting address
    components like street or number).

"""
import enum
from typing import Dict, Generator, List

from app.schemas.address import Address


class AddressServiceError(Exception):
    """Address service base exception class."""


class TokenType(str, enum.Enum):
    """Token type representation."""

    ALPHA = "ALPHA"  # possible street name or part of the street name
    NUM = "NUM"  # possible housenumber


class Token:
    """Represent single chunk of input address."""

    def __init__(self, token_type: TokenType, value: str):
        self.token_type = token_type
        self.value = value

    def __str__(self) -> str:
        """Return token string representation."""
        return f'Token({self.token_type.value}, "{self.value}")'

    def __eq__(self, other):
        if isinstance(other, Token):
            return bool(self.token_type == other.token_type and self.value == other.value)
        return False


class AddressParser:

    internal_punctuation = ".,"   # might want to extend this

    @staticmethod
    def normalize(address: str) -> str:
        """Normalize processed address.

        Args:
            address: Input address.

        Returns:
            Normalized address string.

        """
        # return address.casefold()
        return address

    @staticmethod
    def tokenize(address: str) -> List[str]:
        """Tokenize address statements. For simplicity just split address text (nltk tokenizer
        could be used).

        Args:
            address: Normalized input address.

        Returns:
            List of tokens.

        """
        return address.strip().split()

    @staticmethod
    def tag(tokenized_address: List[str]) -> List[Token]:
        """Perform very simple tagging on address components. Assign token type to each token.
        Skip punctuation marks tokens.

        Notes:
            If time was not a root factor I would definitely investigate e.g. NLTK to try another
            way of tagging: maybe built-in or maybe there is a way to build custom one:
            https://www.nltk.org/book/ch07.html

        Args:
            tokenized_address: Address tokens.

        Returns:
            List of tagged address components (tokens).

        """
        tokens = []
        for word in tokenized_address:
            word = word.replace(".", "").replace(",", "")
            if word.isalpha():
                token = Token(TokenType.ALPHA, word)
            elif word.isnumeric():
                token = Token(TokenType.NUM, word)
            elif word.isalnum():
                if word[0].isdigit() and word[-1].isalpha():
                    token = Token(TokenType.NUM, word)
                elif word[0].isdigit() and word[-1].isdigit() and "/" in word:
                    token = Token(TokenType.NUM, word)
                else:
                    raise AddressServiceError(
                        f"unsupported address format: {' '.join(tokenized_address)}"
                    )
            elif word[0].isdigit() and word[-1].isdigit() and "/" in word:
                token = Token(TokenType.NUM, word)
            else:
                raise AddressServiceError(
                    f"unsupported address format: {' '.join(tokenized_address)}"
                )
            tokens.append(token)
        return tokens

    @staticmethod
    def chunk(tokens: List[Token]) -> List[Token]:
        result = []
        chunk = []
        for token in tokens:
            if token.token_type == TokenType.ALPHA:
                chunk.append(token)
            if token.token_type == TokenType.NUM:
                if chunk:
                    result.append(
                        Token(token_type=TokenType.ALPHA, value=" ".join([t.value for t in chunk]))
                    )
                    chunk = []
                result.append(token)
        if chunk:
            result.append(
                Token(token_type=TokenType.ALPHA, value=" ".join([t.value for t in chunk]))
            )
        return result

    @staticmethod
    def parse(address) -> Dict:
        """Parse given address.

        Args:
            address: Input address string.

        Raise:
            AddressServiceError: If address format is not supported.

        Returns:
            Address components Python dictionary with street and house_number.
        """
        # very basic tokenized address pattern matching, it's definitely not a solution
        # of the future (and as a whole) as different addresses may surprise us

        address_parser = AddressParser()
        parse_map = [
            {
                "pattern": (TokenType.ALPHA, TokenType.NUM),
                "map": {"street": [0], "house_number": [1]}
            },
            {
                "pattern": (TokenType.NUM, TokenType.ALPHA),
                "map": {"street": [1], "house_number": [0]}
            },
            {
                "pattern": (TokenType.ALPHA, TokenType.NUM, TokenType.ALPHA),
                "map": {"street": [0], "house_number": [1, 2]}
            },
            {
                "pattern": (TokenType.ALPHA, TokenType.NUM, TokenType.NUM),
                "map": {"street": [0, 1], "house_number": [2]}
            },
            {
                "pattern": (TokenType.ALPHA, TokenType.NUM, TokenType.ALPHA, TokenType.NUM),
                "map": {"street": [0, 1], "house_number": [2, 3]}
            }
        ]

        normalized_address = address_parser.normalize(address)
        tokenized_address = address_parser.tokenize(normalized_address)
        tagged = address_parser.tag(tokenized_address)
        chunked = address_parser.chunk(tagged)

        # ugly but it's late on Monday and I just want to make it work...
        match = None
        patterns = [option for option in parse_map if len(option["pattern"]) == len(chunked)]
        for option in patterns:
            if list(option["pattern"]) == [chunk.token_type for chunk in chunked]:
                match = option
                break
        if not match:
            raise AddressServiceError(f"unsupported address format: {' '.join(tokenized_address)}")
        try:
            street = " ".join(
                [chunked[i].value for i, _ in enumerate(chunked) if i in match["map"]["street"]]
            )
            house_number = " ".join(
                [
                    chunked[i].value for i, _ in enumerate(chunked)
                    if i in match["map"]["house_number"]
                ]
            )
        except AttributeError as err:
            raise AddressServiceError(f"unsupported address format: {' '.join(tokenized_address)}")\
                from err
        parsed = {"street": street, "house_number": house_number}
        return parsed


class AddressService:

    @staticmethod
    def extract_address_components(address: str) -> Address:
        """
        Args:

            address:

        Raises:
            AddressServiceError if extracting separated street and number values from address fails.

        Returns:

            If processing input address succeeds Address instance with separated street and number
            is returned.

        """
        parsed_address = AddressParser().parse(address)
        return Address(**parsed_address)


def get_address_service() -> Generator[AddressService, None, None]:
    """Return address service generator."""
    yield AddressService()
