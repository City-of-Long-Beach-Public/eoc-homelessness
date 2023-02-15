# City of Long Beach Addressing Homelessness Data Dictionary
This document defines the data and formulas used to power the City of Long Beach homelessness dashboard hosted at [insert link here](https://longbeach.gov "insert link here"). 

## Definitions
|  Acronym | Definition  |
| ------------ | ------------ |
| HMIS  | Homeless Management Information System  |
| DHHS  | [Department of Health and Human Services](https://www.longbeach.gov/health/) |
| Program  | Most efforts and activities of DHHS such as homeless outreach, case management, providing shelter or permanent housing happens in the context of a "Program". In order to provide our unhoused community members with services such as financial assistance, referrals or housing, the staff enrolls the individual in one or more programs as needed. A person can be enrolled in one or more programs at different point in times. Individuals also "exit programs" either with successful outcomes such as finding subsidized housing or in some cases to undesirable situations such as back to homelessness |
| Interim Housing  |  Provides immediate assistance to an unhoused individual at a City or partner-run shelter. Learn more about [interim housing in Long Beach](https://www.longbeach.gov/homelessness/homeless-services/#shelterbeds "interim housing in Long Beach").  The HUD project codes that are "Emergency Shelter", "Transitional Housing", "Safe Haven". |
| Permanent Housing | The goal of permanent housing is to provide safe and stable housing for those living in or in danger of falling into unsheltered homelessness.  Learn more about [permanent housing in Long Beach](https://www.longbeach.gov/homelessness/homeless-services/#permhousing). The HUD project codes used are "PH - Rapid Re-Housing", "PH - Permanent Supportive Housing (disability required for entry", "PH - Housing with Services (no disability required for entry)", "PH - Housing Only". |
| Street Outreach Services | Teams of employees that proactively engage people experiencing homelessness [Street Outreach](https://www.longbeach.gov/homelessness/homeless-services/#outreach)
| Point in time (PIT) Count | A community survey of the number of people experiencing homelessness. It is taken every year in the winter. Learn more about [Point in Time Count](https://www.longbeach.gov/homelessness/annual-homeless-count/). |
| Street Outreach Services | Teams of employees that proactively engage people experiencing homelessness [Street Outreach](https://www.longbeach.gov/homelessness/homeless-services/#outreach)



## Data Dictionary

|  Metric | Description  | Calculation Method  | Source  |
| ------------ | ------------ | ------------ | ------------ |
| **People Served**  | Number of individuals enrolled in the program.  | Distinct sum of all clients based on unique client number  | Long Beach HMIS  |
| **Number of Services**  | Total number of instances of some form of service provided to an individual. One individual may receive many services, this metric serves as the sum of all services for all people  | Sum of all services provided to all program participants  | Long Beach HMIS  |
| **People Found Permanent Housing or Program Outcome**  | An enrollment that ends with an individual in a more positive situation  | Individuals who exit the program are given an exit survey to show where they are heading to. This is translated to positive or negative outcomes by HUDs [performance metric guidance](https://files.hudexchange.info/resources/documents/System-Performance-Measure-7-Housing-Destination-Summary.pdf). Alternatively, an individual could have moved in to the permanent housing which is recorded as the "Housing Move-in Date" as per HUD [3.20](https://files.hudexchange.info/resources/documents/HMIS-Data-Standards-Manual.pdf)   | Long Beach HMIS 
|**Age Groups** | The age group that a person belongs to at the time that the program started | The groups are based off Eligibility for section 8 housing based off Youth (0-17), student (18-24) and seniors (62+) | Long Beach HMIS
|**Average Age** | Average age of program participant as they enter a program.  This measure will include the same individual multiple times as one individual is eligible to receive multiple services over time. | Average age of participant at program entry.  | Long Beach HMIS
|**Average Program Stay in Days** | Average number of days spent in a program.  | Average number of days spent in a program | Long Beach HMIS
|**Monthly Participation Trends** | Number of entries into a program shown as monthly trends over time.  | Sum of services grouped by service type and month/year | Long Beach HMIS
|**Racial Demographics** | Race and ethnicity breakdown for program participants.   | Race and ethnicity groupings divided by total number of People. Ethnicity and Race are combined while giving precedence to "Black, African American and African" then "Hispanic/Latin(a)(o)(x)", then whatever a person entered in for their race. (*Client doesn't know*, *Client refused*, *Data not collected*) are counted as **Unknown**. | Long Beach HMIS
|**Veteran Status** | Describes whether a participant is identified as a veteran or not.  | Sum of *Yes* values denote **Yes**, sum of all other values (*unknown*, *no*, blank, *declined to state*) are counted as **no**.  | Long Beach HMIS
|**Gender** | Describes the participant's gender  | *Client doesn't know*, *Client refused*, *Data not collected*, *Questioning*, *Transgender*, *A gender other than singularly female or male (e.g., non-binary, genderfluid, agender, culturally specific gender)*, *declined to state* are counted as **Others**.  | Long Beach HMIS
|**Destination** | Describes where a program participant went after exiting a program. Unique to the program exit, not to the individual. | Sum of program exit destinations, grouped by exit destination. Does **not** include data for unknown/blank destinations. | Long Beach HMIS
