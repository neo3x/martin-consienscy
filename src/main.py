"""Main entry point for the Artificial Consciousness Architecture - Phase 0.

This module provides the interactive interface to the system.
"""

import sys
from pathlib import Path

import structlog
from dotenv import load_dotenv

from .config import settings
from .core.loop import InteractionLoop
from .utils.logger import configure_logging

# Load environment variables
load_dotenv()

# Configure logging
configure_logging()
logger = structlog.get_logger()


def print_banner() -> None:
    """Print the welcome banner."""
    banner = """
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║     ARTIFICIAL CONSCIOUSNESS ARCHITECTURE - Phase 0              ║
║     Experimental Exploration of Emergent Cognition               ║
║                                                                  ║
║     A philosophical exploration with a technical artifact        ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝

Current Phase: 0 (Foundation)
Capabilities:
  - Emotional state tracking (5 dimensions)
  - Episodic memory with subjective valence
  - State-modulated responses
  - Memory consolidation and search

Type 'help' for commands, 'quit' to exit.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    print(banner)


def print_help() -> None:
    """Print help information."""
    help_text = """
Available Commands:
  help          - Show this help message
  status        - Show current system status
  quit, exit    - Exit the system
  reset         - Reset system state (development only)

  Any other input will be processed as a conversation.
"""
    print(help_text)


def print_status(loop: InteractionLoop) -> None:
    """Print current system status.

    Args:
        loop: The interaction loop
    """
    status = loop.get_system_status()

    print("\n━━━━ System Status ━━━━")
    print(f"\nPhase: {status['phase']}")

    print("\nEmotional State:")
    dims = status["emotional_state"]["dimensions"]
    print(f"  Valence:    {dims['valence']:+.2f} (-1 to +1)")
    print(f"  Activation: {dims['activation']: .2f} (0 to 1)")
    print(f"  Certainty:  {dims['certainty']: .2f} (0 to 1)")
    print(f"  Aperture:   {dims['aperture']: .2f} (0 to 1)")
    print(f"  Connection: {dims['connection']: .2f} (0 to 1)")
    print(f"  Intensity:  {status['emotional_state']['intensity']: .2f}")
    print(f"  Duration:   {status['emotional_state']['duration']} interactions")

    print("\nMemory:")
    print(f"  Total memories:     {status['memory_stats']['total_memories']}")
    print(f"  Formative memories: {status['memory_stats']['formative_memories']}")

    print("━━━━━━━━━━━━━━━━━━━━\n")


def interactive_mode() -> None:
    """Run the system in interactive mode (REPL)."""
    print_banner()

    # Initialize the interaction loop
    logger.info("initializing_system")
    try:
        loop = InteractionLoop()
        logger.info("system_initialized_successfully")
    except Exception as e:
        logger.error("system_initialization_failed", error=str(e))
        print(f"\nError initializing system: {e}")
        print("Please check your configuration and try again.")
        return

    print("\nSystem initialized. Ready for interaction.\n")

    # Main interaction loop
    while True:
        try:
            # Get user input
            user_input = input("\n You: ").strip()

            if not user_input:
                continue

            # Handle commands
            if user_input.lower() in ["quit", "exit"]:
                print("\nShutting down system...")
                logger.info("system_shutdown_requested")
                break

            elif user_input.lower() == "help":
                print_help()
                continue

            elif user_input.lower() == "status":
                print_status(loop)
                continue

            elif user_input.lower() == "reset":
                confirm = input("\nAre you sure you want to reset the system? (yes/no): ")
                if confirm.lower() == "yes":
                    loop.reset()
                    print("\nSystem reset complete.\n")
                else:
                    print("\nReset cancelled.\n")
                continue

            # Process as normal interaction
            print("\nSystem: ", end="", flush=True)
            response = loop.process_interaction(user_input)
            print(response)

        except KeyboardInterrupt:
            print("\n\nInterrupted. Type 'quit' to exit.\n")
            continue

        except EOFError:
            print("\n\nExiting...")
            break

        except Exception as e:
            logger.error("unexpected_error_in_interaction", error=str(e), exc_info=True)
            print(f"\nUnexpected error: {e}")
            print("The system will continue, but you may want to check the logs.\n")

    print("\nGoodbye.\n")
    logger.info("system_shutdown_complete")


def main() -> None:
    """Main entry point."""
    try:
        interactive_mode()
    except Exception as e:
        logger.error("fatal_error", error=str(e), exc_info=True)
        print(f"\nFatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
