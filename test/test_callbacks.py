import pytest
import pandas as pd
import altair as alt
from datetime import datetime
from unittest.mock import patch

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


# Sample mock data
mock_data = pd.DataFrame({
    "InvoiceNo": [536365, 536365, 536365, 536365, 536365, 536366, 536366, 536367, 536367, 536368],
    "StockCode": ["85123A", "71053", "84406B", "84029G", "84029E", "22752", "21730", "22633", "22556", "22557"],
    "Description": [
        "WHITE HANGING HEART T-LIGHT HOLDER", "WHITE METAL LANTERN",
        "CREAM CUPID HEARTS COAT HANGER", "KNITTED UNION FLAG HOT WATER BOTTLE",
        "RED WOOLLY HOTTIE WHITE HEART.", "SET 7 BABUSHKA NESTING BOXES",
        "GLASS STAR FROSTED T-LIGHT HOLDER", "HAND WARMER UNION JACK",
        "PLUSH PANDA SOFT TOY", "LUNCH BAG RED RETROSPOT"
    ],
    "Quantity": [6, 6, 8, 6, 6, 2, 6, 6, 3, -1],  # Negative quantity represents a refund
    "InvoiceDate": pd.to_datetime([
        "2024-01-01", "2024-01-01", "2024-01-01", "2024-01-01", "2024-01-01",
        "2024-02-15", "2024-02-15", "2024-03-01", "2024-03-01", "2024-03-15"
    ]),
    "UnitPrice": [2.55, 3.39, 2.75, 3.39, 3.39, 7.65, 4.25, 1.85, 5.99, 7.99],
    "CustomerID": [17850.0, 17850.0, 17850.0, 17850.0, 17850.0, 13047.0, 13047.0, 12583.0, 12583.0, 13587.0],
    "Country": ["Germany", "France", "Germany", "France", "Germany", "Spain", "Spain", "Italy", "Italy", "United Kingdom"],
    "Revenue": [15.30, 20.34, 22.00, 20.34, 20.34, 15.30, 25.50, 11.10, 17.97, -7.99],  # Refund for UK transaction
    "MonthYear": ["Jan-2024", "Jan-2024", "Jan-2024", "Jan-2024", "Jan-2024", "Feb-2024", "Feb-2024", "Mar-2024", "Mar-2024", "Mar-2024"]
})

@pytest.fixture
def setup_mock_data():
    """Fixture to patch the global df variable with mock data."""
    with patch("src.callbacks.df", mock_data):
        yield



def test_plot_monthly_revenue_chart(setup_mock_data):
    """Test that the function generates a valid Altair chart specification."""
    
    start_date = "2024-01-01"
    end_date = "2024-03-31"
    selected_countries = ["Germany", "France", "Spain", "Italy"]

    # Call the function
    chart_spec = plot_monthly_revenue_chart(start_date, end_date, selected_countries)

    # Ensure the function returns a dictionary
    assert isinstance(chart_spec, dict), "The output should be a dictionary."

    # Ensure required keys exist in the chart spec
    assert "encoding" in chart_spec, "Chart spec should contain 'encoding'."
    assert "mark" in chart_spec, "Chart spec should contain 'mark'."
    assert "data" in chart_spec, "Chart spec should contain 'data'."
    assert "datasets" in chart_spec, "Chart spec should contain 'datasets'."

    # Extract dataset name
    dataset_name = chart_spec["data"]["name"]
    assert dataset_name in chart_spec["datasets"], f"Dataset '{dataset_name}' should exist in 'datasets'."

    # Retrieve the dataset from the chart spec
    chart_data = pd.DataFrame(chart_spec["datasets"][dataset_name])

    # Validate that the dataset contains expected months
    expected_months = {"Jan-2024", "Feb-2024", "Mar-2024"}
    assert expected_months.issubset(set(chart_data["MonthYear"])), "Chart data should include expected months."

    # Compute expected revenue per month
    expected_revenue = (
        mock_data[mock_data["Country"].isin(selected_countries)]
        .groupby("MonthYear")["Revenue"]
        .sum()
        .reset_index()
    )

    # Validate computed revenue values in the dataset
    for _, row in expected_revenue.iterrows():
        month = row["MonthYear"]
        expected_value = row["Revenue"]

        # Find the corresponding value in chart data
        chart_value = chart_data.loc[chart_data["MonthYear"] == month, "Revenue"].values[0]

        assert chart_value == expected_value, f"Expected {expected_value} for {month}, but got {chart_value}"

    # Ensure tooltip contains expected fields
    assert "tooltip" in chart_spec["encoding"], "Chart should include tooltips."
    assert any(t["field"] == "MonthYear" for t in chart_spec["encoding"]["tooltip"]), "Tooltip should contain 'MonthYear'."
    assert any(t["field"] == "Revenue" for t in chart_spec["encoding"]["tooltip"]), "Tooltip should contain 'Revenue'."


