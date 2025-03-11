import pytest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.components import card_loyal_customer_ratio, card_loyal_customer_sales

def test_components_exist():
    assert card_loyal_customer_ratio is not None
    assert card_loyal_customer_sales is not None