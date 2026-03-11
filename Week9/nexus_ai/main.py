import asyncio
import os
import sys
import time
from datetime import datetime

from nexus_ai.config import model_client
from nexus_ai.orchestrator.master_orchestrator import MasterOrchestrator


# ===== SAFE LOG PATH =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "logs", "system.log")
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)


def log_event(event, data=None):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now().isoformat()} | {event} | {data}\n")


async def run_nexus(orchestrator, query):

    print("\n" + "=" * 70)
    print("NEXUS AI — AUTONOMOUS MULTI-AGENT SYSTEM")
    print("*" * 70)
    print(f"TASK → {query}")
    print("-" * 70 + "\n")

    start = time.time()

    try:
        result = await orchestrator.run(query)

        duration = round(time.time() - start, 2)

        log_event("run_success", {
            "query": query,
            "time_sec": duration
        })

        return {
            "success": True,
            "output": result,
            "time": duration
        }

    except Exception as e:

        duration = round(time.time() - start, 2)

        log_event("run_failure", {
            "query": query,
            "error": str(e),
            "time_sec": duration
        })

        return {
            "success": False,
            "error": str(e),
            "time": duration
        }


async def interactive_shell():

    orchestrator = MasterOrchestrator(model_client)

    print("\nNEXUS AI Interactive Shell Ready")
    print("Type 'exit' or press Ctrl+C to quit.\n")

    while True:

        try:
            query = input("Enter Task → ").strip()

            if not query:
                continue

            if query.lower() in ["exit", "quit"]:
                print("Shutting down Nexus AI.")
                break

            result = await run_nexus(orchestrator, query)

            print("\n" + "=" * 70)

            if result["success"]:
                print(f"COMPLETED in {result['time']} sec\n")
                print(result["output"])
            else:
                print(f"FAILED in {result['time']} sec")
                print("ERROR:", result["error"])

            print("=" * 70 + "\n")

        except KeyboardInterrupt:
            print("\nInterrupted by user. Exiting...")
            sys.exit(0)

        except Exception as e:
            print(f"\nFatal Shell Error: {e}")
            log_event("shell_fatal", {"error": str(e)})


async def main():
    await interactive_shell()


if __name__ == "__main__":
    asyncio.run(main())
