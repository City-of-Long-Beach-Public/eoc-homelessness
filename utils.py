import pandas as pd


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
            if destination_category == "Permanent Housing Situations":
                out = "Positive"
            elif destination_category == "Other":
                out = "Negative"
            elif destination in negative_for_street_and_temp:
                out = "Negative"
            else:
                out = "Positive"

        else:
            if destination_category == "Permanent Housing Situations":
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
    services_set = {
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
    if code in services_set:
        return "Services"


def determine_program(row):
    program_set = {
        "Housing & Shelter Services",
        "Housing/Shelter Services",
        "Shelter Services",
        "Transitional Housing/Shelter",
        "Housing Services",
    }
    out = row["Services Name"] in program_set

    if pd.isna(row["Services Name"]):
        out = True
    return out
