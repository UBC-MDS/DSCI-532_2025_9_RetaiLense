import pytest
import pandas as pd
from unittest.mock import MagicMock
from datetime import datetime

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.callbacks import (
    plot_monthly_revenue_chart,
    plot_stacked_chart,
    plot_top_products_revenue,
    plot_top_countries_pie_chart,
    update_cards,
    compute_other_countries,
    store_selected_country,
    update_country_dropdown
)
from src.app import cache

def disable_cache():
    cache.clear()  # Clear any existing cache
    cache.memoize = lambda *args, **kwargs: lambda func: func  # Disable caching

disable_cache()

@pytest.mark.parametrize("start_date, end_date, selected_countries", [("2010-12-01", "2010-12-31", ["United Kingdom", "France"])])
def test_plot_monthly_revenue_chart(start_date, end_date, selected_countries):
    """
    Tests the plot_monthly_revenue_chart function to ensure it returns a valid Altair chart specification.
    """
    result = plot_monthly_revenue_chart(start_date, end_date, selected_countries)
    assert isinstance(result, dict), "Output should be a dictionary representing an Altair chart."

@pytest.mark.parametrize("start_date, end_date, selected_countries", [("2010-12-01", "2010-12-31", ["United Kingdom", "France"])])
def test_plot_stacked_chart(start_date, end_date, selected_countries):
    """
    Tests the plot_stacked_chart function to ensure it returns a valid Altair chart specification.
    """
    result = plot_stacked_chart(start_date, end_date, selected_countries)
    assert isinstance(result, dict), "Output should be a dictionary representing an Altair chart."

@pytest.mark.parametrize("start_date, end_date, selected_countries", [("2010-12-01", "2010-12-31", ["United Kingdom", "France"] )])
def test_plot_top_products_revenue(start_date, end_date, selected_countries):
    """
    Tests the plot_top_products_revenue function to ensure it returns a valid Altair chart specification.
    """
    result = plot_top_products_revenue(start_date, end_date, selected_countries)
    assert isinstance(result, dict), "Output should be a dictionary representing an Altair chart."

@pytest.mark.parametrize("start_date, end_date", [("2010-12-01", "2010-12-31")])
def test_plot_top_countries_pie_chart(start_date, end_date):
    """
    Tests the plot_top_countries_pie_chart function to ensure it returns a valid Altair chart specification.
    """
    result = plot_top_countries_pie_chart(start_date, end_date)
    assert isinstance(result, dict), "Output should be a dictionary representing an Altair chart."

@pytest.mark.parametrize("start_date, end_date, selected_countries", [
    ("2010-12-01", "2010-12-31", ["United Kingdom", "France"]),
    ("2010-12-01", "2010-12-31", ["Malta"])
])
def test_update_cards(start_date, end_date, selected_countries):
    """
    Tests the update_cards function to ensure it returns a tuple containing four elements.
    """
    result = update_cards(start_date, end_date, selected_countries)
    assert isinstance(result, tuple), "Output should be a tuple of four elements."
    assert len(result) == 4, "Tuple should contain four elements."


@pytest.mark.parametrize('start_date, end_date', [('2010-12-01', '2010-12-31')])
def test_compute_other_countries(start_date, end_date):
    store = {}  # Or None, [] depending on expected type
    result = compute_other_countries(start_date, end_date, store)
    assert isinstance(result, list), 'Output should be a list of country names.'

@pytest.mark.parametrize("signalData, expected", [
    ({"selected_country": {"Country": ["Germany"]}}, "Germany"),
    ({"selected_country": {"Country": ["Others"]}}, "Others"),
    ({}, None)
])
def test_store_selected_country(signalData, expected):
    """
    Tests the store_selected_country function to ensure it correctly extracts the selected country.
    """
    result = store_selected_country(signalData)
    assert result == expected, "Selected country should match expected value."

@pytest.mark.parametrize("selected_country, other_countries, dropdown_value, expected", [
    ("Germany", [], [], ["Germany"]),
    ("Others", ["Italy", "Spain"], [], ["Italy", "Spain"]),
    (None, [], ["United Kingdom"], ["United Kingdom"])
])
def test_update_country_dropdown(selected_country, other_countries, dropdown_value, expected):
    """
    Tests the update_country_dropdown function to ensure the dropdown updates correctly based on selection.
    """
    result = update_country_dropdown(selected_country, other_countries, dropdown_value)
    assert result == expected, "Dropdown value should update accordingly."