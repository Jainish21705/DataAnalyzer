import os
import sys
import tempfile

import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from main import DataAnalyzer
from Exceptions.exception import CustomException

# ─────────────────────────────────────────────
#  App setup
# ─────────────────────────────────────────────
app = FastAPI(
    title="DataAnalyzer API",
    description=(
        "Automated Dataset Analysis Tool.\n\n"
        "Upload a **CSV or Excel** file to any endpoint below "
        "and get instant insights on your data."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten this in production
    allow_methods=["*"],
    allow_headers=["*"],
)

ALLOWED_EXTENSIONS = {"csv", "xlsx", "xls"}

# ─────────────────────────────────────────────
#  Utility helpers
# ─────────────────────────────────────────────
def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def cleanup(path: str):
    """Silently delete a temp file."""
    try:
        if path and os.path.exists(path):
            os.remove(path)
    except Exception:
        pass


async def save_temp_file(file: UploadFile) -> str:
    """Persist the uploaded file to a temp path and return that path."""
    suffix = os.path.splitext(file.filename)[1]   # .csv / .xlsx / .xls
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        contents = await file.read()
        tmp.write(contents)
        return tmp.name


def validate_file(file: UploadFile):
    """Raise 400 if the file type is not supported."""
    if not allowed_file(file.filename):
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Please upload a CSV or Excel (.xlsx / .xls) file.",
        )


# ─────────────────────────────────────────────
#  POST /api/summary
# ─────────────────────────────────────────────
@app.post(
    "/api/summary",
    tags=["Analysis"],
    summary="Get dataset summary",
    description="Returns shape, column names, data types, and basic statistics of the uploaded dataset.",
)
async def summary(file: UploadFile = File(..., description="CSV or Excel file to analyze")):
    validate_file(file)
    tmp_path = None
    try:
        tmp_path = await save_temp_file(file)
        analyzer = DataAnalyzer()
        analyzer.load_dataset(tmp_path)
        analyzer.analyze_data_summary()
        return {
            "status": "success",
            "data": analyzer.return_output().get("data_summary", {}),
        }
    except CustomException as ce:
        raise HTTPException(status_code=500, detail=str(ce))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cleanup(tmp_path)


# ─────────────────────────────────────────────
#  POST /api/missing-values
# ─────────────────────────────────────────────
@app.post(
    "/api/missing-values",
    tags=["Analysis"],
    summary="Detect missing values",
    description="Identifies columns with missing data, returns count and percentage per column.",
)
async def missing_values(file: UploadFile = File(..., description="CSV or Excel file to analyze")):
    validate_file(file)
    tmp_path = None
    try:
        tmp_path = await save_temp_file(file)
        analyzer = DataAnalyzer()
        analyzer.load_dataset(tmp_path)
        analyzer.analyze_missing_values()
        return {
            "status": "success",
            "data": analyzer.return_output().get("missing_values", {}),
        }
    except CustomException as ce:
        raise HTTPException(status_code=500, detail=str(ce))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cleanup(tmp_path)


# ─────────────────────────────────────────────
#  POST /api/duplicates
# ─────────────────────────────────────────────
@app.post(
    "/api/duplicates",
    tags=["Analysis"],
    summary="Detect duplicate rows",
    description="Counts duplicate rows and returns details about them.",
)
async def duplicates(file: UploadFile = File(..., description="CSV or Excel file to analyze")):
    validate_file(file)
    tmp_path = None
    try:
        tmp_path = await save_temp_file(file)
        analyzer = DataAnalyzer()
        analyzer.load_dataset(tmp_path)
        analyzer.analyze_duplicates()
        return {
            "status": "success",
            "data": analyzer.return_output().get("duplicates", {}),
        }
    except CustomException as ce:
        raise HTTPException(status_code=500, detail=str(ce))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cleanup(tmp_path)


# ─────────────────────────────────────────────
#  POST /api/outliers
# ─────────────────────────────────────────────
@app.post(
    "/api/outliers",
    tags=["Analysis"],
    summary="Detect outliers",
    description="Finds statistical outliers in numeric columns using IQR / Z-score methods.",
)
async def outliers(file: UploadFile = File(..., description="CSV or Excel file to analyze")):
    validate_file(file)
    tmp_path = None
    try:
        tmp_path = await save_temp_file(file)
        analyzer = DataAnalyzer()
        analyzer.load_dataset(tmp_path)
        analyzer.analyze_outliers()
        return {
            "status": "success",
            "data": analyzer.return_output().get("outliers", {}),
        }
    except CustomException as ce:
        raise HTTPException(status_code=500, detail=str(ce))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cleanup(tmp_path)

@app.post("/api/column-stats", tags=["Analysis"])
async def column_stats(file: UploadFile = File(..., description="CSV or Excel file")):
    validate_file(file)
    tmp_path = None
    try:
        tmp_path = await save_temp_file(file)
        analyzer = DataAnalyzer()
        analyzer.load_dataset(tmp_path)
        analyzer.analyze_numeric_columns_statistics()      # ← your new method name
        analyzer.analyze_categorical_columns_statistics()  # ← your new method name
        return {
            "status": "success",
            "data": {
                "numeric_stats":     analyzer.return_output().get("numeric_columns_statistics", {}),
                "categorical_stats": analyzer.return_output().get("categorical_columns_statistics", {}),
            }
        }
    except CustomException as ce:
        raise HTTPException(status_code=500, detail=str(ce))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cleanup(tmp_path)


# ─────────────────────────────────────────────
#  POST /api/analyze  —  full pipeline
# ─────────────────────────────────────────────
@app.post(
    "/api/analyze",
    tags=["Analysis"],
    summary="Run full analysis pipeline",
    description=(
        "Runs all four analyses in one shot: **summary**, **missing values**, "
        "**duplicates**, and **outliers**. Returns a combined JSON response."
    ),
)
async def analyze_all(file: UploadFile = File(..., description="CSV or Excel file to analyze")):
    validate_file(file)
    tmp_path = None
    try:
        tmp_path = await save_temp_file(file)
        analyzer = DataAnalyzer()
        result = analyzer.run_pipeline(tmp_path)
        return {"status": "success", "data": result}
    except CustomException as ce:
        raise HTTPException(status_code=500, detail=str(ce))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cleanup(tmp_path)


# ─────────────────────────────────────────────
#  GET /api/health
# ─────────────────────────────────────────────
@app.get(
    "/api/health",
    tags=["Health"],
    summary="Health check",
    description="Returns 200 OK if the API is up and running.",
)
def health():
    return {"status": "ok", "message": "DataAnalyzer API is running."}


# ─────────────────────────────────────────────
#  Entry point
# ─────────────────────────────────────────────
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)