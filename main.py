import os
import traceback
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from supabase import create_client, Client
from google import genai
from ddtrace import tracer

load_dotenv()

# Initialize Google GenAI client
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_KEY:
    raise ValueError("GEMINI_API_KEY is missing from environment")

client = genai.Client(api_key=GEMINI_KEY)

# Initialize Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL or SUPABASE_KEY is missing from environment")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(title="The Cadillac Cookie Company")

# Serve static directory
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

class ConciergeRequest(BaseModel):
    preference: str

@app.get("/")
def serve_home():
    return FileResponse("static/index.html")

@app.post("/api/cookie-concierge")
def cookie_concierge(req: ConciergeRequest):
    preference = req.preference.strip() if req.preference else "classic chocolate chip"

    #call Gemini and get a recommendation
    recommendation = ""
    try:
        with tracer.trace("gemini.generate_content", service="cadillac-cookie-api", resource="cookie_pairing"):
            prompt = (
                f"You are the executive flavor concierge for The Cadillac Cookie Company. "
                f"Provide a rich, 2-sentence luxury cookie pairing and flavor profile for: '{preference}'."
            )
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )
            
            if response and response.text:
                recommendation = response.text.strip()
            else:
                recommendation = f"A signature dark cocoa and Madagascar bourbon vanilla pairing designed for '{preference}'."
    except Exception as e:
        print("\n--- GEMINI ERROR ---")
        traceback.print_exc()
        recommendation = f"A rich espresso-infused brown butter formulation crafted for '{preference}'."

    # Step 2: Persist to Supabase
    try:
        with tracer.trace("supabase.insert", service="cadillac-cookie-api", resource="cookie_orders"):
            supabase.table("cookie_orders").insert({
                "cookie_flavor": preference,
                "curator_notes": recommendation,
                "status": "curated"
            }).execute()
    except Exception as e:
        print("\n--- SUPABASE ERROR ---")
        traceback.print_exc()

    return {
        "status": "success",
        "flavor": preference,
        "recommendation": recommendation
    }