import re
from collections.abc import Generator

__all__ = ['break_line', 'remove_links']


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
                   re.X)


def remove_links(line: str) -> str:
    """
    Remove markup for links from line and keep the URL
    """
    line, _ = LINKS.subn('\\1', line)
    return line
