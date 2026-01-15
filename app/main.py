from fastapi import FastAPI, UploadFile, File, HTTPException, Query

app = FastAPI(title="CSV -> Pandas -> MongoDB API")


@app.post("/top-threats")
def read_csv_and_add_to_db(file):
    ...

