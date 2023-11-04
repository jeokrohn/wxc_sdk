import re
from collections.abc import Generator

__all__ = ['break_line', 'remove_links', 'sanitize_class_name', 'remove_html_comments', 'snake_case', 'words_to_camel']

from typing import Optional


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
    r = r.lower()
    return r


def sanitize_class_name(class_name: Optional[str]) -> str:
    if class_name is None:
        return class_name
    class_name, _ = re.subn('\W', '', class_name)
    return class_name


def break_line(line: str, width: int = 80, prefix: str = '') -> Generator[str, None, None]:
    """
    Break line in multiple lines of given length
    """
    while line:
        if len(line) <= width:
            yield line
            return
        end_of_previous_word = next((i for i in range(len(line)) if line[width - i] == ' '), None)
        if end_of_previous_word is None:
            yield line
            return
        start = line[:width - end_of_previous_word]
        yield start
        line = line[width - end_of_previous_word + 1:]
        line = f'{prefix}{line}'


LINKS = re.compile(r"""\[               # links start with a squared bracket
                        .+?]            # followed by some text until the closing bracket
                        \((http.+?)\)   # and then the URL in rounded brackets. We want to extract the part 
                                        # in the brackets""",
                   re.X + re.MULTILINE)


def remove_links(line: str) -> str:
    """
    Remove markup for links from line and keep the URL
    """
    line, _ = LINKS.subn('\\1', line)
    return line


def remove_html_comments(text: str) -> str:
    text, _ = re.subn(r'<!--.+?-->\s+', '', text, flags=re.MULTILINE)
    return text
