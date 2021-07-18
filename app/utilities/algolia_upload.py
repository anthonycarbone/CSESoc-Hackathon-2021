import json

import config
import pandas as pd
from algoliasearch.search_client import SearchClient

APP_ID = config.ALGOLIA_APP_ID
API_KEY = config.ALGOLIA_API_KEY


def importData(csvPath):
    df: pd.DataFrame = pd.read_excel(csvPath, header=0)
    return df.to_json(orient="records")


client = SearchClient.create(APP_ID, API_KEY)

index = client.init_index("schollars")

scholarships = json.loads(importData("app/data/db.xlsx"))

index.save_objects(scholarships, {"autoGenerateObjectIDIfNotExist": True})
