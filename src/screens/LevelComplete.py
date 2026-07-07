from typing import Dict, Literal, Callable, Any, Optional

# ==========================================
# FROM: LevelComplete.tsx (Console Engine)
# ==========================================
class TerminalLevelComplete:
    """
    Renders the promotional completion screen when a learner masterfully completes
    all current curriculum topic vectors, allowing them to advance to the next level track.
    """
    def __init__(self, state: Dict[str, Any], dispatch_callback: Callable[[str, Any], None]):
        self.state = state
        self.dispatch = dispatch_callback
        
        # State path state matrix routes matching the React component configuration keys
        self.next_levels: Dict[str, Optional[str]] = {
            "explorer": "adventurer",
            "adventurer": "scholar",
            "scholar": "researcher",
            "researcher": None,
        }

    @property
    def current_level(self) -> str:
        return self.state.get("level", "explorer")

    @property
    def next_level(self) -> Optional[str]:
        return self.next_levels.get(self.current_level)

    def handle_advance(self):
        """Dispatches action state transitions upgrading the profile stream."""
        if self.next_level:
            print(f"\n✨ Upgrading path stream vector: {self.current_level.upper()} ➔ {self.next_level.upper()} ✨")
            self.dispatch("SET_LEVEL", self.next_level)
            self.dispatch("SET_SCREEN", "learning")
        else:
            print("\n[Action Error]: Maximum researcher mastery level threshold reached.")

    def render_ui(self):
        """Paints the text-art trophy frame capturing metric milestones reached."""
        print("\n" + "🏆" * 20)
        print("🎉  PATH CURRICULUM MASTERED COMPLETE!")
        print("🏆" * 20)
        print(f"   Incredible job, traveler! You have successfully completed")
        print(f"   the official {self.current_level.upper()} educational stream track.")
        print("-" * 50)
        
        # Display localized metrics scorecard summary stats
        print("   📊 QUANTUM SUMMARY SCORECARD:")
        print(f"     • Final Total Score : {self.state.get('xp', 0)} Accumulative XP")
        print(f"     • Unlocked Badges   : {len(self.state.get('earnedBadgeIds', []))} Medals Vault")
        print(f"     • Syllabus Progress : ALL TOPICS (100% Completed)")
        print("-" * 50)

        # Render conditional terminal button frames based on available pathways
        if self.next_level:
            print(f"   🚀 Level-Up Ready: [1] Advance to {self.next_level.upper()} Path")
            print("                      [2] Stay Here & Review Labs")
        else:
            print("   🏆 GRANDMASTER STATUS ACCHIEVED: You have reached the terminal apex")
            print("   of the researcher tier! Outstanding quantum physics academic success.")
            print("\n   Options:           [2] Return to Workspace Labs View")
        print("🏆" * 20 + "\n")

    def execute_prompt(self):
        """Captures option indices to execute linear step transitions."""
        self.render_ui()
        choice = input("Select operation option index: ").strip()