import re
from collections.abc import Generator, Iterator, Iterable

__all__ = ['break_line', 'remove_links', 'sanitize_class_name', 'remove_html_comments', 'snake_case', 'words_to_camel',
           'lines_for_docstring', 'remove_div']

from itertools import chain, repeat

from re import Match

from typing import Optional
from urllib.parse import urljoin

from html2text import html2text


def words_to_camel(s: str) -> str:
    """
    Generate a camel case Python name from multi-word input string
    Example: 'User name' --> 'UserName'
    """

    def cap_first(s: str) -> str:
        return f'{s[0].upper()}{s[1:]}'

    r = ''.join(cap_first(w) for w in s.split())
    r, _ = re.subn(r'\W', '', r)
    return r


def snake_case(s: str) -> str:
    """
    Generate a snake case Python name for given input string.
    Input string can be a multiple words or a camel case string
    Examples:
        * 'user name' --> user_name
        * 'User Name' --> user_name
    """
    # get rid of all spaces
    r = s.replace(' ', '_')
    # add underscore whenever a capital letter is preceded by lower case or digit
    r, _ = re.subn(r'([a-z0-9])([A-Z])', '\\1_\\2', r)
    # add underscore whenever a letter or digit is preceded by non-word character other than underscore
    r, _ = re.subn(r'[^_\w]([A-Za-z0-9])', '_\\1', r)
    # finally get rid of all unwanted characters
    r, _ = re.subn(r'[^_\w0-9]', '_', r)
    r = r.lower()
    return r


def sanitize_class_name(class_name: Optional[str]) -> str:
    if class_name is None:
        return class_name
    class_name, _ = re.subn(r'\W', '', class_name)
    return class_name


def break_line(line: str, width: int = None, prefix: str = '',
               prefix_first_line: str = None) -> Generator[str, None, None]:
    """
    Break line in multiple lines of given length
    """

    def net_len(p: str) -> int:
        # len(p) only counting text (w/o links)
        p, _ = LINKS.subn('\\1', p)
        r = len(p)
        return r

    def cannot_be_line_start(p: str) -> bool:
        # some parts cannot be at start of line
        return False

    width = width or 120
    # convert something like this:
    #   ... this link (https://.....) for the format.
    # to something like this:
    #   ... this [link](https://.....) for the format.
    line, _ = re.subn(r"""(\S+)     # capture: sequence of non spaces
                          \s+       # followed by space(s)
                          (         # capture: 
                            \(      # opening bracket
                            https?:[^\)]+  # sequence of characters except closing bracket
                            \)      # closing bracket
                          )""", '[\\1]\\2', line, flags=re.VERBOSE)
    # consume line tokens while length of combined token sequence (for links only consider text) smaller than desired
    # width. If token that's pushing to next line is a scope (bla:blub) then also push the previous token to next line.
    # when yielding a line convert links to RST links .. which breaks the line into two lines
    # RST links: https://docutils.sourceforge.io/docs/user/rst/quickref.html#hyperlink-targets
    # parts of line, reversed to be able to pop/push
    if prefix_first_line is None:
        prefix_first_line = prefix
    line = line.strip()
    if not line.strip():
        # shortcut for empty lines
        yield f'{prefix_first_line}{line}'
        return
    parts = list(reversed(list(line_parts(line))))
    line = []
    line_len = len(prefix_first_line)
    while parts:
        next_part = parts.pop()
        line_len += net_len(next_part)
        if line_len < width or not line:
            # for some reason a single token is longer than the max line len we still want to add a line just with
            # this token
            line.append(next_part)
        else:
            # line will be too long
            if cannot_be_line_start(next_part):
                parts.append(next_part)
                parts.append(line.pop())
            else:
                parts.append(next_part)
            yield from links_to_rst(''.join(line), prefix_first_line=prefix_first_line, prefix=prefix)
            prefix_first_line = prefix
            line_len = len(prefix_first_line)
            line = []
    if line:
        try:
            yield from links_to_rst(''.join(line), prefix_first_line=prefix_first_line, prefix=prefix)
        except TypeError as e:
            foo = 1

    # while line:
    #     if len(line) <= width:
    #         yield line
    #         return
    #     end_of_previous_word = next((i for i in range(len(line)) if line[width - i] == ' '), None)
    #     if end_of_previous_word is None:
    #         yield line
    #         return
    #     start = line[:width - end_of_previous_word]
    #     yield start
    #     line = line[width - end_of_previous_word + 1:]
    #     line = f'{prefix}{line}'
    return


