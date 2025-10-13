"""
HCC Plan Web Unified - Haupteinstiegspunkt
"""

from fastapi import FastAPI

app = FastAPI(title="HCC Plan Web Unified")

@app.get("/")
async def root():
    return {"message": "HCC Plan Web Unified"}