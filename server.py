import os
import json
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv

# Load environment variables (equivalent to dotenv.config())
load_dotenv()

app = Flask(__name__, static_folder="dist")
PORT = int(os.environ.get("PORT", 3000))

# Mock data registries simulating imported references/skills arrays
PHYSICS_GROUND_TRUTH = {
    "magic_coin": {
        "approved": [
            "Superposition is a genuine physical state — not uncertainty about a hidden value, enabling quantum speedup via amplitude amplification and wave interference. Does that distinction make sense?"
        ]
    }
}

# ==========================================
# FALLBACK RESPONSES CALCULATOR
# ==========================================
def get_fallback_response(message: str, level: str, current_topic: dict) -> dict:
    """Replicates the local fallback rules mapping for offline/error handling."""
    topic_id = current_topic.get("id", "general") if current_topic else "general"
    lower_msg = message.lower()
    
    text = ""
    actions = []

    if topic_id == "magic_coin":
        if level == "explorer":
            text = (
                "Hello there! I'm Quantum Compass, your friendly guide. 🧭 Let's talk about **The Magic Quantum Coin**!\n\n"
                "Think of a normal coin. It can be Heads or Tails. But when you spin it on a table, is it heads or tails while it's spinning? "
                "It is actually a blur of both states simultaneously until you slap your hand down onto it!"
            )
            actions = [{"type": "award_xp", "amount": 10}]
    else:
        text = f"I am here to guide you through your quantum journey. Tell me more about your thoughts on this system."
        actions = []

    return {"text": text, "actions": actions, "citations": []}


# ==========================================
# ENDPOINT: /api/tutor (Core Channel Proxy)
# ==========================================
@app.route("/api/tutor", methods=["POST"])
def tutor_endpoint():
    """
    Main route accepting frontend payloads. Unpacks parameters, triggers
    AI inference rules or fires state fallbacks.
    """
    try:
        data = request.get_json() or {}
        
        user_message = data.get("message", "")
        history = data.get("history", [])
        level = data.get("level", "explorer")
        current_topic = data.get("currentTopic", {})
        completed_topic_ids = data.get("completedTopicIds", [])
        user_api_key = data.get("userApiKey", "")

        # Target API key derivation hierarchy (Injected System Key vs. User Session Key)
        active_api_key = user_api_key or os.environ.get("GEMINI_API_KEY")

        # Fallback branch triggered if credentials haven't been passed
        if not active_api_key:
            fallback = get_fallback_response(user_message, level, current_topic)
            return jsonify(fallback)

        # --- Replicating LLM Model Calling Pipeline Layout ---
        # Simulate standard response cleaning/sanitization hooks
        clean_text = "Superposition lets multiple states mix before any measurement isolates a singular value."
        actions = [{"type": "award_xp", "amount": 25}]
        citations = [{"title": "Quantum Systems Fundamentals", "url": "https://example.edu/fundamentals"}]

        # Replicating validatePhysicsOutput check routine
        has_physics_error = "uncertainty about a hidden value" in user_message.lower()
        if has_physics_error:
            ground_truth = PHYSICS_GROUND_TRUTH.get(current_topic.get("id"), {})
            approved_phrases = ground_truth.get("approved", [])
            fallback_msg = approved_phrases[0] if approved_phrases else "Superposition is a genuine state."
            clean_text = f"That's a really common idea — but quantum mechanics tells us something subtler. {fallback_msg}"

        return jsonify({
            "text": clean_text,
            "actions": actions,
            "citations": citations
        })

    except Exception as e:
        print(f"Error in /api/tutor: {e}")
        return jsonify({"error": str(e) or "An error occurred inside the server-side Quantum Tutor."}), 500


# ==========================================
# ENDPOINT: /api/config (System Metadata Check)
# ==========================================
@app.route("/api/config", methods=["GET"])
def config_endpoint():
    """Reports back if the host server owns an environment API key constraint."""
    has_system_key = "GEMINI_API_KEY" in os.environ and bool(os.environ["GEMINI_API_KEY"].strip())
    return jsonify({"hasSystemKey": has_system_key})


# ==========================================
# STATIC ASSETS / Single-Page Application Fallback Routing
# ==========================================
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    """Serves frontend builds from the dist directory mirror matching index.html fallbacks."""
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")


if __name__ == "__main__":
    print(f"📡 [Server Engine Core Launching]: Binding connection sockets on port http://localhost:{PORT}...")
    app.run(host="0.0.0.0", port=PORT, debug=os.environ.get("NODE_ENV") != "production")