def test_plot_stacked_chart(setup_mock_data):
    """Test that the function generates a valid Altair chart specification."""
    
    start_date = "2024-01-01"
    end_date = "2024-03-31"
    selected_countries = ["Germany", "France", "Spain", "Italy"]

    # Call the function
    chart_spec = plot_stacked_chart(start_date, end_date, selected_countries)

    # Ensure the function returns a dictionary
    assert isinstance(chart_spec, dict), "The output should be a dictionary."

    # Ensure required keys exist in the chart spec
    assert "encoding" in chart_spec, "Chart spec should contain 'encoding'."
    assert "mark" in chart_spec, "Chart spec should contain 'mark'."
    assert "data" in chart_spec, "Chart spec should contain 'data'."
    assert "datasets" in chart_spec, "Chart spec should contain 'datasets'."

    # Extract dataset name
    dataset_name = chart_spec["data"]["name"]
    assert dataset_name in chart_spec["datasets"], f"Dataset '{dataset_name}' should exist in 'datasets'."

    # Retrieve the dataset from the chart spec
    chart_data = pd.DataFrame(chart_spec["datasets"][dataset_name])

    # Validate that the dataset contains expected revenue components
    expected_components = {"Net Revenue", "Refunds"}
    assert expected_components.issubset(set(chart_data["Component"])), "Chart data should include expected components."

    # Compute expected revenue values
    gross_revenue = mock_data[mock_data["Country"].isin(selected_countries) & (mock_data["Quantity"] > 0)]["Revenue"].sum()
    refunds = abs(mock_data[mock_data["Country"].isin(selected_countries) & (mock_data["Quantity"] < 0)]["Revenue"].sum())
    net_revenue = gross_revenue - refunds  # Net Revenue = Gross Revenue - Refunds

    # Validate computed values in the dataset
    net_revenue_chart_value = chart_data.loc[chart_data["Component"] == "Net Revenue", "Value"].values[0]
    refunds_chart_value = chart_data.loc[chart_data["Component"] == "Refunds", "Value"].values[0]

    assert net_revenue_chart_value == net_revenue, f"Expected Net Revenue: {net_revenue}, Got: {net_revenue_chart_value}"
    assert refunds_chart_value == refunds, f"Expected Refunds: {refunds}, Got: {refunds_chart_value}"

    # Ensure tooltip contains expected fields
    assert "tooltip" in chart_spec["encoding"], "Chart should include tooltips."
    assert any(t["field"] == "Component" for t in chart_spec["encoding"]["tooltip"]), "Tooltip should contain 'Component'."
    assert any(t["field"] == "Value" for t in chart_spec["encoding"]["tooltip"]), "Tooltip should contain 'Value'."


def test_plot_top_products_revenue(setup_mock_data):
    """Test that the function generates a valid Altair chart specification."""
    
    start_date = "2024-01-01"
    end_date = "2024-03-31"
    selected_countries = ["Germany", "France", "Spain", "Italy"]
    n_products = 5

    # Call the function
    chart_spec = plot_top_products_revenue(start_date, end_date, selected_countries, n_products)

    # Ensure the function returns a dictionary
    assert isinstance(chart_spec, dict), "The output should be a dictionary."

    # Ensure required keys exist in the chart spec
    assert "encoding" in chart_spec, "Chart spec should contain 'encoding'."
    assert "mark" in chart_spec, "Chart spec should contain 'mark'."
    assert "data" in chart_spec, "Chart spec should contain 'data'."
    assert "datasets" in chart_spec, "Chart spec should contain 'datasets'."

    # Extract dataset name
    dataset_name = chart_spec["data"]["name"]
    assert dataset_name in chart_spec["datasets"], f"Dataset '{dataset_name}' should exist in 'datasets'."

    # Retrieve the dataset from the chart spec
    chart_data = pd.DataFrame(chart_spec["datasets"][dataset_name])

    # Compute expected top products by revenue
    expected_revenue = (
        mock_data[mock_data["Country"].isin(selected_countries)]
        .groupby("Description")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(n_products)
        .reset_index()
    )

    # Validate that the dataset contains expected products
    expected_products = set(expected_revenue["Description"])
    assert expected_products.issubset(set(chart_data["Description"])), "Chart data should include expected top products."

    # Validate computed revenue values in the dataset
    for _, row in expected_revenue.iterrows():
        product = row["Description"]
        expected_value = row["Revenue"]

        # Find the corresponding value in chart data
        chart_value = chart_data.loc[chart_data["Description"] == product, "Revenue"].values[0]

        assert chart_value == expected_value, f"Expected {expected_value} for '{product}', but got {chart_value}"

    # Ensure tooltip contains expected fields
    assert "tooltip" in chart_spec["encoding"], "Chart should include tooltips."
    assert any(t["field"] == "Description" for t in chart_spec["encoding"]["tooltip"]), "Tooltip should contain 'Description'."
    assert any(t["field"] == "Revenue" for t in chart_spec["encoding"]["tooltip"]), "Tooltip should contain 'Revenue'."


