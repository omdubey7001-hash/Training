import asyncio

from orchestrator.orchestrator import run_orchestration, summarize_results
from agents.answer_agent import answer_agent


async def main():

    print("\n===== DAY 3 TOOL AGENT SYSTEM =====\n")

    # User input (default fallback)
    user_query = input(
        "Enter your query (press enter for default): "
    ).strip()

    if not user_query:
        user_query = "Analyze sales.csv and generate top 5 insights"

    print(f"\nUser Query: {user_query}\n")

    try:

        # Step 1: Run orchestrator
        print("Running orchestration...\n")
        context = await run_orchestration(user_query)

        # Step 2: Combine worker outputs
        print("Summarizing worker outputs...\n")
        final_summary = summarize_results(context)

        # Step 3: Prepare final answer task
        task = (
            "You must answer the user question using the context below.\n\n"
            f"User Query:\n{user_query}\n\n"
            f"Context from tools and workers:\n{final_summary}"
        )

        # Step 4: Generate final response
        result = await answer_agent.run(task=task)

        print("\n========== FINAL ANSWER ==========\n")
        print(result.messages[-1].content)

    except Exception as e:
        print("\n❌ Error during execution")
        print(str(e))


if __name__ == "__main__":
    asyncio.run(main())