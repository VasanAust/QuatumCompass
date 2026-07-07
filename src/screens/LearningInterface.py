import json
import time
from typing import List, Dict, Any, Literal, TypedDict, Optional

# ==========================================
# TYPE DEFINITIONS & MODELS
# ==========================================
class Message(TypedDict):
    role: Literal['user', 'ai']
    text: str
    timestamp: int

class Toast(TypedDict):
    id: str
    message: str
    type: Literal['xp', 'badge', 'info']

class AppState(TypedDict):
    level: Literal['explorer', 'adventurer', 'scholar', 'researcher']
    xp: int
    earnedBadgeIds: List[str]
    completedTopicIds: List[str]
    currentTopicIndex: int
    chatHistory: List[Message]
    toasts: List[Toast]
    userApiKey: str


# ==========================================
# FROM: LearningInterface.tsx (Terminal Console Hub)
# ==========================================
class TerminalLearningInterface:
    """
    The master workspace dashboard panel. Hooks into backend service payloads,
    manages the core application state loop, and prints structural shell grids.
    """
    def __init__(self, initial_state: AppState, tutor_service_instance: Any):
        self.state: AppState = initial_state
        self.tutor_service = tutor_service_instance
        
        # UI Toggles
        self.show_sim_info = True
        self.accent_colors = {
            "explorer": "PURPLE",
            "adventurer": "TEAL",
            "scholar": "AMBER",
            "researcher": "RED"
        }

        # Mock Curriculum Database matching assets.ts configurations
        self.curriculum_db = {
            "explorer": [
                {"id": "magic_coin", "title": "The Magic Quantum Coin", "simulationType": "coin_flip", "xpReward": 25},
                {"id": "mystery_box", "title": "The Mystery Box", "simulationType": "box_peek", "xpReward": 25}
            ],
            "adventurer": [
                {"id": "double_slit", "title": "Double-Slit Wave Mechanics", "simulationType": "double_slit", "xpReward": 40}
            ],
            "scholar": [
                {"id": "bloch_sphere", "title": "Bloch Sphere State Vectors", "simulationType": "bloch_sphere", "xpReward": 60}
            ],
            "researcher": [
                {"id": "vqe_solver", "title": "Variational Quantum Eigensolver", "simulationType": "vqe_viz", "xpReward": 100}
            ]
        }

    @property
    def current_curriculum(self) -> List[Dict[str, Any]]:
        return self.curriculum_db.get(self.state["level"], self.curriculum_db["explorer"])

    @property
    def active_topic(self) -> Dict[str, Any]:
        idx = self.state["currentTopicIndex"]
        curr = self.current_curriculum
        if idx >= len(curr):
            return curr[0]
        return curr[idx]

    @property
    def accent_color(self) -> str:
        return self.accent_colors.get(self.state["level"], "PURPLE")

    def dispatch_action(self, action_type: str, payload: Any = None):
        """Replicates Reducer dispatch action mutation pipelines."""
        if action_type == "ADD_TOAST":
            self.state["toasts"].append(payload)
        elif action_type == "REMOVE_TOAST":
            self.state["toasts"] = [t for t in self.state["toasts"] if t["id"] != payload]
        elif action_type == "SET_TOPIC_INDEX":
            if 0 <= payload < len(self.current_curriculum):
                self.state["currentTopicIndex"] = payload
                self.state["chatHistory"] = [] # Clear contextual threads on topic shifts
                print(f"[Workspace Navigation]: Shifted topic target node index to -> {payload}")
        elif action_type == "LOGOUT":
            print("🚪 Exiting runtime environment context. Clearing cached session vectors.")
            self.state["userApiKey"] = ""

    def handle_send_message(self, text: str):
        """Processes synchronous message flows, feeding outputs to dispatcher action loops."""
        if not text.strip():
            return

        # 1. Mount user chat bubble onto state array timeline
        user_msg: Message = {"role": "user", "text": text, "timestamp": int(time.time())}
        self.state["chatHistory"].append(user_msg)
        
        print(f"\n[You]: {text}")
        print("🤖 Quantum Tutor is typing...")
        time.sleep(0.8) # Mock computational engine latency

        # 2. Fire backend payload service proxy dispatcher
        try:
            response = self.tutor_service.send_to_quantum_tutor(
                user_message=text,
                history=self.state["chatHistory"][:-1],
                level=self.state["level"],
                current_topic=self.active_topic,
                completed_topic_ids=self.state["completedTopicIds"],
                user_api_key=self.state["userApiKey"]
            )
            
            # 3. Handle message rendering injection
            ai_msg: Message = {"role": "ai", "text": response["text"], "timestamp": int(time.time())}
            self.state["chatHistory"].append(ai_msg)

            # 4. Parse transaction side-effect mutations array loops
            for action in response.get("actions", []):
                if action["type"] == "award_xp":
                    pts = action.get("amount", 10)
                    self.state["xp"] += pts
                    self.dispatch_action("ADD_TOAST", {"id": str(time.time()), "message": f"+{pts} Quantum XP Granted!", "type": "xp"})
                
                elif action["type"] == "award_badge":
                    bid = action.get("badgeId", "unknown")
                    if bid not in self.state["earnedBadgeIds"]:
                        self.state["earnedBadgeIds"].append(bid)
                        self.dispatch_action("ADD_TOAST", {"id": str(time.time()), "message": f"🏆 Unlocked Badge: {bid.upper()}", "type": "badge"})
                
                elif action["type"] == "complete_topic":
                    tid = self.active_topic["id"]
                    if tid not in self.state["completedTopicIds"]:
                        self.state["completedTopicIds"].append(tid)
                        print(f"🏁 milestone achieved! Mastered topic registry block: {tid}")
                        # Automatically advance step bounds if available
                        if self.state["currentTopicIndex"] + 1 < len(self.current_curriculum):
                            self.dispatch_action("SET_TOPIC_INDEX", self.state["currentTopicIndex"] + 1)

        except Exception as e:
            error_msg: Message = {"role": "ai", "text": f"⚠️ Operational Error: {str(e)}", "timestamp": int(time.time())}
            self.state["chatHistory"].append(error_msg)

    def render_ui(self):
        """Paints a layout map tracking curriculum progress bars, histograms, and conversation lists."""
        print("\n" + "=========================================================================")
        print(f"🔬  QUANTUM LEARNING STUDIO CONSOLE WORKSPACE  |  Level: {self.state['level'].upper()}")
        print("=========================================================================")
        
        # Row A: Scoreboard Banner Status bar
        print(f"🏅 Rank Progression Score: {self.state['xp']} XP  |  Caches: {len(self.state['earnedBadgeIds'])} Badges Earned  |  Accent Theme: {self.accent_color}")
        print("-" * 73)

        # Row B: Structural Layout Columns Split
        print(" [📚 CURRICULUM MAP PANEL]             [🎮 ACTIVE LAB SIMULATOR DEVICE]")
        for i, topic in enumerate(self.current_curriculum):
            status = "✓" if topic["id"] in self.state["completedTopicIds"] else ("▶" if i == self.state["currentTopicIndex"] else " 🔒")
            print(f"   ({status}) Topic {i+1}: {topic['title']:<24} |   Running Simulation Module: [{self.active_topic['simulationType'].upper()}]")
        
        if self.show_sim_info:
            print(f"                                       |   💡 Formula: Physics engine mapped to Born Rule criteria.")
        
        print("-" * 73)

        # Row C: Conversational Threads Blocks
        print(" 💬 RECENT CONVERSATION HISTORY:")
        if not self.state["chatHistory"]:
            print("    [System]: Channel initialized. Introduce yourself to begin.")
        else:
            for m in self.state["chatHistory"][-3:]: # Display tail limit entries
                speaker = "👤 You" if m["role"] == "user" else "🤖 Guide"
                print(f"    {speaker}: {m['text']}")
        
        # Row D: Flash notifications Toast Alerts Banner
        if self.state["toasts"]:
            print("\n ✨ TOAST NOTIFICATIONS ALERT:")
            for t in self.state["toasts"]:
                print(f"    🌟 [{t['type'].upper()}] {t['message']}")
            self.state["toasts"] = [] # Clear toast vectors after rendering frame

        print("=========================================================================\n")


# Executable runtime sandbox environment
if __name__ == "__main__":
    # Import previously generated mock service frameworks
    from quantumTutor import QuantumTutorService
    mock_tutor_api = QuantumTutorService()

    # Initialise application state tree records
    initial_app_state: AppState = {
        "level": "explorer",
        "xp": 120,
        "earnedBadgeIds": ["coin_toss_badge"],
        "completedTopicIds": ["magic_coin"],
        "currentTopicIndex": 1, # Set on 'The Mystery Box'
        "chatHistory": [],
        "toasts": [],
        "userApiKey": "sk-sandbox-twin-token-2026"
    }

    # Instantiate workspace layout component
    workspace = TerminalLearningInterface(initial_state=initial_app_state, tutor_service_instance=mock_tutor_api)

    # 1. Output empty rest state screen
    workspace.render_ui()

    # 2. Simulate typing interaction event payload triggers
    workspace.handle_send_message("I am guessing the box container holds a composite mixed wave matrix before I pop the latch?")
    workspace.render_ui()