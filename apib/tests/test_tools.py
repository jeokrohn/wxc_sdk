from unittest import TestCase

from apib.tools import line_parts, break_line


class TestLineIter(TestCase):
    def test_simple_words(self):
        words = list(line_parts('just some simple words.'))
        self.assertEqual(['just', ' some', ' simple', ' words.'], words)

    def test_words_with_link(self):
        link = '[this is a link](https://www.something.org)'
        line = f'line with a link: {link}'
        words = list(line_parts(line))
        self.assertEqual(['line', ' with', ' a', ' link:', f' {link}'], words)

    def test_words_with_link_and_dot(self):
        link = '[this is a link](https://www.something.org).'
        line = f'line with a link: {link}'
        words = list(line_parts(line))
        self.assertEqual(['line', ' with', ' a', ' link:', f' {link}'], words)

    def test_xxxx(self):
        s = "Authorizations are user grants to applications to act on the user's behalf. Authorizations are how [Integrations](/docs/integrations) get authorized with specific [access scopes](/docs/integrations#scopes) in the oAuth client life-cycle. Integrations and some of the Webex service portals, like [developer.webex.com](https://developer.webex.com/), are all oAuth clients, each with their unique `clientId`."
        words = list(line_parts(s))
        lines = list(break_line(s, prefix_first_line='    '))

        s = "Your application receives an API [access token](/docs/integrations#getting-an-access-token) and a [refresh token](/docs/integrations#using-the-refresh-token) through the oAuth process. The access token is used to call Webex APIs for which the user authorized the scopes. Access tokens expire fairly frequently, while refresh tokens (when being regularly used) will be refreshed to last forever (see [Using the Refresh Token](/docs/integrations#using-the-refresh-token) for details)."
        words = list(line_parts(s))
        lines = list(break_line(s, prefix_first_line='    '))
        foo = 1