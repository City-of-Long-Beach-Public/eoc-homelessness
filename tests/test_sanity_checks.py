import pytest

import os
import pandas as pd
import json

data_file = "./data/enrollees_extract.csv"

requirements_filepath = os.path.abspath("./data/enrollees_extract_requirements.json")
with open(requirements_filepath, "r") as requirements_file:
    requirements = json.load(requirements_file)

filepath = os.path.abspath(data_file)

df = pd.read_csv(
    filepath,
    dtype=requirements["types"],
    parse_dates=requirements["date_columns"],
    engine="python",
)


# df.info()
def test_codes_all_categorized():
    assert (df["Programs Project Type Category"].notna()).all()


def test_no_safe_haven():
    safe_haven = df[df["Programs Project Type Category"] == "Safe Haven"]
    assert safe_haven.empty


afro_latino = df.query(
    "`Clients Ethnicity` == 'Hispanic/Latin(a)(o)(x)' & `Clients Race` == 'Black, African American, or African'"
)

white_latino = df.query(
    "`Clients Ethnicity` == 'Hispanic/Latin(a)(o)(x)' & `Clients Race` == 'White'"
)


class TestRaceEthnicity:
    def test_make_sure_black_precedence(self):
        assert (
            afro_latino["Clients Race / Ethnicity"]
            == "Black, African American, or African"
        ).all()
        assert (
            afro_latino["Clients Race Cleaned"] == "Black, African American, or African"
        ).all()

    def test_make_sure_hispanic_precedence(self):
        assert (
            white_latino["Clients Race / Ethnicity"] == "Hispanic/Latin(a)(o)(x)"
        ).all()
        assert (white_latino["Clients Race Cleaned"] == "White").all()


def test_gender_cleaned():
    values = pd.unique(df["Clients Gender Cleaned"])
    assert len(values) == 3
    assert "Male" in values
    assert "Female" in values
    assert "Other" in values


def test_veteran_cleaned():
    values = pd.unique(df["Clients Veteran Status Cleaned"])
    assert len(values) == 2
    assert "Yes" in values
    assert "No" in values


excluded_permanent_df = df.query(
    "`Update/Exit Screen Destination` == 'Long-term care facility or nursing home' & `Programs Project Type Category` == 'Permanent Housing'"
)


class TestProgramOutcome:
    def test_values(self):
        values = pd.unique(df["Program Outcome"])
        assert len(values) == 5
        assert "Positive" in values
        assert "Negative" in values
        assert "Permanent" in values
        assert "Temporary" in values
        assert "Exclude" in values

    def test_exclude(self):
        assert (excluded_permanent_df["Program Outcome"] == "Exclude").all()


def test_is_service_event():
    assert df["is Service Event"].dtype.name == "boolean"


class TestDestination:
    def test_enroll_exists(self):
        assert "Enrolled" in pd.unique(df["Destination Cleaned"])
        assert "Enrolled" in pd.unique(df["Destination Category Cleaned"])

    def test_no_nulls(self):
        assert (~pd.isna(df["Destination Cleaned"])).all()
        assert (~pd.isna(df["Destination Category Cleaned"])).all()


moved_in_df = df[~pd.isna(df["Housing Move-in Date"])]


class TestMoveIn:
    def test_has_destination_if_no_exit(self):
        no_dest_df = moved_in_df[
            ~pd.isna(moved_in_df["Update/Exit Screen Destination"])
        ]
        assert (
            no_dest_df["Destination Cleaned"] == "No Exit interview completed"
        ).all()
        assert (no_dest_df["Destination Category Cleaned"] == "Permanent Housing").all()

    def test_outcome(self):
        assert (moved_in_df["Program Outcome"] == "Permanent").all()


class TestPrevEnrollments:
    def test_last_year_calc_is_capped(self):
        assert df["Days since first Enrollment (Last Year)"].max() < 366

    def test_enrollments_last_year_is_less(self):
        diff_in_enrolls = (
            df["Number of Previous Enrollments"]
            - df["Number of Previous Enrollments (Last Year)"]
        )
        assert len(pd.unique(diff_in_enrolls)) > 0
