import json
import os
from typing import List, Dict, Any, Literal, TypedDict, Optional, Callable

# ==========================================
# IMPORTING REGISTERED APPLICATION MODULES
# ==========================================
from ApiKeySetup import TerminalApiKeySetup
from KnowledgeAssessment import TerminalKnowledgeAssessment
from LearningInterface import TerminalLearningInterface, AppState, Message
from LevelComplete import TerminalLevelComplete
from Settings import TerminalSettings
from quantumTutor import QuantumTutorService

# File names mimicking window.localStorage mechanics
LOCAL_STORAGE_STATE_FILE = "QUANTUM_COMPASS_STATE.json"
LOCAL_STORAGE_KEY_FILE = "QUANTUM_COMPASS_KEY.txt"


# ==========================================
# FROM: App.tsx (State Reducer & Router Orchestrator)
# ==========================================
class TerminalAppOrchestrator:
    """
    The main runtime framework container. Manages core state mutations, 
    hydrates data maps from historical session logs, and routes execution windows.
    """
    def __init__(self):
        # 1. Replicating the initialization parameters from initialState
        self.state: Dict[str, Any] = {
            "screen": "api_setup", # Initial gate layout screen
            "userApiKey": "",
            "level": None,         # Choices: 'explorer', 'adventurer', 'scholar', 'researcher'
            "currentTopicIndex": 0,
            "completedTopicIds": [],
            "earnedBadgeIds": [],
            "xp": 0,
            "chatHistory": [],
            "toasts": []
        }
        
        self.tutor_service = QuantumTutorService()
        self.hydrate_state_from_storage()

    def app_reducer(self, action_type: str, payload: Any):
        """
        Replicates the client appReducer switch case matrix. 
        Synchronously calculates state fields and initiates disk trace flushes.
        """
        if action_type == "SET_API_KEY":
            self.state["userApiKey"] = payload
            self.state["screen"] = "assessment"
            
        elif action_type == "SET_LEVEL":
            is_level_changed = self.state["level"] != payload
            self.state["level"] = payload
            self.state["currentTopicIndex"] = 0
            if is_level_changed:
                self.state["chatHistory"] = [] # Clear context threads on track split shifts
                
        elif action_type == "SET_SCREEN":
            self.state["screen"] = payload
            
        elif action_type == "LOAD_PERSISTED_STATE":
            if payload:
                self.state.update(payload)
                
        elif action_type == "RESET_PROGRESS":
            self.state = {
                "screen": "assessment",
                "userApiKey": "",
                "level": None,
                "currentTopicIndex": 0,
                "completedTopicIds": [],
                "earnedBadgeIds": [],
                "xp": 0,
                "chatHistory": [],
                "toasts": []
            }
            # Unlink cached credentials matching localStorage removals
            if os.path.exists(LOCAL_STORAGE_KEY_FILE): os.remove(LOCAL_STORAGE_KEY_FILE)
            if os.path.exists(LOCAL_STORAGE_STATE_FILE): os.remove(LOCAL_STORAGE_STATE_FILE)

        # Mirror useEffect lifecycle monitoring bounds by auto-saving changes on state updates
        self.persist_state_to_storage()

    def hydrate_state_from_storage(self):
        """Reads persistent storage files to recreate active session vectors."""
        try:
            # Check for saved custom API Key tokens
            if os.path.exists(LOCAL_STORAGE_KEY_FILE):
                with open(LOCAL_STORAGE_KEY_FILE, "r") as kf:
                    saved_key = kf.read().strip()
                    if saved_key:
                        self.state["userApiKey"] = saved_key
                        self.state["screen"] = "assessment"

            # Check for saved application progress metrics maps
            if os.path.exists(LOCAL_STORAGE_STATE_FILE):
                with open(LOCAL_STORAGE_STATE_FILE, "r") as sf:
                    saved_state = json.load(sf)
                    self.state.update(saved_state)
        except Exception as err:
            print(f"⚠️ Failed to hydrate state from local memory tracks: {err}")

    def persist_state_to_storage(self):
        """Flushes transient run metrics onto system cache sheets."""
        try:
            if self.state["userApiKey"]:
                with open(LOCAL_STORAGE_KEY_FILE, "w") as kf:
                    kf.write(self.state["userApiKey"])
            
            # Serialize state dictionary excluding hot network tokens or ephemeral views
            save_payload = {k: v for k, v in self.state.items() if k not in ["userApiKey", "screen", "toasts"]}
            with open(LOCAL_STORAGE_STATE_FILE, "w") as sf:
                json.dump(save_payload, sf, indent=2)
        except Exception as err:
            print(f"⚠️ State synchronization layer failed: {err}")

    def start_runtime_