from math import sqrt


def calculate_metrics(
    actuals: list[float],
    forecasts: list[float],
) -> dict[str, float | int | None]:
    if len(actuals) != len(forecasts):
        raise ValueError("Actuals and forecasts must have equal lengths")

    if not actuals:
        return {
            "periods": 0,
            "mae": None,
            "rmse": None,
            "bias": None,
            "wape": None,
        }

    errors = [
        forecast - actual
        for actual, forecast in zip(actuals, forecasts)
    ]

    absolute_errors = [abs(error) for error in errors]
    squared_errors = [error**2 for error in errors]

    total_actual = sum(abs(actual) for actual in actuals)
    wape = (
        sum(absolute_errors) / total_actual * 100
        if total_actual
        else None
    )

    return {
        "periods": len(errors),
        "mae": sum(absolute_errors) / len(errors),
        "rmse": sqrt(sum(squared_errors) / len(errors)),
        "bias": sum(errors) / len(errors),
        "wape": wape,
    }