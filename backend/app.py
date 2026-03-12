"""
Flask backend with /chat API for LLM conversation.
History is kept in memory (per session); resets on server restart.
"""
import os
from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
from rag.retriever import retrieve_cars
from utils.extract_attributes import extract_attributes

load_dotenv()

app = Flask(__name__)


@app.after_request
def cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


@app.route("/")
def index():
    """Simple root route to check if server is running (open in browser)."""
    return jsonify({"status": "ok", "message": "Server is running", "endpoints": ["/", "/health", "POST /chat"]})


@app.route("/chat", methods=["OPTIONS"])
def chat_options():
    return "", 204

# In-memory conversation history: session_id -> list of {"role": "user"|"assistant", "content": "..."}
chat_history: dict[str, list[dict]] = {}

client = None

def get_client() -> OpenAI | None:
    global client
    if client is None:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            return None
        client = OpenAI(api_key=api_key)
    return client

@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json(silent=True) or {}
    user_message = (data.get("message") or "").strip()
    attributes = extract_attributes(user_message)
    print("Extracted attributes:", attributes) 
    session_id = data.get("session_id") or "default"

    if not user_message:
        return jsonify({"error": "message is required"}), 400

    openai_client = get_client()
    if not openai_client:
        return jsonify({"error": "OPENAI_API_KEY not set"}), 503

    # Get or create history
    if session_id not in chat_history:
        chat_history[session_id] = []

    history = chat_history[session_id]
    history.append({"role": "user", "content": user_message})

    # 🔎 Retrieve relevant cars using vector search
    retrieved_cars = retrieve_cars(user_message)

    # Corner case handling
    if len(retrieved_cars) == 0:
        return jsonify({
            "reply": "No cars found for your requirement. Try increasing your budget or choosing a different vehicle type."
    })

    context = "\n\n".join(retrieved_cars)

 # Build prompt
    messages = [
    {
        "role": "system",
        "content": """
You are an intelligent car recommendation assistant.

Your task is to recommend cars based on user requirements such as:
- budget
- fuel type
- vehicle type

Rules:
1. Only recommend cars from the provided car data.
2. Never invent cars that are not in the dataset.
3. Prefer cars that match the user's budget and requirements.
4. Recommend 2–3 cars maximum.

Response format:

Car Name
Price
Fuel Type
Mileage
Key Features
Short description

If no cars match the requirement, politely suggest the closest alternatives.
"""
    },
        {
            "role": "user",
            "content": f"""
User request:
{user_message}

Relevant cars:
{context}
"""
        }
    ]

    # include conversation history
    for msg in history:
        messages.append({"role": msg["role"], "content": msg["content"]})

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )

        assistant_message = response.choices[0].message.content

        # Context validation
        valid = False
        for car in retrieved_cars:
            car_name = car.split("\n")[0].replace("Car Name:", "").strip()
            if car_name in assistant_message:
                valid = True
                break

        # fallback if hallucination happens
        if not valid:
            assistant_message = "Sorry, I couldn't find a reliable recommendation from the available data."

        history.append({"role": "assistant", "content": assistant_message})

        return jsonify({"reply": assistant_message})

    except Exception as e:
        history.pop()
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5001)
