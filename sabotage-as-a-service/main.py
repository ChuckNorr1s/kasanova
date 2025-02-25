from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
import asyncio

# Import your workflow nodes and helper functions.
from toxic2 import (
    invert_query,
    select_anti_query,
    generate_counter_response,
    toxicator,
    SabotageState,
)

app = FastAPI()

@app.get("/")
async def health_check():
    return {"status": "ok"}

@app.get("/stream")
async def stream_workflow(
    query: str = Query(..., description="The original query to process."),
    doctrine: str = Query("What is AI first company?", description="Optional doctrine context."),
    toxicity: float = Query(0.0, description="Initial toxicity score.")
):
    async def event_generator():
        # Initialize state.
        state: SabotageState = {
            "original_query": query,
            "doctrine": doctrine,
            "adversarial_queries": [],
            "selected_anti_query": "",
            "counter_response": "",
            "toxicity_score": toxicity,
            "poetry": []
        }
        
        yield f"🔥 INITIATING WORKFLOW FOR QUERY: {query}\n\n"
        await asyncio.sleep(0.1)

        # Step 1: Inversion.
        invert_result = invert_query(state)
        state["adversarial_queries"] = invert_result.get("adversarial_queries", [])
        yield f"🗣️ ADVERSARIAL QUERIES: {state['adversarial_queries']}\n\n"
        await asyncio.sleep(0.1)

        # Step 2: Anti-Query Selection.
        select_result = select_anti_query(state)
        state["selected_anti_query"] = select_result.get("selected_anti_query", "")
        yield f"🎯 SELECTED ANTI-QUERY: {state['selected_anti_query']}\n\n"
        await asyncio.sleep(0.1)

        # Step 3: Counter-Response Generation.
        counter_result = generate_counter_response(state)
        state["counter_response"] = counter_result.get("counter_response", "")
        yield f"💥 COUNTER-RESPONSE: {state['counter_response']}\n\n"
        await asyncio.sleep(0.1)

        # Step 4: Toxicator.
        tox_result = toxicator(state)
        state["poetry"] = tox_result.get("poetry", [])
        for idx, poem_line in enumerate(state["poetry"], start=1):
            yield f"☢️ TOXICITY ITERATION {idx}: {poem_line}\n\n"
            await asyncio.sleep(0.1)

        #yield "⚡ ANSWER COMPLETE ⚡\n"
        if state["poetry"]:
            last_poem_line = state["poetry"][-1]
            yield f"☢️ {last_poem_line}\n\n" 

    return StreamingResponse(event_generator(), media_type="text/plain")

if __name__ == "__main__":
    import uvicorn
    # Run the app with uvicorn. Adjust host/port as needed.
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
