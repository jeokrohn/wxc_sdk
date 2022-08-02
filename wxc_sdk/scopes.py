"""
utility function to parse scopes from various input forms
"""
import urllib.parse


def parse_scopes(scopes: str) -> str:
    """
    parse various ways scopes might be defined.

    Examples:

    * 'https://webexapis.com/v1/authorize?client_id=Ce429631..d4835&response_type=code&redirect_uri=http%3A%2F
      %2Flocalhost%3A6001%2Fredirect&scope=spark%3Acalls_write%20spark%3Akms%20spark%3Apeople_read%20spark
      %3Acalls_read%20spark-admin%3Atelephony_config_read&state=set_state_here'
    * 'scope=spark%3Acalls_write%20spark%3Akms%20spark%3Apeople_read%20spark%3Acalls_read%20spark-admin
      %3Atelephony_config_read&state=set_state_here'
    * 'spark%3Acalls_write%20spark%3Akms%20spark%3Apeople_read%20spark%3Acalls_read%20spark-admin
      %3Atelephony_config_read&state=set_state_here'
    * 'spark%3Acalls_write%20spark%3Akms%20spark%3Apeople_read%20spark%3Acalls_read%20spark-admin
      %3Atelephony_config_read'
    * 'spark:calls_write spark:kms spark:people_read spark:calls_read spark-admin:telephony_config_read'

    :param scopes: scopes in one of the forms above
    :type scopes: str
    :return: space separated list of scopes
    :rtype: str
    """
    parsed = urllib.parse.urlparse(scopes)
    if parsed.query:
        # looks like we got full url
        query = parsed.query
    else:
        # else we assume that the string we got is a query or part of that
        query = scopes
    # try to parse the query and see whether the scope= part was in it
    parsed_query = urllib.parse.parse_qs(query)
    if 'scope' in parsed_query:
        return parsed_query['scope'][0]
    # .. else just unquote the string and return the part before the 1st "&" ... or the full string
    unquoted = urllib.parse.unquote(scopes)
    return unquoted.split('&')[0]
