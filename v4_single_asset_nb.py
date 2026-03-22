import marimo

__generated_with = "0.21.1"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    from version_4 import (
        calculate_39c_annual_deduction_cap,
        calculate_39c_deferred_depreciation_one_asset,
    )

    return (
        calculate_39c_annual_deduction_cap,
        calculate_39c_deferred_depreciation_one_asset,
        mo,
    )


@app.cell
def _(mo):
    mo.md(
        """
        # Version 4 single-asset results

        This notebook uses the **example usage from picture** at the bottom of
        `version_4.py` and exposes the one-asset helpers for a selected asset.
        """
    )
    return


@app.cell
def _():
    loyers = [10_000, 8_000, 18_000, 4_000]
    charges = [5_000, 6_000, 20_000, 3_000]
    booked_depreciations = [3_000, 9_000, 13_000, 5_000]

    return booked_depreciations, charges, loyers


@app.cell
def _(loyers, mo):
    asset_options = [f"Asset {i + 1}" for i in range(len(loyers))]
    asset_selector = mo.ui.dropdown(
        options=asset_options,
        value=asset_options[0],
        label="Select asset",
    )
    asset_selector
    return (asset_selector,)


@app.cell
def _(
    asset_selector,
    booked_depreciations,
    calculate_39c_annual_deduction_cap,
    calculate_39c_deferred_depreciation_one_asset,
    charges,
    loyers,
):
    i = int(asset_selector.value.split()[-1]) - 1
    accrued_rent = loyers[i]
    related_expenses = charges[i]
    booked_depreciation = booked_depreciations[i]

    annual_deduction_cap = calculate_39c_annual_deduction_cap(
        accrued_rent=accrued_rent,
        related_expenses=related_expenses,
    )
    deferred_depreciation = calculate_39c_deferred_depreciation_one_asset(
        booked_depreciation=booked_depreciation,
        annual_deduction_cap=annual_deduction_cap,
    )

    result = {
        "asset": f"Asset {i + 1}",
        "accrued_rent": accrued_rent,
        "related_expenses": related_expenses,
        "booked_depreciation": booked_depreciation,
        "annual_deduction_cap": annual_deduction_cap,
        "deferred_depreciation": deferred_depreciation,
    }

    return (result,)


@app.cell
def _(mo, result):
    mo.md("## Single-asset result")
    mo.ui.table([result])
    return


if __name__ == "__main__":
    app.run()
