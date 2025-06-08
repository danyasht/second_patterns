#api_routes
from fastapi import APIRouter, UploadFile, File
from database import get_connection, insert_index, insert_currency_pair
from models import IndexCreate, CurrencyPairCreate
from fastapi.responses import JSONResponse
from upload_csv import process_uploaded_csv

router = APIRouter()

@router.get("/indexes")
def get_all_indexes():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Indexes")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

@router.get("/indexes/{index_id}")
def get_index(index_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Indexes WHERE id=%s", (index_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if not result:
        return JSONResponse(status_code=404, content={"detail": f"Index with ID {index_id} not found"})
    return result

@router.post("/indexes")
def create_index(index: IndexCreate):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Indexes WHERE name=%s", (index.name,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return JSONResponse(status_code=200, content={"detail": f"Index '{index.name}' already exists"})

    insert_index(index.name, index.value)
    cursor.close()
    conn.close()
    return {"message": "Index added"}

@router.put("/indexes/{index_id}")
def update_index(index_id: int, index: IndexCreate):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Indexes WHERE id=%s", (index_id,))
    if cursor.fetchone() is None:
        cursor.close()
        conn.close()
        return JSONResponse(status_code=404, content={"detail": f"Index with ID {index_id} not found"})

    cursor.execute(
        "UPDATE Indexes SET name=%s, value=%s WHERE id=%s",
        (index.name, index.value, index_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Index updated"}

@router.delete("/indexes/{index_id}")
def delete_index(index_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Indexes WHERE id=%s", (index_id,))
    if cursor.fetchone() is None:
        cursor.close()
        conn.close()
        return JSONResponse(status_code=404, content={"detail": f"Index with ID {index_id} not found"})

    cursor.execute("DELETE FROM Indexes WHERE id=%s", (index_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Index deleted"}

@router.get("/currency-pairs")
def get_currency_pairs():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM CurrencyPairs")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

@router.get("/currency-pairs/{pair_id}")
def get_currency_pair(pair_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM CurrencyPairs WHERE id=%s", (pair_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if not result:
        return JSONResponse(status_code=404, content={"detail": f"Currency pair with ID {pair_id} not found"})
    return result

@router.post("/currency-pairs")
def create_currency_pair(pair: CurrencyPairCreate):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id FROM CurrencyPairs 
        WHERE baseCurrency=%s AND quoteCurrency=%s
    """, (pair.baseCurrency, pair.quoteCurrency))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return JSONResponse(status_code=200, content={"detail": f"Currency pair {pair.baseCurrency}/{pair.quoteCurrency} already exists"})

    insert_currency_pair(pair.baseCurrency, pair.quoteCurrency, pair.exchangeRate)
    cursor.close()
    conn.close()
    return {"message": "Currency pair added"}

@router.put("/currency-pairs/{pair_id}")
def update_currency_pair(pair_id: int, pair: CurrencyPairCreate):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM CurrencyPairs WHERE id=%s", (pair_id,))
    if cursor.fetchone() is None:
        cursor.close()
        conn.close()
        return JSONResponse(status_code=404, content={"detail": f"Currency pair with ID {pair_id} not found"})

    cursor.execute("""
        UPDATE CurrencyPairs
        SET baseCurrency=%s, quoteCurrency=%s, exchangeRate=%s
        WHERE id=%s
    """, (pair.baseCurrency, pair.quoteCurrency, pair.exchangeRate, pair_id))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Currency pair updated"}

@router.delete("/currency-pairs/{pair_id}")
def delete_currency_pair(pair_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM CurrencyPairs WHERE id=%s", (pair_id,))
    if cursor.fetchone() is None:
        cursor.close()
        conn.close()
        return JSONResponse(status_code=404, content={"detail": f"Currency pair with ID {pair_id} not found"})

    cursor.execute("DELETE FROM CurrencyPairs WHERE id=%s", (pair_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Currency pair deleted"}

@router.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        return JSONResponse(status_code=404, content={"detail": "Only CSV files are allowed"})

    await process_uploaded_csv(file)
    return {"message": "CSV uploaded and processed successfully"}
