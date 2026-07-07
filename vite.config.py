"""
FRAMEWORK CONFIGURATION (Equivalent to vite.config.ts)

Establishes global module path resolving, configuration parameters, 
and sets system resource utilization rules for local development and execution flags.
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional

class FrameworkConfig:
    """
    Manages global configuration parameters, mock asset aliases, 
    and controls background process pooling behaviors.
    """
    def __init__(self):
        # Resolve path directories (Equivalent to path.resolve(__dirname, '.'))
        self.BASE_DIR: Path = Path(__file__).resolve().parent
        
        # Path aliases dictionary map (Equivalent to resolve.alias: {'@': ...})
        self.ALIAS: Dict[str, Path] = {
            "@": self.BASE_DIR,
            "@skills": self.BASE_DIR / "skills",
            "@components": self.BASE_DIR / "components"
        }

        # Watcher/Performance configurations matching HMR block rules
        # In systems with heavy background processes, file watching can be toggled
        self.DISABLE_HOT_RELOAD: bool = os.environ.get("DISABLE_HMR") == "true"
        
        # Determine internal performance polling delays based on environment rules
        self.POLLING_INTERVAL: Optional[float] = None if self.DISABLE_HOT_RELOAD else 0.5

    def get_absolute_path(self, alias_path: str) -> Path:
        """Translates frontend framework path expressions into concrete system paths."""
        for alias, actual_path in self.ALIAS.items():
            if alias_path.startswith(alias):
                return actual_path / alias_path[len(alias):].lstrip("/")
        return self.BASE_DIR / alias_path

    def export_config_summary(self) -> Dict[str, Any]:
        """Provides an inspection matrix for verifying workspace status parameters."""
        return {
            "root_path": str(self.BASE_DIR),
            "performance_throttling_active": self.DISABLE_HOT_RELOAD,
            "hot_file_polling_seconds": self.POLLING_INTERVAL,
            "registered_aliases": list(self.ALIAS.keys())
        }


# Executable instance sandbox
if __name__ == "__main__":
    # Simulate turning on the resource-saving lock matching environment overrides
    os.environ["DISABLE_HMR"] = "true"
    
    config = FrameworkConfig()
    summary = config.export_config_summary()
    
    print("\n" + "⚙️" * 20)
    print("🛠️   QUANTUM ENGINE RUNTIME METADATA")
    print("⚙️" * 20)
    print(f"   Root Target Workspace : {summary['root_path']}")
    print(f"   Path Aliases Mapped   : {summary['registered_aliases']}")
    print(f"   File System Watcher   : {'[PAUSED / CPU CONSERVATION ACTIVE]' if summary['performance_throttling_active'] else '[ACTIVE]'}")
    print("⚙️" * 20 + "\n")