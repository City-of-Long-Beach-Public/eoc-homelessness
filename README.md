# Homelessness Emergency scripts / ETL / Queries

```
pipenv install
```

## Enrollees ( HMIS Data)

1. Have the Health Department Liason download yearly files from the Looker site and put it in the sharepoint site

1. From the Sharepoint folder grab the new files per year and put it in the "data/enrollees_extract" Folder

2. Run 
```
pipenv run enrollees
```

or, in the appropriate shell environment with the right python interpreter
```
python clean_enrollees_extract.py
```

3. The cleaned up csv will be outputted as "data/enrollees_extract.csv"
4. Upload the output to the sharepoint site

## Outreach ( Encampment Data )

1. Go to the [Cognito Forms](https://www.cognitoforms.com/) website

2. Download the "Outreach Requests" form by going to Entries > Actions > Export > Current View

3. Place the xlsx document as "data/outreach_extract/Outreach Requests.xlsx"

2. Run 
```
pipenv run outreach
```

or, in the appropriate shell environment with the right python interpreter
```
python clean_outreach.py
```

3. The cleaned up csv will be outputted as "data/outreach_extract.csv"
4. Upload the output to the sharepoint site


## Rental ( Rental Assistance Data )

1. Ask Development Services to download an extract of data in our Yardi system from tracking Rental Assistance

3. Place the xlsx document as "data/rentals_extract/rental_case_summary.xlsx"

2. Run 
```
pipenv run rentals
```

or, in the appropriate shell environment with the right python interpreter
```
python clean_rentals.py
```

3. The cleaned up csv will be outputted as "data/rentals_extract.csv"

4. Upload the output to the sharepoint site

5. Ask Development Services liaison to update the budget amounts

6. In Power BI change the measure for "Total Grant Amount"

## Shelter Beds 

1. Copy the Shelter bed tracker xlsx document into the EOC sharepoint location

## MSC Visits

1. Go to the original file in Sharepoint

2. Go to the tab for the month

3. Copy over the visits column and the date

4. Download the previous csv

5. Add the new month

6. Save and reupload to the sharepoint

## Emergency Housing Vouchers

1. Ask the liaison to the Housing Department to update the raw spreadsheet of values

2. Download the current csv

3. Add in the new line for the new month

4. Make sure housed column is Column L de-running totalled

5. Reupload to the right sharepoint location