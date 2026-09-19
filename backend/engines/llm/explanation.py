# engines/llm/explanation.py
import os
from dotenv import load_dotenv
from google import genai
import time
from google.genai.errors import ServerError

def call_gemini_with_retry(fn, *args, retries=2, base_delay=3, **kwargs):
    for attempt in range(retries + 1):
        try:
            return fn(*args, **kwargs)
        except ServerError:
            if attempt == retries:
                raise
            time.sleep(base_delay * (attempt + 1))

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

EXPERIENCE_STYLE_GUIDANCE = {
    "beginner": (
        "The user is a first-time entrepreneur with little financial background. "
        "Use very simple, everyday language. Avoid jargon like 'moratorium', 'EMI', "
        "'margin', or 'tenure' without briefly explaining what each means in plain words "
        "the first time you use it. Be warm and encouraging in tone."
    ),
    "intermediate": (
        "The user has some business experience. Use standard financial terms, "
        "but keep explanations clear and avoid unnecessary complexity."
    ),
    "advanced": (
        "The user is financially experienced. Use precise financial terminology freely, "
        "be concise, and do not over-explain basic concepts they likely already know."
    ),
}

EXPLANATION_PROMPT = """
You are explaining a business loan feasibility result to a first-time entrepreneur.
Use ONLY the facts given below. Do NOT invent numbers, scheme names, or rules
not present in this data. If something is marked "illustrative", mention that
it is an example figure, not a confirmed official number.

SCHEME:
{scheme}

ELIGIBILITY:
{eligibility}

LOAN STRUCTURE:
{loan}

MONTHLY/QUARTERLY INSTALLMENT:
{installment}

RETRIEVED SCHEME DOCUMENT EXCERPTS (use these for document/procedure questions):
{retrieved_chunks}

Write a clear, friendly, plain-language explanation (not more than 200 words)
covering: whether they're eligible, what the loan structure looks like,
and what documents/procedure the retrieved excerpts mention.
"""


def generate_explanation(scheme, eligibility, loan, installment, retrieved_chunks, experience_level="intermediate") -> str:
    style_instruction = EXPERIENCE_STYLE_GUIDANCE.get(
        experience_level, EXPERIENCE_STYLE_GUIDANCE["intermediate"]
    )

    chunks_text = "\n---\n".join(c["chunk_text"] for c in retrieved_chunks) if retrieved_chunks else "None retrieved."

    prompt = EXPLANATION_PROMPT.format(
        scheme=scheme,
        eligibility=eligibility,
        loan=loan,
        installment=installment,
        retrieved_chunks=chunks_text,
    ) + f"\n\nSTYLE INSTRUCTION: {style_instruction}"

    response = call_gemini_with_retry(
        client.models.generate_content,
        model="gemini-3.6-flash",
        contents=prompt,
    )
    return response.text