# Solution

First I must thank you for opportunity to challenge myself with such 
a great problem I have never thought about earlier. It seems to be a really complex
issue to parse address string without any prior knowledge about the country.

At the beginning I totally rejected regex based solution. I thought that extending solution
to handle another fields and maintaining regex which grows and grows (considering multinational
addresses) will be hell.

As I had some basic knowledge about NLP (playing with nltk and spacy) I decided to go this way.
But instead of using existing package like the ones I mentioned I decided to write completely 
own parser. General idea was that each address must go through multiple steps:

1. normalization
2. tokenization
3. tagging
4. chunking
5. parsing (which might be considered as chunk pattern matching and getting required result)

For the simplicity I left normalization and tokenization almost untouched - it is easy to add 
some customization if needed.

Tagging process is a process when each token (string) is tagged as a `TokenType.ALPHA` 
or `TokenType.NUM` token. Tokens like "43/45" or "123B" are considered to be `TokenType.NUM`.

Chunking process is a process of merging tagged tokens. In a considered case only `TokenType.ALPHA`
tokens are merged into chunks. 

In the last parsing part I must admire I was in a hurry and there is a very naive pattern matching.

## Web service

All webapp stuff is here as I first thought, hey, let's make a web service to show Python backend
skills.

## Tests

Tests could be easily extended to any addresses but due to time limitation I tested only given
dataset + few Polish ones considered to be difficult.

## Summary

Definitely not something to be proud of but still I taught a lot. Parsing even so easy address
can be challenging. It was quite easy to become convinced of that. I took first Czech address
from Google Maps: "5. května 798/62" and my pattern matching failed as pair number-alpha in this
case is not chunked correctly and even if it was chunked correctly we hit list of predefined 
`patterns` in `AddressParser`.

If I were to have more time I would definitely go into more details of text extraction topic,
like here: https://www.nltk.org/book/ch07.html (seems to be good for beginning). 

I would also get more into details about tagging (IOB tags or just implement some more sophisticated
custom tagging mechanism) and chunking (I saw some chunker examples in nltk).

As the last instead of stupid pattern matching maybe using some trained model would be good?
Don't know as still it requires training data set.

To sum up, as I mentioned at the beginning, address parsing turned out to be really challenging :)
