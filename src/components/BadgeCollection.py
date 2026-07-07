import random
from typing import List, Dict, TypedDict

# ==========================================
# DEPENDENCY MAP: Static Badge Registry 
# (Sourced from assets.ts to remain standalone)
# ==========================================
class Badge(TypedDict):
    id: str
    label: str
    icon: str
    topicId: str
    level: str

STATIC_BADGES: List[Badge] = [
    { "id": "coin_master",      "label": "Quantum Coin Master",    "icon": "🪙", "topicId": "magic_coin",             "level": "explorer"   },
    { "id": "mystery_solver",   "label": "Mystery Box Solver",     "icon": "📦", "topicId": "mystery_box",            "level": "explorer"   },
    { "id": "star_connector",   "label": "Star Connector",         "icon": "⭐", "topicId": "connected_stars",        "level": "explorer"   },
    { "id": "wave_master",      "label": "Wave Master",            "icon": "🌊", "topicId": "wave_interference",      "level": "adventurer" },
    { "id": "double_slit",      "label": "Double-Slit Detective",  "icon": "🔍", "topicId": "double_slit",            "level": "adventurer" },
    { "id": "qubit_navigator",  "label": "Qubit Navigator",        "icon": "🌐", "topicId": "qubit_math",             "level": "scholar"    },
    { "id": "circuit_builder",  "label": "Circuit Architect",      "icon": "⚡", "topicId": "quantum_gates",          "level": "scholar"    },
    { "id": "qec_expert",       "label": "Error Correction Expert","icon": "🔐", "topicId": "error_correction",       "level": "researcher" },
]


# ==========================================
# FROM: BadgeCollection.tsx (Console Component)
# ==========================================
class TerminalBadgeCollection:
    """
    Simulates the visual React grid interface for tracking and displaying
    the user's unlocked achievement badges directly inside a terminal window.
    """
    def __init__(self, earned_badge_ids: List[str], accent_color: str = "PURPLE"):
        self.earned_badge_ids = earned_badge_ids
        self.accent_color = accent_color

    def render_ui(self):
        """
        Renders the collection frame header and computes a 4-column item layout,
        injecting status indicators [🔒] for locked or unearned milestones.
        """
        print("\n" + "▪️" * 30)
        print(f"🏆  EARNED BADGES  |  Accent: {self.accent_color}")
        print("▪️" * 30)

        # Configurable grid layout constraints matching the `grid-cols-4` target layout
        columns = 4
        current_row: List[str] = []

        for badge in STATIC_BADGES:
            is_earned = badge["id"] in self.earned_badge_ids
            
            # Format visual item representation
            if is_earned:
                # Active/Earned state representation
                status_block = f"[{badge['icon']} {badge['label']}]"
            else:
                # Dimmed/Locked state representation matching the opacity-35 and Lock icon logic
                status_block = f"[🔒 (Locked) {badge['label']}]"
            
            current_row.append(status_block)

            # Flush current row text chunk when full matrix boundary is hit
            if len(current_row) == columns:
                # Print nicely spaced columnar blocks
                print("  │  ".join(f"{item:<32}" for item in current_row))
                current_row = []

        # Catch remaining row objects if allocation length leaves a trailing index remainder
        if current_row:
            print("  │  ".join(f"{item:<32}" for item in current_row))
            
        print("▪️" * 30 + "\n")


# Executable runtime instance sandbox
if __name__ == "__main__":
    # Simulate a user state where they have unlocked the first two initial topic tiers
    user_inventory = ["coin_master", "mystery_solver"]
    
    collection_widget = TerminalBadgeCollection(earned_badge_ids=user_inventory)
    collection_widget.render_ui()