import json
import logging
import re
import sys
from typing import List

import requests
from bs4 import BeautifulSoup
from pydantic import ValidationError

from tidecast.constants import LOCATIONS
from tidecast.exceptions import TidecastError
from tidecast.models import LowDaylightTides, LowTide, TideDay

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)


def main() -> None:
    """Entrypoint"""
    results = {}
    for location, url in LOCATIONS:
        _logger.info(f"Finding low tides for {location}...")
        try:
            results[location] = _get_low_tide_data(url)
        except TidecastError as e:
            _logger.error(f"Could not find low tides at {location} due to: {e}")
        except Exception as ex:
            _logger.exception(
                f"There was an unhandled exception while trying to find tide data for {location}: {ex}"
            )
            sys.exit(1)

    _pretty_print_results(results)


def _get_low_tide_data(url: str) -> List[LowDaylightTides]:
    """
    Get all low daylight tides from a given location at www.tide-forecast.com

    :param url: The tide-forecast URL for the given location, eg https://www.tide-forecast.com/locations/Wrightsville-Beach-North-Carolina/tides/latest
    :return: Low tide data
    """

    page_data: str = _load_page_data(url)
    tide_days: List[TideDay] = _parse_tide_data_from_page(page_data)
    return _find_low_daylight_tides(tide_days)


def _pretty_print_results(results):
    """Just pretty print the results to stdout."""
    print("Low tides during daylight hours:")
    for location, data in results.items():
        print(f"\n{location}:")
        for day in data:
            print(f"  {day.date}")
            if not day.tides:
                print("    No low tides during the day")
            else:
                for tide in day.tides:
                    print(f"    Low Tide: {tide.time} Height: {tide.height}")


def _load_page_data(url) -> str:
    """
    Load a particular tide-forecast page, and return the raw html content.

    :raises TidecastException: if the request failed for any reason
    """
    try:
        _logger.info(f"Requesting data from url: {url}")
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        raise TidecastError(
            f"Failed to get tidal data from {url} because the request failed: {e}"
        )


def _parse_tide_data_from_page(html_page_data: str) -> List[TideDay]:
    """
    Parse all the tide info out of the given html.

    :raises: TidecastException if the given page data could not be parsed.
    """
    try:
        _logger.info("Decoding html data...")
        soup: BeautifulSoup = BeautifulSoup(html_page_data, features="html.parser")

        # A JS object is available, wrapped in CDATA tags with all of the tidal info needed.
        cdata = soup.find(string=re.compile("CDATA"))
        if not cdata:
            raise TidecastError("Could not find CDATA section in the given page data")

        # Strip some junk away from the edges of the cdata, so we can turn it into a plain object
        json_str: str = (
            str(cdata.extract())
            .lstrip("\n//<![CDATA[\nwindow.FCGON =")
            .rstrip(";\n//]]>\n")
        )

        return [TideDay(**day) for day in json.loads(json_str)["tideDays"]]

    except (json.JSONDecoder, KeyError, ValidationError) as e:
        raise TidecastError(
            "The parsed CDATA was not formatted as expected, so we failed to parse it."
        ) from e


def _find_low_daylight_tides(tide_days: List[TideDay]) -> List[LowDaylightTides]:
    """Filter out all non-daylight, non-low tides."""
    _logger.info("Finding low tides in the day...")

    results: List[LowDaylightTides] = []
    for tide_day in tide_days:
        low_tides = []
        for tide in tide_day.tides:
            # Some days have no low tides during daylight hours
            if (
                tide_day.sunrise <= tide.timestamp <= tide_day.sunset
                and tide.type == "low"
            ):
                low_tides.append(LowTide(height=tide.height, time=tide.time))
        results.append(LowDaylightTides(date=tide_day.date, tides=low_tides))

    return results


main()
