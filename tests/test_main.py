import pytest

from tidecast.exceptions import TidecastError
from tidecast.main import (_find_low_daylight_tides, _get_low_tide_data,
                           _load_page_data, _parse_tide_data_from_page)
from tidecast.models import TideDay


@pytest.fixture
def valid_forecast_html():
    with open("tests/resources/tide_forecasts/valid_page.html", "r") as f:
        yield f.read()


def test_parse_tide_data_from_page__valid_page__results_parsed(valid_forecast_html):
    results = _parse_tide_data_from_page(valid_forecast_html)

    assert len(results) == 29
    assert all(isinstance(v, TideDay) for v in results)
    assert results[0].date == "2022-10-11"


@pytest.mark.parametrize(
    "filename", ["empty_response.html", "no_cdata.html", "malformed_cdata.html"]
)
def test_parse_tide_data_from_page__unexpected_html__errors_caught(filename):
    with open(f"tests/resources/tide_forecasts/{filename}", "r") as f:
        with pytest.raises(TidecastError):
            _parse_tide_data_from_page(f.read())