LINKS = re.compile(r"""\[               # links start with a squared bracket
                        (.+?)]            # followed by some text until the closing bracket
                        \((.+?)\)   # and then the URL in rounded brackets. We want to extract the part 
                                        # in the brackets""",
                   re.X + re.MULTILINE)


def remove_links(line: str) -> str:
    """
    Remove markup for links from line and keep the URL
    """

    def repl(m: Match) -> str:
        return f'`{m.group(1)}<{m.group(2)}>`_'

    line, _ = LINKS.subn(repl, line)
    return line


LINK_BASE = 'https://developer.webex.com'


def links_to_rst(line: str, prefix: str, prefix_first_line: str) -> Generator[str, None, None]:
    """
    Generate (multiple) lines required for lines with links. RST links are multi-line
    """

    def repl(m: Match) -> str:
        # an RST link looks like this:
        #   External hyperlinks, like `Python
        #   <https://www.python.org/>`_.
        link = m.group(2)
        if link.startswith('/'):
            urljoin(LINK_BASE, link)
            link = f'{LINK_BASE}{link}'
        nl = '\n'
        r = f'`{m.group(1)}{nl}<{link}>`_'
        return r

    line = line.strip()
    line, _ = LINKS.subn(repl, line)
    lines = line.splitlines()
    prefixes = [prefix_first_line, prefix]
    yield from (f'{p}{l}' for l, p in zip(lines, prefixes))


def remove_html_comments(text: str) -> str:
    """
    Remove stuff like:
        <!-- feature-toggle-name:wxc-cpapi-receptionist-72075 -->
    :param text:
    :return:
    """
    text, _ = re.subn(r'<!--.+?-->\s*', '', text, flags=re.MULTILINE)
    return text


def remove_div(text: str):
    def repl(m: Match) -> str:
        r = html2text(m.group(0))
        return r

    text, _ = re.subn(r'<div>.+?</div>', repl, text)
    return text


def line_parts(line: str) -> Iterator[str]:
    fiter = re.finditer(r"""(?P<word>\s*
                                     (?:     # split lines in sequences of ...
                                     (?:\[               # links: start with a squared bracket
                                          (.+?)]            # followed by some text until the closing bracket
                                          \((.+?)\))    # .. and the actual link in brackets
                                     |\S    # or a non-whitespace character 
                                    )+)""",
                        line,
                        re.VERBOSE)
    return (m.group('word') for m in fiter)


def lines_for_docstring(docstring: str, text_prefix_for_1st_line: str = '', indent: int = 0,
                        indent_first_line: int = 0, width: int = None) -> Iterable[str]:
    """
    Break a docstring in lines where the 1st line has a leading text, make sure that all lines are properly indented
    """
    if not docstring:
        return []
    doc_string_lines = (f'{p}{line}' for p, line in zip(chain([text_prefix_for_1st_line],
                                                              repeat('')),
                                                        docstring.splitlines()))
    return chain.from_iterable(break_line(line, prefix=' ' * indent,
                                          prefix_first_line=' ' * indent_first,
                                          width=width)
                               for line, (indent_first, indent) in zip(doc_string_lines,
                                                                       chain([(indent_first_line, indent)],
                                                                             repeat((indent_first_line,
                                                                                     indent_first_line)
                                                                                    ))))
