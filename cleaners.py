import pandas as pd
import os

from datetime import timedelta


def clean_race(row):
    out = row["Clients Race"]
    if row["Black, African American, or African"] == "Yes":
        out = "Black, African American, or African"
    if out in {"Client doesn't know", "Client refused", "Data not collected"}:
        out = "Unknown"
    return out


def combine_race_ethnicity(row):
    out = row["Clients Race Cleaned"]

    if (row["Clients Ethnicity"] == "Hispanic/Latin(a)(o)(x)") & (
        out != "Black, African American, or African"
    ):
        out = "Hispanic/Latin(a)(o)(x)"
    return out


def clean_gender(row):
    other_set = {
        "Questioning",
        "Transgender",
        "A gender other than singularly female or male (e.g., non-binary, genderfluid, agender, culturally specific gender)",
    }
    unknown_set = {"Client doesn't know", "Client refused", "Data not collected"}
    out = row["Clients Gender"]
    if out in other_set:
        out = "Other"
    if out in unknown_set:
        out = "Unknown"
    return out


def clean_veteran(row):
    unknown_set = {"Client doesn't know", "Client refused", "Data not collected"}
    out = row["Clients Veteran Status"]
    if (out in unknown_set) | (pd.isna(out)):
        out = "Unknown"
    return out


def hud_performance_outcomes(row):
    # https://files.hudexchange.info/resources/documents/System-Performance-Measure-7-Housing-Destination-Summary.pdf
    exclude_non_street_set = {
        "Foster care home or foster care group home",
        "Long-term care facility or nursing home",
    }
    exclude_if_street_set = {
        "Hospital or other residential non-psychiatric medical facility",
        "Residential project or halfway house with no homeless criteria",
    }
    exclude_in_all_set = {"Deceased"}
    negative_for_street_and_temp = {
        "Place not meant for human habitation",
        "Jail, prison or juvenile detention facility",
    }

    destination = row["Update/Exit Screen Destination"]
    destination_category = row["Update/Exit Screen Destination Category"]
    out = ""

    if destination in exclude_in_all_set:
        out = "Exclude"
    if row["Programs Project Type Code"] == "Street Outreach":
        if destination in exclude_if_street_set:
            out = "Exclude"
    elif destination in exclude_non_street_set:
        out = "Exclude"

    if out != "Exclude":
        if row["Programs Project Type Code"] == "Street Outreach":
            if pd.isna(destination_category):
                out = "Negative"
            elif destination_category == "Permanent Housing Situations":
                out = "Positive"
            elif destination_category == "Other":
                out = "Negative"
            elif destination in negative_for_street_and_temp:
                out = "Negative"
            else:
                out = "Positive"

        else:
            if pd.isna(destination_category):
                out = "Temporary"
            elif destination_category == "Permanent Housing Situations":
                out = "Permanent"
            else:
                out = "Temporary"
    return out


def determine_outcomes(row):
    out = hud_performance_outcomes(row)

    if not pd.isna(row["Housing Move-in Date"]):
        out = "Permanent"
    return out


def bin_type_code(row):
    code = row["Programs Project Type Code"]
    interim_set = {"Emergency Shelter", "Transitional Housing", "Safe Haven"}
    permanent_set = {
        "PH - Rapid Re-Housing",
        "PH - Housing Only",
        "PH - Housing with Services (no disability required for entry)",
        "PH - Permanent Supportive Housing (disability required for entry)",
    }
    support_set = {
        "Street Outreach",
        "Coordinated Entry",
        "Homelessness Prevention",
        "Services Only",
        "Other",
    }

    if code in interim_set:
        return "Interim Housing"
    if code in permanent_set:
        return "Permanent Housing"
    if code in support_set:
        return "Support Services"


def determine_service_event(row):
    program_set = {
        "Housing & Shelter Services",
        "Housing/Shelter Services",
        "Shelter Services",
        "Transitional Housing/Shelter",
        "Housing Services",
    }
    out = row["Services Name"] not in program_set

    if pd.isna(row["Services Name"]):
        out = False
    return out


def clean_destination(row):
    destination = row["Update/Exit Screen Destination"]
    category = row["Update/Exit Screen Destination Category"]

    if pd.isna(destination) & ~pd.isna(row["Enrollments Exit Date Filter Date"]):
        if not pd.isna(row["Housing Move-in Date"]):
            destination = "No exit interview completed"
            category = "Permanent Housing Situations"
        else:
            destination = "No exit interview completed"
            category = "Other"

    if row["Enrollments Exit Date Filter Date"] == pd.to_datetime(
        os.getenv("DATE_UPLOADED")
    ):
        destination = "Enrolled"
        category = "Enrolled"

    category = category.replace(" Situations", "")

    return destination, category

def add_prev_enrollments(row, original_df):

    current_date = row["Enrollments Project Start Date"]
    df = original_df[
        original_df["Clients Unique Identifier"] == row["Clients Unique Identifier"]
    ]

    prev_df = df[df["Enrollments Project Start Date"] < current_date]

    prev_within_year_df = prev_df[
        prev_df["Enrollments Project Start Date"] > (current_date - timedelta(days=365))
    ]

    prev_enrollments = prev_df.groupby(["Enrollment ID"])[
        "Enrollments Project Start Date"
    ].first()

    prev_enrollments_last_year = prev_within_year_df.groupby(["Enrollment ID"])[
        "Enrollments Project Start Date"
    ].first()
    if prev_enrollments.empty:
        prev_enrollments_counts = 0
        days_last_enroll = None
        days_first_enroll = None

    else:
        prev_enrollments_counts = prev_enrollments.size
        days_last_enroll = (current_date - prev_enrollments.max()).days
        days_first_enroll = (current_date - prev_enrollments.min()).days

    if prev_enrollments_last_year.empty:
        prev_enrollments_last_year_counts = 0
        days_first_enroll_last_year = None
    else:
        prev_enrollments_last_year_counts = prev_enrollments_last_year.size
        days_first_enroll_last_year = (
            current_date - prev_enrollments_last_year.min()
        ).days

    return (
        prev_enrollments_counts,
        prev_enrollments_last_year_counts,
        days_last_enroll,
        days_first_enroll,
        days_first_enroll_last_year,
    )
