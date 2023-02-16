# Homelessness Emergency scripts / ETL / Queries

```
pipenv install
```

## Enrollees

1. From the Sharepoint folder grab the new files per year and put it in the "data/enrollees_extract" Folder

2. Run 
```
pipenv run enrollees
```

or, in the appropriate shell environment with the right python interpreter
```
python clean_enrollees_extract.py
```

5. The cleaned up csv will be outputted as "data/enrollees_extract.csv"
6. Upload the output to the sharepoint site
