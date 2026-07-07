from typing import List, Dict, Callable, TypedDict, Union

# ==========================================
# DEPENDENCY MAP: Static Data Types & Assets
# ==========================================
class Topic(TypedDict):
    id: str
    title: str
    prerequisiteIds: List[str]
    simulationType: str
    openingPrompt: str
    completionCriteria: str
    xpReward: int

class Badge(TypedDict):
    id: str
    label: str
    icon: str
    topicId: str
    level: str

# Static badges from assets.ts to map icons to topics
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
# FROM: CurriculumMap.tsx (Console UI Layer)
# ==========================================
class TerminalCurriculumMap:
    """
    Simulates the visual React layout engine for progression pathways, 
    evaluating dependency graph restrictions and rendering locked/completed states.
    """
    def __init__(
        self,
        topics: List[Topic],
        current_topic_index: int,
        completed_topic_ids: List[str],
        on_topic_select: Callable[[int], None],
        accent_color: str = "PURPLE"
    ):
        self.topics = topics
        self.current_topic_index = current_topic_index
        self.completed_topic_ids = completed_topic_ids
        self.on_topic_select = on_topic_select
        self.accent_color = accent_color

    def is_topic_unlocked(self, topic: Topic) -> bool:
        """Helper to determine if a topic is unlocked based on its prerequisite chain."""
        if not topic["prerequisiteIds"]:
            return True
        return all(prereq_id in self.completed_topic_ids for prereq_id in topic["prerequisiteIds"])

    def render_ui(self):
        """Renders a visual vertical path representing the curriculum timeline node grid."""
        print("\n" + "=" * 60)
        print(f"📖  CURRICULUM PROGRESSION  |  Accent: {self.accent_color}")
        print("=" * 60)

        for idx, topic in enumerate(self.topics):
            is_current = idx == self.current_topic_index
            is_completed = topic["id"] in self.completed_topic_ids
            is_unlocked = self.is_topic_unlocked(topic)
            
            # Retrieve badge icon from asset mapping file configuration lookup
            badge_icon = "🎓"
            for b in STATIC_BADGES:
                if b["topicId"] == topic["id"]:
                    badge_icon = b["icon"]
                    break

            # 1. Compute state prefix indicator character
            if is_completed:
                indicator = "✅"
            elif not is_unlocked:
                indicator = "🔒"
            elif is_current:
                indicator = "▶️ "
            else:
                indicator = f"{idx + 1:2d}"

            # 2. Compute timeline context descriptions
            if is_completed:
                meta_label = f"✨ {badge_icon} badge earned"
            elif is_current:
                meta_label = "🔥 NOW TEACHING"
            else:
                meta_label = f"+ {topic['xpReward']} XP Reward"

            # 3. Format block bounding line style depending on current state highlight rules
            focus_bracket_open = "👉 [ " if is_current else "   ( "
            focus_bracket_close = " ]" if is_current else " )"

            # Render line output text chunk block matching the row content mapping
            print(f"{focus_bracket_open}{indicator}{focus_bracket_close} {topic['title']:<28} │ {meta_label}")
            
            # Print intermediate dotted tracking separator connection path unless last node index
            if idx < len(self.topics) - 1:
                print("         ┊")

        print("=" * 60 + "\n")

    def handle_click_node(self, index: int):
        """Simulates clicking a topic row element block inside the scroll timeline window."""
        if index < 0 or index >= len(self.topics):
            print("[System Error]: Invalid topic reference boundary.")
            return

        target_topic = self.topics[index]
        if self.is_topic_unlocked(target_topic):
            print(f"[UI Interaction]: Topic selected -> Index {index}: {target_topic['title']}")
            self.on_topic_select(index)
        else:
            print(f"[UI Interaction Blocked]: Topic '{target_topic['title']}' remains locked behind prerequisites.")


# Executable runtime instance sandbox
if __name__ == "__main__":
    # Sample Mock Explorer Topics array directly matching assets.ts configurations
    sample_topics: List[Topic] = [
        {
            "id": "magic_coin",
            "title": "The Magic Quantum Coin",
            "prerequisiteIds": [],
            "simulationType": "coin_flip",
            "openingPrompt": "Introduce the quantum coin...",
            "completionCriteria": "Learner explains magic coin concept...",
            "xpReward": 25
        },
        {
            "id": "mystery_box",
            "title": "The Mystery Box",
            "prerequisiteIds": ["magic_coin"],
            "simulationType": "box_peek",
            "openingPrompt": "Connect to the magic coin...",
            "completionCriteria": "Learner explains superposition logic...",
            "xpReward": 25
        },
        {
            "id": "connected_stars",
            "title": "The Connected Stars",
            "prerequisiteIds": ["magic_coin", "mystery_box"],
            "simulationType": "entanglement_stars",
            "openingPrompt": "Introduce two magical best-friend stars...",
            "completionCriteria": "Learner explains non-separable state correlation...",
            "xpReward": 30
        }
    ]

    # Callback action handler simulation logic
    def mock_on_select(new_index: int):
        print(f"🔄 App State Updated: active curriculum reference moved to index {new_index}")

    # Initial App sandbox instance state: User completed first topic, currently studying topic 2
    map_component = TerminalCurriculumMap(
        topics=sample_topics,
        current_topic_index=1,
        completed_topic_ids=["magic_coin"],
        on_topic_select=mock_on_select
    )

    # Render layout view
    map_component.render_ui()

    # Simulate navigation timeline selection clicks
    print("User attempts to click node index 0 (Completed topic)...")
    map_component.handle_click_node(0)
    
    print("\nUser attempts to click node index 2 (Locked topic)...")
    map_component.handle_click_node(2)