`print('([\(\d\.]+[-\.\/\s]*[tor]*\d*[\.\/\s]*?\d*\s*)({})?[\s\)]+'.format('[cC][uU][pP]|[cC]'))`


`([\(\d\.]+[-\.\/\s]*[tor]*\d*[\.\/\s]*?\d*\s*)({})?[\s\)]+`

Let's break down the units regex. It has three chunks:

1. `([\(\d\.]+[-\.\/\s]*[tor]*\d*[\.\/\s]*?\d*\s*)` looks for:
    - **at least one** starting `(`, digit (`\d`), or `.` via `[\(\d\.]+`
    - followed by zero or more of `-`, `.`, `/`, or whitespace
    - followed by zero or more of `[tor]*` (which *should* match "to" and "or")
    - followed by zero or more digits `\d*`
    - followed by zero or more of `-`, `.`, `/`, or whitespace
    - followed by zero or more digits `\d*`
    - should we then look for parentheticals?
    - followed by zero or more whitespace `\s*`
2. `({})?` -> `([cC][uU][pP]|[cC])?` looks for units matches (of which there are many more), trying to match the shortest one (via the `?`)
3. `[\s\)]+` looks for
    - at least one whitespace `\s` or closing parenthesis `)`

I feel pretty good about chunks 2 and 3, but I suspect chunk 1 is missing some things.

We should break these down into mini-regexes and test the parts!

Ways we see units written:

- 1 cup
- 1/2 cup
- 0.5 cup
- .5 cup
- 1 1/2 cups
- 1-1/2 cups
- (8-ounce) as a modifier to an each unit, e.g. `1 (8-ounce) can`
- 1 or 2 cups
- 1 to 3 cups

Since we convert all vulgar fractions (e.g. ½) to normal ones, we don't need to worry about those in the regex.

Question: why is this parsing subsequent things with spaces (e.g. "1 1/2 cups") to 1ea, 0.5cups?

Everything but the starting ~digit sequence is optional.

We should also capture numbers as words: one, two, three, etc.
