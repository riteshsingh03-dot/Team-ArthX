import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types
import time
from google.genai.errors import ServerError

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def call_gemini_with_retry(fn, *args, retries=2, base_delay=3, **kwargs):
    for attempt in range(retries + 1):
        try:
            return fn(*args, **kwargs)
        except ServerError:
            if attempt == retries:
                raise
            time.sleep(base_delay * (attempt + 1))

EXTRACTION_PROMPT = """
Extract structured information from the user's message about starting a business.
Return ONLY valid JSON, no other text, matching exactly this shape:

{{
  "project_cost": <number or null>,
  "state": <string or null>,
  "business_category": <string or null>,
  "margin_capital": <number or null>,
  "village_name": <string or null>,
  "block": <string or null>,
  "district": <string or null>
}}

If a field isn't mentioned, use null. Do not guess or invent values.
Amounts in "lakh" mean multiply by 100000 (e.g. "1 lakh" = 100000).
village_name, block, and district refer to the user's location in India --
extract whichever of these the user mentions (e.g. "I'm in Barasat village,
North 24 Parganas district" -> village_name: "Barasat", district: "North 24 Parganas").
If the user only gives one place name and it's ambiguous whether it's a village,
block, or district, put it in village_name.

User message: "{message}"
"""


def extract_user_intent(message: str) -> dict:
    prompt = EXTRACTION_PROMPT.format(message=message)
    response = call_gemini_with_retry(
        client.models.generate_content,
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(response_mime_type="application/json"),
    )
    return json.loads(response.text)