def test_plot_top_countries_pie_chart(setup_mock_data):
    """Test that the function generates a valid Altair pie chart specification."""
    
    start_date = "2024-01-01"
    end_date = "2024-03-31"

    # Call the function
    chart_spec = plot_top_countries_pie_chart(start_date, end_date)

    # Ensure the function returns a dictionary
    assert isinstance(chart_spec, dict), "The output should be a dictionary."

    # Ensure 'layer' exists since this is a layered chart
    assert "layer" in chart_spec, "Chart spec should contain 'layer'."
    assert isinstance(chart_spec["layer"], list), "Chart 'layer' should be a list."

    # Extract the first layer where encoding should be present
    first_layer = chart_spec["layer"][0]

    # Ensure required keys exist in the first layer
    assert "encoding" in first_layer, "First layer should contain 'encoding'."

    # Ensure tooltip is correctly set
    encoding = first_layer["encoding"]
    assert "tooltip" in encoding, "Encoding should contain 'tooltip'."
    assert any(t["field"] == "Country" for t in encoding["tooltip"]), "Tooltip should contain 'Country'."
    assert any(t["field"] == "Percentage" for t in encoding["tooltip"]), "Tooltip should contain 'Percentage'."

    # Extract dataset name
    dataset_name = chart_spec["data"]["name"]
    assert dataset_name in chart_spec["datasets"], f"Dataset '{dataset_name}' should exist in 'datasets'."



def test_update_cards(setup_mock_data):
    """Test that the function correctly computes financial metrics for the dashboard cards."""
    
    start_date = "2024-01-01"
    end_date = "2024-03-31"
    selected_countries = ["Germany", "France", "Spain", "Italy"]

    # Call the function
    result = update_cards(start_date, end_date, selected_countries)

    # Ensure the function returns a tuple with 4 elements
    assert isinstance(result, tuple), "Output should be a tuple."
    assert len(result) == 4, "Tuple should contain four elements."

    # Extract card values from result
    card_loyal_customer_ratio, card_loyal_customer_sales, card_net_sales, card_total_returns = result

    # Compute expected values
    filtered_df = mock_data[
        (mock_data["InvoiceDate"] >= pd.to_datetime(start_date)) &
        (mock_data["InvoiceDate"] <= pd.to_datetime(end_date)) &
        (mock_data["Country"].isin(selected_countries))
    ]

    # Compute Loyal Customer Ratio
    loyal_customers = filtered_df["CustomerID"].nunique()
    non_loyal_customers = filtered_df[filtered_df["CustomerID"].isna()]["InvoiceNo"].nunique()
    total_unique_customers = loyal_customers + non_loyal_customers
    expected_loyal_customer_ratio = (loyal_customers / total_unique_customers * 100) if total_unique_customers else 0

    # Compute Loyal Customer Sales
    loyal_customer_sales = filtered_df[filtered_df["CustomerID"].notna()]["Revenue"].sum()

    # Compute Net Sales
    net_sales = filtered_df["Revenue"].sum()

    # Compute Total Returns
    total_returns = abs(filtered_df[filtered_df["Revenue"] < 0]["Revenue"].sum())

    # Extract displayed values from Dash components
    assert isinstance(card_loyal_customer_ratio, list), "Loyal customer ratio card should be a list."
    assert isinstance(card_loyal_customer_sales, list), "Loyal customer sales card should be a list."
    assert isinstance(card_net_sales, list), "Net sales card should be a list."
    assert isinstance(card_total_returns, list), "Total returns card should be a list."

    # Validate Loyal Customer Ratio
    displayed_loyal_ratio = float(card_loyal_customer_ratio[1].children.children.replace("%", ""))
    assert displayed_loyal_ratio == round(expected_loyal_customer_ratio, 2), f"Expected {expected_loyal_customer_ratio}% loyal customers, but got {displayed_loyal_ratio}%."

    # Validate Loyal Customer Sales
    displayed_loyal_sales = float(card_loyal_customer_sales[1].children.children.replace("£", "").replace(",", ""))
    assert displayed_loyal_sales == round(loyal_customer_sales, 2), f"Expected £{loyal_customer_sales}, but got £{displayed_loyal_sales}."

    # Validate Net Sales
    displayed_net_sales = float(card_net_sales[1].children.children.replace("£", "").replace(",", ""))
    assert displayed_net_sales == round(net_sales, 2), f"Expected £{net_sales}, but got £{displayed_net_sales}."

    # Validate Total Returns
    displayed_total_returns = float(card_total_returns[1].children.children.replace("-£", "").replace(",", ""))
    assert displayed_total_returns == round(total_returns, 2), f"Expected £{total_returns} in total returns, but got £{displayed_total_returns}."

