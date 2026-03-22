"""Exploratory article 39 C helpers for the current ``v4`` branch.

The wording in this module is anchored to ``v4/sources.md``.

Current decisions reflected here:

- default yearly booked amount follows article 39 C(I):
  "réparti sur la durée normale d'utilisation";
- the one-asset cap for the natural-person branch follows article 39 C(II.2):
  deduction is limited by "le montant du loyer acquis ... diminué du montant
  des autres charges afférentes";
- the multi-asset cap follows the current BOFiP:
  "C'est l'ensemble des loyers et des charges ... qu'il convient de comparer";
- asset-level allocation is still exploratory, so the literal-reading helpers
  stay separate from the interpreted allocation path.

Assumptions for the current prototype:

- France / article 39 C natural-person branch;
- real-estate-oriented inputs;
- amortizable amount is already net of non-amortizable land.
"""

# use temporary Money type for now, to be replaced with actual Money type later
Money = float

######################
# #### One Asset ####
######################


# 39c default amortization
def calculate_39c_booked_depreciation(amortizable_amount: float, normal_use_duration: int):
    """Return the default yearly booked amount under article 39 C(I).

    Source phrase in ``sources.md``:
    "L'amortissement des biens ... est réparti sur la durée normale
    d'utilisation".

    Current decision: for the default branch, the annual booked amount is
    modeled as straight-line amortization over the normal use duration.
    """
    return amortizable_amount / normal_use_duration


def calculate_39c_annual_deduction_cap(
    accrued_rent: float,  
    related_expenses: float,  
):
    """Return the one-asset article 39 C yearly deduction cap.

    Source phrasing in ``sources.md``:
    - CGI II.2: "dans la limite du montant du loyer acquis ... diminue du
      montant des autres charges afferentes"
    - BOFiP: "l'amortissement sera deductible dans la limite de la difference
      entre les loyers acquis ... et les charges afferentes"

    Current decision: the cap is the positive rent-minus-charges amount, so
    this helper returns ``max(0, accrued_rent - related_expenses)``.
    """
    return max(0, accrued_rent - related_expenses)


def calculate_39c_deferred_depreciation_one_asset(
    booked_depreciation: float, annual_deduction_cap: float
):
    """Return the current-year amount rejected by the article 39 C cap.

    Source phrasing in ``sources.md``:
    - CGI II.3: "L'amortissement regulierement comptabilise ... et non
      deductible ... peut etre deduit du resultat des exercices suivants"
    - BOFiP example: "La fraction de l'annuite d'amortissement ecartee ...
      sera susceptible d'etre deduite des resultats des exercices suivants"

    Current decision: despite the provisional helper name, this computes the
    same-year nondeducted amount, not the later carryforward stock workflow.
    """
    return max(0, booked_depreciation - annual_deduction_cap)


# Numeric example (single asset, no code execution):
# - booked depreciation = 18_000 / 5 = 3_600
# - annual deduction cap = max(0, 2_500 - 1_000) = 1_500
# - allocation base = 2_500 - 1_000 = 1_500
# - deferred depreciation (with this module's current literal logic) =
#   max(0, 3_600 - 1_500) = 2_100
#
# Note:
# The BOFiP example also applies a separate article 39 limitation before the
# 39 C comparison. This module does not model that layer here.


# #### Multiple Assets ####

def calculate_39c_annual_deduction_cap_multiasset(
    total_accrued_rent: float,
    total_related_expenses: float,
):
    """Return the pool-level cap for the current multi-asset reading.

    Source phrasing in ``sources.md``:
    "Il n'y a pas lieu d'appliquer cette limite en considerant isolement chacun
    de ces biens. C'est l'ensemble des loyers et des charges ... qu'il convient
    de comparer".

    Current decision: compare global rents and global charges first, then floor
    the result at zero.
    """
    return max(0, total_accrued_rent - total_related_expenses)


