import json

import pandas as pd
from algoliasearch.search_client import SearchClient

APP_ID = "U5XKVGUK9E"
API_KEY = "42383009143547ad8d5a2f7f8c5865e1"


def importData(csvPath):
    df: pd.DataFrame = pd.read_excel(csvPath, header=0)
    return df.to_json(orient="records")


client = SearchClient.create(APP_ID, API_KEY)

index = client.init_index("schollars")

scholarships = json.loads(importData("app/db.xlsx"))

index.save_objects(scholarships, {"autoGenerateObjectIDIfNotExist": True})
