import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

from database import db, create_document, get_documents
from schemas import Event, Publication, BlogPost, Commission, Center, Member, ContactMessage

app = FastAPI(
    title="Kolegium Dermatologi, Venereologi & Estetika API",
    description="Backend API untuk konten dinamis (event, publikasi, blog, komisi, senter, anggota, kontak)",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Kolegium Dermatologi, Venereologi & Estetika API"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": "❌ Not Set",
        "database_name": "❌ Not Set",
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set"
            response["database_name"] = getattr(db, 'name', '✅ Connected')
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:20]
                response["database"] = "✅ Connected & Working"
                response["connection_status"] = "Connected"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response

# ----- Public content endpoints (list, simple create) -----

@app.get("/api/events", response_model=List[dict])
def list_events(limit: Optional[int] = 50):
    try:
        docs = get_documents("event", {}, limit)
        for d in docs:
            d["_id"] = str(d.get("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/events")
def create_event(event: Event):
    try:
        inserted_id = create_document("event", event)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/publications", response_model=List[dict])
def list_publications(limit: Optional[int] = 50):
    try:
        docs = get_documents("publication", {}, limit)
        for d in docs:
            d["_id"] = str(d.get("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/publications")
def create_publication(pub: Publication):
    try:
        inserted_id = create_document("publication", pub)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/blogs", response_model=List[dict])
def list_blogs(limit: Optional[int] = 50):
    try:
        docs = get_documents("blogpost", {}, limit)
        for d in docs:
            d["_id"] = str(d.get("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/blogs")
def create_blog(post: BlogPost):
    try:
        inserted_id = create_document("blogpost", post)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/commissions", response_model=List[dict])
def list_commissions(limit: Optional[int] = 50):
    try:
        docs = get_documents("commission", {}, limit)
        for d in docs:
            d["_id"] = str(d.get("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/commissions")
def create_commission(comm: Commission):
    try:
        inserted_id = create_document("commission", comm)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/centers", response_model=List[dict])
def list_centers(limit: Optional[int] = 50):
    try:
        docs = get_documents("center", {}, limit)
        for d in docs:
            d["_id"] = str(d.get("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/centers")
def create_center(center: Center):
    try:
        inserted_id = create_document("center", center)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/contact")
def submit_contact(msg: ContactMessage):
    try:
        inserted_id = create_document("contactmessage", msg)
        return {"id": inserted_id, "status": "received"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
