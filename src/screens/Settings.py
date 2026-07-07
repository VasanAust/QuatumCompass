import time
from typing import Dict, Literal, Callable, Any, List, Optional

# ==========================================
# FROM: Settings.tsx (Console Config Panel)
# ==========================================
class TerminalSettings:
    """
    Simulates the options settings console overlay. Allows changing active 
    knowledge stream channels, clearing session credentials, and performing full progress wipes.
    """
    def __init__(self, state: Dict[str, Any], dispatch_callback: Callable[[str, Any], None]):
        self.state = state
        self.dispatch = dispatch_callback
        
        # Submenu interactive modal confirmation states
        self.level_to_confirm: Optional[Literal['explorer', 'adventurer', 'scholar', 'researcher']] = None
        self.show_clear_key_confirm = False
        self.show_reset_confirm = False

        self.levels: List[Literal['explorer', 'adventurer', 'scholar', 'researcher']] = [
            "explorer", "adventurer", "scholar", "researcher"
        ]

    def render_ui(self):
        """Paints a structural settings control panel card box layout."""
        print("\n" + "⚙️" * 20)
        print("⚙️   QUANTUM ENGINE CONFIGURATION CONTROLS")
        print("⚙️" * 20)
        print(f"   Current Active Stream : {self.state.get('level', 'explorer').upper()}")
        print(f"   Stored Workspace Key  : {'[CONNECTED LOCAL TOKEN]' if self.state.get('userApiKey') else '[NO CUSTOM KEY ASSIGNED]'}")
        print("-" * 55)

        print("   📂 CHOOSE OPERATION CHANNEL INDEX:")
        print("     [1] Force Override Active Stream Track Level")
        print("     [2] Revoke Secure API Key Credentials")
        print("     [3] Clear Local Sandbox History (Hard Factory Reset)")
        print("     [4] Exit Settings & Return to Main Dashboard Workspace")
        print("-" * 55)

        # Draw confirmation prompt contexts inline based on active states
        if self.level_to_confirm:
            print(f"   ⚠️ OVERRIDE WARNING: Are you sure you want to jump to the")
            print(f"       [{self.level_to_confirm.upper()}] track? Syllabus indexes will recalibrate.")
            print("       Options: [Y] Confirm Shift  |  [N] Abort Shift")
        
        elif self.show_clear_key_confirm:
            print("   ⚠️ CREDENTIALS REVOCATION: Delete cached access codes from memory?")
            print("       Options: [Y] Clear Token    |  [N] Abort Cleardown")
            
        elif self.show_reset_confirm:
            print("   🚨🚨 DANGER HARD CLEAR: This will permanently delete everything!")
            print("       All earned simulation medals and accumulated XP points will go to 0.")
            print("       Options: [Y] YES, WIPE EVERYTHING  |  [N] Cancel Reset")
            
        print("⚙️" * 20 + "\n")

    def execute_prompt(self):
        """Processes interaction loops and feeds choice matrices into state callback paths."""
        self.render_ui()
        choice = input("Select settings index option: ").strip()

        # Route A: Change active profile level tier
        if choice == "1":
            print("\nAvailable Track Levels: [1] Explorer | [2] Adventurer | [3] Scholar | [4] Researcher")
            lvl_idx = input("Select level target index: ").strip()
            if lvl_idx in ["1", "2", "3", "4"]:
                self.level_to_confirm = self.levels[int(lvl_idx) - 1]
                self.render_ui()
                confirm = input("Confirm stream shift (y/n): ").strip().lower()
                if confirm == "y":
                    self.dispatch("SET_LEVEL", self.level_to_confirm)
                    print(f"✓ Profile stream calibrated successfully to {self.level_to_confirm.upper()}.")
                self.level_to_confirm = None

        # Route B: Purge AI studio credentials
        elif choice == "2":
            self.show_clear_key_confirm = True
            self.render_ui()
            confirm = input("Clear API credentials (y/n): ").strip().lower()
            if confirm == "y":
                self.dispatch("SET_API_KEY", "")
                print("✓ Secure cache keys removed from active runtime channel vectors.")
            self.show_clear_key_confirm = False

        # Route C: Execute hard data clear down
        elif choice == "3":
            self.show_reset_confirm = True
            self.render_ui()
            confirm = input("Execute complete database wipe (y/n): ").strip().lower()
            if confirm == "y":
                print("\n💥 Purging local state fields. Clearing telemetry indices...")
                time.sleep(0.5)
                self.dispatch("RESET_PROGRESS", None)
                self.dispatch("SET_SCREEN", "assessment")
                print("✓ Wipe successfully completed. Re-routing back to placement assessment.")
            self.show_reset_confirm = False

        # Route D: Back navigation exit
        elif choice == "4":
            print("\nReturning to active dashboard workspace view...")
            self.dispatch("SET_SCREEN", "learning")
            
        else:
            print("[Settings Warning]: Operation code ignored or input timed out.")


# Executable runtime instance sandbox
if __name__ == "__main__":
    # Mocking active application dictionary state values
    mock_app_state = {
        "level": "adventurer",
        "userApiKey": "sk-gemini-sandbox-token-99823",
        "xp": 280,
        "screen": "settings"
    }

    def handle_reducer_dispatch(action_type: str, payload: Any):
        print(f"\n🔄 Reducer Dispatch Trigger -> Type: [{action_type}] | Payload Hooked: '{payload}'")
        if action_type == "SET_LEVEL":
            mock_app_state["level"] = payload
        elif action_type == "SET_API_KEY":
            mock_app_state["userApiKey"] = payload
        elif action_type == "SET_SCREEN":
            mock_app_state["screen"] = payload
        elif action_type == "RESET_PROGRESS":
            mock_app_state["level"] = "explorer"
            mock_app_state["xp"] = 0
            mock_app_state["userApiKey"] = ""

    # Instantiate configuration gate panel controller
    settings_panel = TerminalSettings(state=mock_app_state, dispatch_callback=handle_reducer_dispatch)
    
    # Execute setting option selection sequences
    settings_panel.execute_prompt()