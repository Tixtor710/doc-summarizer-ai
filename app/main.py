from fastapi import FastAPI

app = FastAPI(title="Document Summarizer AI")


@app.get("/health")
def health_check():
    return {"status": "ok"}
