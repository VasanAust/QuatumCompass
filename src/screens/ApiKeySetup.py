import getpass
import time
from typing import Callable, Optional

# ==========================================
# FROM: ApiKeySetup.tsx (Console Config Gate)
# ==========================================
class TerminalApiKeySetup:
    """
    Simulates the visual onboarding screen, performing initial fallback 
    environment checks and prompting for missing credentials with secure inputs.
    """
    def __init__(self, on_key_submit: Callable[[str], None], on_bypass: Callable[[], None]):
        self.on_key_submit = on_key_submit
        self.on_bypass = on_bypass
        
        self.has_system_key = False
        self.is_loading = True

    def check_system_config(self, mock_env_has_key: bool = False):
        """Simulates asynchronous system check network loop to determine API status."""
        print("⚡ Loading environment profile metadata...")
        time.sleep(0.4) # Mock fetch latency
        
        # Mirror state injection flags
        self.has_system_key = mock_env_has_key
        self.is_loading = False

    def render_ui(self):
        """Renders the welcoming terminal setup shield box layout."""
        if self.is_loading:
            self.check_system_config()

        print("\n" + "🔑" * 20)
        print("🛡️   QUANTUM TUTOR ACCESSIBILITY SIGN-IN")
        print("🔑" * 20)
        print("   Welcome traveler! To communicate with your quantum guide,")
        print("   an AI core credentials channel must be authenticated.")
        print("-" * 50)

        if self.has_system_key:
            print("   ✨ STATUS: Host system key detected inside server workspace configuration!")
            print("   You may bypass authorization manually to inherit system values.")
            print("\n   Options: [1] Use System Credentials  |  [2] Provide Custom API Key Token")
        else:
            print("   ⚠️  STATUS: No global credentials file found in direct workspace pathways.")
            print("   Please pass an AIStudio / Gemini API Key string to open the module terminal.")
            print("\n   Options: [1] Enter Custom API Key Token")

        print("\n   🔒 Privacy Policy: Keys are locked securely inside session caches.")
        print("   Data packets are passed explicitly to official endpoints via TLS proxy routes.")
        print("🔑" * 20 + "\n")

    def execute_prompt(self):
        """Captures input commands and routes through callback confirmation states."""
        self.render_ui()
        choice = input("Select operation index: ").strip()

        if self.has_system_key and choice == "1":
            print("\n🚀 Bypassing custom form. System credentials configuration inherited.")
            self.on_bypass()
        else:
            print("\n--- SECURE HIDDEN INPUT OPTION ACTIVE ---")
            # Uses getpass to hide terminal key characters as they are typed
            custom_key = getpass.getpass("🔑 Paste API Key String: ").strip()
            
            if custom_key:
                print("✨ Key payload captured successfully. Mounting runtime core tunnels...")
                self.on_key_submit(custom_key)
            else:
                print("[Setup Aborted]: Input token cannot be left empty.")