def test_update_cards_no_customers(setup_mock_data):
    """Test when there are no transactions, ensuring the loyal customer ratio is 0%."""
    
    start_date = "2025-01-01"
    end_date = "2025-01-31"
    selected_countries = ["Germany", "France", "Spain", "Italy"]

    # Call the function
    result = update_cards(start_date, end_date, selected_countries)

    # Extract card values from result
    card_loyal_customer_ratio, _, _, _ = result

    # Extract displayed value from Dash component
    displayed_loyal_ratio = float(card_loyal_customer_ratio[1].children.children.replace("%", ""))

    # Validate Loyal Customer Ratio is 0%
    assert displayed_loyal_ratio == 0, f"Expected 0% loyal customers, but got {displayed_loyal_ratio}%"



def test_compute_other_countries(setup_mock_data):
    """Test that the function correctly computes the list of 'Other' countries."""
    
    start_date = "2024-01-01"
    end_date = "2024-03-31"
    store = None  # The stored value isn't used in the computation

    # Call the function
    other_countries = compute_other_countries(start_date, end_date, store)

    # Ensure the function returns a list
    assert isinstance(other_countries, list), "The output should be a list."

    # Ensure the United Kingdom is excluded
    assert "United Kingdom" not in other_countries, "United Kingdom should not be in the 'Others' category."

    # Compute expected countries sorted by frequency
    country_counts = (
        mock_data[mock_data["Country"] != "United Kingdom"]
        .groupby("Country")
        .size()
        .reset_index(name="Count")
        .sort_values(by="Count", ascending=False)
    )

    # Extract the bottom-ranked countries beyond the top 5
    expected_other_countries = country_counts.iloc[5:]["Country"].tolist()

    # Validate computed "Others" countries
    assert set(other_countries) == set(expected_other_countries), f"Expected {expected_other_countries}, but got {other_countries}"

def test_compute_other_countries_with_few_countries(setup_mock_data):
    """Test case when there are fewer than 5 countries (all should be included in 'Others')."""

    start_date = "2024-02-01"
    end_date = "2024-02-28"
    store = None

    # Call the function
    other_countries = compute_other_countries(start_date, end_date, store)

    # Compute expected countries (excluding UK)
    filtered_df = mock_data[
        (mock_data["InvoiceDate"] >= pd.to_datetime(start_date)) &
        (mock_data["InvoiceDate"] <= pd.to_datetime(end_date)) &
        (mock_data["Country"] != "United Kingdom")
    ]

    # Count transactions per country and rank them
    country_counts = (
        filtered_df["Country"]
        .value_counts()
        .reset_index()
        .rename(columns={"index": "Country", "Country": "Count"})
    )

    # Select countries that rank below the top 5
    if len(country_counts) > 5:
        expected_other_countries = country_counts.iloc[5:]["Country"].tolist()
    else:
        expected_other_countries = []  # If there are <=5 countries, there should be no "Others"

    # Ensure the function includes only the countries outside the top 5
    assert set(other_countries) == set(expected_other_countries), f"Expected {expected_other_countries}, but got {other_countries}"