def calculate_total_accrued_rent(accrued_rents: list[float]):
    """Sum the accrued rents used in the pool-level BOFiP comparison.

    This is a mechanical helper for the source phrase
    "l'ensemble des loyers".
    """
    return sum(accrued_rents)


def calculate_total_related_expenses(related_expenses: list[float]):
    """Sum the related expenses used in the pool-level BOFiP comparison.

    This is a mechanical helper for the source phrase
    "l'ensemble ... des charges afferents aux biens loues".
    """
    return sum(related_expenses)


def calculate_total_booked_depreciation(booked_depreciations: list[float]):
    """Sum the booked amounts before applying the pool-level limitation.

    This helper exists because the BOFiP compares the deductible cap against
    the annuity/depreciation charge for the asset pool as a whole.
    """
    return sum(booked_depreciations)

# Numeric example (multiple assets literal, no code execution):
# - accrued rents = [10_000, 8_000, 18_000, 4_000]
# - related expenses = [5_000, 6_000, 20_000, 3_000]
# - booked depreciations = [3_000, 9_000, 13_000, 5_000]
# - total accrued rent = 40_000
# - total related expenses = 34_000
# - total booked depreciation = 30_000
# - annual deduction cap across all assets = max(0, 40_000 - 34_000) = 6_000


# hr
# - total deffered depreciation ?? or base or ??
# - in the example the deferred pool is 24k 
#   - under the reading of overrun, the total overrun is 26k in the denominator.  

# #### Literal Allocation ####

def select_eligible_assets():
    """Select the assets concerned by the proportional split.

    Source phrasing in ``sources.md``:
    "entre les biens pour lesquels la charge d'amortissement excede la
    difference entre le loyer acquis et les autres charges".

    Current decision: the concerned assets are the ones where booked
    depreciation exceeds ``accrued_rent - related_expenses``.
    """
    pass
# in this example 2, 3 and 4


# 6k can be deducted, 24k is deferred.
# which excedent du loyer acquis?
def literal_allocation():
    """Placeholder for the literal BOFiP allocation reading.

    Source phrasing in ``sources.md``:
    "Cette repartition s'opere en retenant pour chacun des biens concernes, au
    numerateur, l'excedent du loyer acquis sur les autres charges ... et, au
    denominateur, la somme de tous les excedents."

    Current decision: keep this literal-reading path explicit and separate,
    because it becomes awkward when an asset has a negative rent-minus-charges
    spread.
    """
    pass

def numerator_version_one(asset_accrued_rent: float, asset_related_expenses: float):
    """Return the literal per-asset numerator from the current BOFiP wording.

    This helper follows the phrase
    "au numerateur, l'excedent du loyer acquis sur les autres charges".

    Current decision: the literal numerator is the positive rent-minus-charges
    spread for one asset.
    """
    return max(0, asset_accrued_rent - asset_related_expenses)

def denominator_version_one(eligible_assets: list[dict]):
    """Sum literal numerators across pre-filtered concerned assets.

    This helper follows the phrase
    "au denominateur, la somme de tous les excedents" after the caller has
    already restricted the set to concerned assets.
    """
    return sum(
        max(0, asset['accrued_rent'] - asset['related_expenses'])
        for asset in eligible_assets
    )
def denominator_version_two(all_assets: list[dict]):
    """Sum literal numerators across all assets without pre-filtering.

    This exists to compare two readings of the BOFiP sentence about
    "la somme de tous les excedents": sum only the concerned assets or sum the
    whole asset set and rely on ``max(0, ...)`` to zero out the others.
    """
    return sum(
        max(0, asset['accrued_rent'] - asset['related_expenses'])
        for asset in all_assets
    )
# #### Interpreted Allocation ####

# Intentionally left empty for now.


"""
example usage from picture (not official) :
loyers = [10000, 8000, 18000, 4000]
charges = [5000, 6000, 20000, 3000]
booked_depreciations = [3000, 9000, 13000, 5000]

excedent ainsi defini per asset ->  charge d'amortissement - (loyer acquis - charge afférente) 
"""
