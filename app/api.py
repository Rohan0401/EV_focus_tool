from collections import defaultdict
import os

from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
import spacy 
import srsly
import uvicorn

from app.models import {
    ENT_PROP_MAP,
    RecordsRequest,
    RecordsResponse,
    RecordsEntitiesByTypeResponse,
}
from app.spacy_extractor import SpacyExtractor

load_dotenv(find_dotenv())
prefix = os.getenv("CLUSTER_ROUTE_PREFIX", "").rstrip("/")

app = FastAPI(
    title="EV_focus_tool",
    version="1.0",
    description="Tool for extracting EV insider trading info",
    openapi_prefix=prefix
)

example_request = srsly.read_json("app/data/example_request.json")

nlp = spacy.load("python")
extractor = SpacyExtractor(nlp)

@app.get("/", include_in_schema=False)
def docs_redirect():
    return RedirectResponse(f"{prefix}/docs")

@app.post("/entities", response_model=RedirectResponse, tags=["NER"])
async def extract_entities(body : RecordRequest = Body(..., example=example_request)):
    """Extract Named Entities from a batch of records """

    res = []
    documents = []

    for val in body.values:
        documents.append({"id" : val.recordId, "text" : val.data.text})
    
    entities_res = extractor.extract_entities(documents)

    res = [
        {"recordsId" : er["id"], "data" : {"entities" : er["entities"]}}
        for er in entities_res
    ]

    return {"values" : res}
@app.post(
    "/entities_by_type", response_model=RecordsEntitiesByTypeResponse, tags=["NER"]
)
async def extract_entities_by_type(body: RecordsRequest = Body(..., example=example_request)):
    """Extract Named Entities from a batch of Records separated by entity label.
        This route can be used directly as a Cognitive Skill in Azure Search
        For Documentation on integration with Azure Search, see here:
        https://docs.microsoft.com/en-us/azure/search/cognitive-search-custom-skill-interface"""

    res = []
    documents = []

    for val in body.values:
        documents.append({"id": val.recordId, "text": val.data.text})

    entities_res = extractor.extract_entities(documents)
    res = []

    for er in entities_res:
        groupby = defaultdict(list)
        for ent in er["entities"]:
            ent_prop = ENT_PROP_MAP[ent["label"]]
            groupby[ent_prop].append(ent["name"])
        record = {"recordId" : er["id"], "data" : groupby}
        res.append(record)
    return {"values" : res}
    