def test_compute_other_countries_with_no_data(setup_mock_data):
    """Test case when no data falls within the selected date range."""

    start_date = "2025-01-01"
    end_date = "2025-01-31"
    store = None

    # Call the function
    other_countries = compute_other_countries(start_date, end_date, store)

    # Expect an empty list
    assert other_countries == [], "Expected an empty list when no data is available."



def test_store_selected_country_valid_selection():
    """Test function when a valid country is selected."""
    signal_data = {
        "selected_country": {
            "Country": ["France"]
        }
    }
    result = store_selected_country(signal_data)
    assert result == "France", f"Expected 'France', but got {result}"

def test_store_selected_country_others_selection():
    """Test function when 'Others' is selected."""
    signal_data = {
        "selected_country": {
            "Country": ["Others"]
        }
    }
    result = store_selected_country(signal_data)
    assert result == "Others", f"Expected 'Others', but got {result}"

def test_store_selected_country_no_selection():
    """Test function when no selection is made (None input)."""
    signal_data = None
    result = store_selected_country(signal_data)
    assert result is None, f"Expected None, but got {result}"

def test_store_selected_country_empty_dict():
    """Test function when an empty dictionary is provided."""
    signal_data = {}
    result = store_selected_country(signal_data)
    assert result is None, f"Expected None, but got {result}"

def test_store_selected_country_missing_country_key():
    """Test function when 'selected_country' key is missing in signalData."""
    signal_data = {
        "wrong_key": {
            "Country": ["Germany"]
        }
    }
    result = store_selected_country(signal_data)
    assert result is None, f"Expected None, but got {result}"

def test_store_selected_country_non_list_country():
    """Test function when 'Country' value is not a list."""
    signal_data = {
        "selected_country": {
            "Country": "Spain"
        }
    }
    result = store_selected_country(signal_data)
    assert result is None, f"Expected None, but got {result}"

def test_store_selected_country_empty_country_list():
    """Test function when 'Country' key contains an empty list."""
    signal_data = {
        "selected_country": {
            "Country": ""
        }
    }
    result = store_selected_country(signal_data)
    assert result is None, f"Expected None, but got {result}"

def test_store_selected_country_multiple_countries():
    """Test function when multiple countries are in the selection."""
    signal_data = {
        "selected_country": {
            "Country": ["Germany", "France"]
        }
    }
    result = store_selected_country(signal_data)
    assert result == "Germany", f"Expected 'Germany' (first country), but got {result}"

def test_store_selected_country_invalid_format():
    """Test function when signalData has unexpected structure."""
    signal_data = {
        "selected_country": {
            "Countries": ["France"]  # Incorrect key name
        }
    }
    result = store_selected_country(signal_data)
    assert result is None, f"Expected None due to invalid structure, but got {result}"

@pytest.fixture
def mock_other_countries():
    """Mock a list of 'Others' countries for testing."""
    return ["Portugal", "Sweden", "Belgium"]

@pytest.fixture
def mock_dropdown_value():
    """Mock the current dropdown value before updating."""
    return ["France"]

def test_update_country_dropdown_valid_country(mock_other_countries, mock_dropdown_value):
    """Test when a valid country is selected from the pie chart."""
    selected_country = "Germany"
    result = update_country_dropdown(selected_country, mock_other_countries, mock_dropdown_value)
    assert result == ["Germany"], f"Expected ['Germany'], but got {result}"

def test_update_country_dropdown_others_selected(mock_other_countries, mock_dropdown_value):
    """Test when 'Others' is selected."""
    selected_country = "Others"
    result = update_country_dropdown(selected_country, mock_other_countries, mock_dropdown_value)
    assert result == mock_other_countries, f"Expected {mock_other_countries}, but got {result}"

def test_update_country_dropdown_none_selected(mock_other_countries, mock_dropdown_value):
    """Test when no country is selected (None)."""
    selected_country = None
    result = update_country_dropdown(selected_country, mock_other_countries, mock_dropdown_value)
    assert result == mock_dropdown_value, f"Expected {mock_dropdown_value}, but got {result}"

def test_update_country_dropdown_empty_other_countries(mock_dropdown_value):
    """Test when 'Others' is selected but no countries are available."""
    selected_country = "Others"
    result = update_country_dropdown(selected_country, [], mock_dropdown_value)
    assert result == [], "Expected an empty list when 'Others' has no countries."
