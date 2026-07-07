import json
from typing import List, Dict, Any, Literal, TypedDict, Optional

# ==========================================
# TYPE DEFINITIONS & MODELS
# ==========================================
class ChatMessage(TypedDict):
    role: Literal['user', 'ai']
    text: str
    timestamp: int

class TopicDefinition(TypedDict):
    id: str
    title: str
    openingPrompt: str
    completionCriteria: str
    xpReward: int

class TutorAction(TypedDict):
    type: Literal['award_xp', 'award_badge', 'complete_topic']
    amount: Optional[int]
    badgeId: Optional[str]

class TutorCitation(TypedDict):
    title: str
    url: str

class TutorResponse(TypedDict):
    text: str
    actions: List[TutorAction]
    citations: Optional[List[TutorCitation]]


# ==========================================
# FROM: quantumTutor.ts (Python Integration Engine)
# ==========================================
class QuantumTutorService:
    """
    Manages communication payloads dispatched to the backend core AI model server.
    Serializes application matrices and mirrors action parser signatures.
    """
    def __init__(self, api_endpoint: str = "/api/tutor"):
        self.api_endpoint = api_endpoint

    def send_to_quantum_tutor(
        self,
        user_message: str,
        history: List[ChatMessage],
        level: Literal['explorer', 'adventurer', 'scholar', 'researcher'],
        current_topic: TopicDefinition,
        completed_topic_ids: List[str],
        user_api_key: str
    ) -> TutorResponse:
        """
        Prepares standard structural JSON network payloads and models 
        the server API endpoint interaction loop.
        """
        # Build identical request serialization layout structure 
        payload = {
            "message": user_message,
            "history": history,
            "level": level,
            "currentTopic": current_topic,
            "completedTopicIds": completed_topic_ids,
            "userApiKey": user_api_key,
        }

        print(f"\n📡 [Network Outbound]: Sending message data to core engine endpoint '{self.api_endpoint}'...")
        # (In a live system, replace this placeholder print with: response = requests.post(..., json=payload))
        # print(json.dumps(payload, indent=2))

        # --- Simulated Server Roundtrip Responses ---
        # Mocking incoming processing action structures returned by the tutor core engine
        mock_response: TutorResponse = {
            "text": "Fascinating prediction! Notice how the interference ripples grow or shrink when you slide it.",
            "actions": [
                { "type": "award_xp", "amount": 25, "badgeId": None },
                { "type": "complete_topic", "amount": None, "badgeId": None }
            ],
            "citations": [
                { "title": "Quantum Wave Mechanics", "url": "https://example.edu/quantum-waves" }
            ]
        }

        return mock_response


# Executable runtime instance sandbox
if __name__ == "__main__":
    tutor_service = QuantumTutorService()

    # Define mock properties matches 
    sample_topic: TopicDefinition = {
        "id": "magic_coin",
        "title": "The Magic Quantum Coin",
        "openingPrompt": "Have you seen a coin spinning in mid-air?",
        "completionCriteria": "Explain superposition behavior...",
        "xpReward": 25
    }

    sample_history: List[ChatMessage] = [
        { "role": "ai", "text": "Hello, traveler! Let's explore quantum coins.", "timestamp": 1717800000 },
        { "role": "user", "text": "I am ready for the challenge!", "timestamp": 1717800010 }
    ]

    # Dispatch request data structure
    response_payload = tutor_service.send_to_quantum_tutor(
        user_message="I think the spinning coin lives in a mixed combination state!",
        history=sample_history,
        level="adventurer",
        current_topic=sample_topic,
        completed_topic_ids=[],
        user_api_key="sk-mock-quantum-key-2026"
    )

    # Output resulting dispatch actions payload items
    print("\n📥 [Network Inbound Response Receiver]:")
    print(f"   💬 Response: {response_payload['text']}")
    print("   🎯 Actions Parsed:")
    for action in response_payload["actions"]:
        if action["type"] == "award_xp":
            print(f"      ✨ Award {action['amount']} Points to User Inventory")
        elif action["type"] == "complete_topic":
            print("      🏁 Flag Topic Complete and Unlock Next Stage Node")
