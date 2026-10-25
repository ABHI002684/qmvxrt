import pytest

from app.services.metrics import calculate_metrics


def test_calculates_forecast_metrics():
    result = calculate_metrics(
        actuals=[100.0, 200.0, 300.0],
        forecasts=[110.0, 180.0, 330.0],
    )

    assert result["periods"] == 3
    assert result["mae"] == pytest.approx(20.0)
    assert result["rmse"] == pytest.approx((1400 / 3) ** 0.5)
    assert result["bias"] == pytest.approx(20 / 3)
    assert result["wape"] == pytest.approx(10.0)


def test_empty_data_returns_empty_metrics():
    result = calculate_metrics([], [])

    assert result["periods"] == 0
    assert result["mae"] is None
    assert result["wape"] is None


def test_mismatched_lengths_raise_error():
    with pytest.raises(ValueError):
        calculate_metrics([100.0], [90.0, 95.0])
