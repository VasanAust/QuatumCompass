"""
MAIN ENTRY POINT (Equivalent to main.tsx)

Bootstraps the terminal ecosystem, verifies safe execution parameters, 
and executes the master runtime loop orchestrator.
"""

import sys
from App import TerminalAppOrchestrator

def main():
    # 1. Replicating React.StrictMode console assertions 
    # Ensure system context variables match execution requirements (e.g., Python 3.8+)
    if sys.version_info < (3, 8):
        print("❌ Runtime Initialisation Error: This app requires Python 3.8 or higher.")
        sys.exit(1)

    print("🌌 Initialising Quantum Compass Framework Emitter...")
    print("🎨 CSS Injection: Standard monospace terminal fonts applied successfully.")
    
    # 2. Instantiate and mount the root application module (equivalent to <App />)
    try:
        app = TerminalAppOrchestrator()
        app.start_runtime_loop()
    except KeyboardInterrupt:
        # Gracefully capture global terminal escape signals (Ctrl+C)
        print("\n\n🌌 Session broken via user sign-off. Safe travels through the multiverse! 🚀")
        sys.exit(0)
    except Exception as e:
        print(f"\n💥 Fatal Application Crash: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()