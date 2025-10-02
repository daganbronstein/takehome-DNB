import requests

from classes.cache import CacheService
from enums.cache_keys import CacheKeys
from models.marketwatch_record import MarketwatchRecord


async def marketwatch_get_performance(stock_symbol) -> MarketwatchRecord:
    """
    The performance is cached/calculated server-side, we have no need for selenium, only the raw HTML.
    """
    # We will cache this content for one minute, as it appears the page updates minutely. If seconds matter, this
    # will require a different strategy.
    cache_key: str = f"{CacheKeys.MARKETWATCH}:{stock_symbol}"
    result: MarketwatchRecord = CacheService().get_object(cache_key)
    if result:
        return result

    content: str = _fetch(stock_symbol)

    # No reason to turn the HTML into an AST, or use regex. Both are slow, and content is not dynamic.
    header_pos: int = content.index(">Performance</span>")

    # The table comes immediately after the header. Determine where the table ends,
    #  to prevent scraping something we didn't mean to.
    end_table_pos: int = content.index("</table>", header_pos)

    performance_table: str = content[header_pos:end_table_pos]

    # TODO We should add a canary/structure sanity check against performance_table so that we can be informed if there
    #   was an unexpected change that broke our logic. We can automatically enumerate the table, of course, but then
    #   we risk unknown and even malformed fields, which is too dangerous

    # Iterates over every character in performance_table in order, and gathers the %
    #  Sanity check above guarantees they arrive in the expected order.
    performance_indices: list[int] = [i for i in range(len(performance_table)) if
                           performance_table.startswith('%', i) and performance_table[i + 1] == '<']

    data: list[str] = []

    for perf_index in performance_indices:
        raw_data: str = performance_table[perf_index - 6:perf_index + 1]

        try:
            span_index: int = raw_data.index(">")
            data.append(raw_data[span_index + 1:perf_index + 1])
        except ValueError:
            data.append(raw_data)

    result = {
        "five_day": data[0],
        "one_month": data[1],
        "three_month": data[2],
        "ytd": data[3],
        "one_year": data[4]
    }

    CacheService().set_object(cache_key, result)

    return result


def _fetch(stock_symbol: str) -> str:
    return requests.get(f"https://www.marketwatch.com/investing/stock/{stock_symbol}", headers={
        "Accept-Language": "en-GB,he;q=0.5",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:143.0) Gecko/20100101 Firefox/143.0",
    }).content.decode()
