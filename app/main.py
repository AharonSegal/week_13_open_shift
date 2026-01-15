from typing import List
import pandas as pd
from fastapi import FastAPI, File, UploadFile, HTTPException, status
from pydantic import ValidationError

from app.db import insert_to_db
from app.models import Threat, TopThreatsResponse

app = FastAPI(title="Top Threats API")
# ---------- Endpoint ----------

@app.post("/top-threats", response_model=TopThreatsResponse)
def top_threats(file: UploadFile | None = File(default=None)):
    """
    POST csv data do db
    get csv 
        if no file -> return code 400 {"detail": "No file provided"}
        if csv parsing error  -> return code 400 {"detail": "Invalid CSV file"}
        if db connection fail -> returncode  503 {"detail": "Database unavailable}
        if pydantic invalid -> return 422 {"detail": "Invalid data format"}
    """
    # PART 1 : IMPORT CSV FILE TO PD DF

    # if no file
    if file is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file provided",
        )

    # if not csv
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid CSV file",
        )

    # convert to pd df
    try:
        df = pd.read_csv(file)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid CSV file",
        )

    # PART 2: FORMAT DF
    
    # sort in descending order 
    df_sorted = df.sort_values(by="danger_rate", ascending=False)
    print("df sorted")
    print(df_sorted)

    # select top 5 
    df_top = df_sorted.head(5)
    # validate and clean: leave only -> name, location , danger_rate
    threats: List[Threat] = []

    # add to list after validating if invalid return 422 error
    try:
        for _, row in df_top.iterrows():
            threat = Threat(
                name=str(row["name"]),
                location=str(row["location"]),
                danger_rate=int(row["danger_rate"]),
            )
            threats.append(threat)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            # pydantic error description
            detail=e.errors(),
        )
    
    # convert list of pydantic obj to list of dicts
    threats_list_dicts = []    
    for threat in threats:
        threat_dict = {}
        threat_dict["name"] = threat.name
        threat_dict["location"] = threat.location
        threat_dict["danger_rate"] = threat.danger_rate
        threats_list_dicts.append(threat_dict)

    # PART 3: SAVE TO DB
    try:
        insert_to_db(threats_list_dicts)
    except:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database unavailable",
        )

    return threats_list_dicts