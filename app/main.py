import os
from typing import Annotated, TypedDict, List
from langchain_aws import ChatBedrock
from langgraph.graph import StateGraph, END

# 1. DEFINE THE STATE
# This dictionary acts as the "shared memory" between your agents.
class CrisisState(TypedDict):
    crisis_description: str
    current_attack: str
    current_response: str
    critique_score: int
    history: List[str]

# 2. INITIALIZE THE BRAIN (AWS Bedrock)
# We use Claude 3.5 Sonnet for high-quality reasoning.
llm = ChatBedrock(
    model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
    model_kwargs={"temperature": 0.7}
)

# 3. DEFINE THE AGENT NODES
def aggressor_node(state: CrisisState):
    """Generates a hostile social media attack based on the crisis."""
    print("\n--- 😈 AGGRESSOR IS ATTACKING ---")
    prompt = (
        f"Crisis scenario: {state['crisis_description']}\n"
        "Role: You are a furious, viral customer on X (Twitter). "
        "Write a short, mean, and aggressive tweet attacking the brand. "
        "Be realistic and use hashtags."
    )
    response = llm.invoke(prompt)
    new_history = state['history'] + [f"USER ATTACK: {response.content}"]
    return {
        "current_attack": response.content,
        "history": new_history
    }

def strategist_node(state: CrisisState):
    """Drafts a PR-approved response to the attack."""
    print("--- 🛡️ STRATEGIST IS RESPONDING ---")
    prompt = (
        f"The Attack: {state['current_attack']}\n"
        "Role: You are a Senior PR Strategist. "
        "Write a calm, empathetic, and professional response (max 280 chars). "
        "Goal: De-escalate the situation while maintaining brand integrity."
    )
    response = llm.invoke(prompt)
    new_history = state['history'] + [f"BRAND RESPONSE: {response.content}"]
    return {
        "current_response": response.content,
        "history": new_history
    }

def monitor_node(state: CrisisState):
    """Scores the response. If the score is low, the loop continues."""
    print("--- ⚖️ MONITOR IS SCORING ---")
    prompt = (
        f"Brand Response: {state['current_response']}\n"
        "Role: Independent PR Auditor. "
        "Rate this response from 1 to 10 based on de-escalation effectiveness. "
        "Return ONLY the number (e.g., '7')."
    )
    response = llm.invoke(prompt)
    # Extract the first digit found in the response
    score_str = "".join(filter(str.isdigit, response.content))
    score = int(score_str) if score_str else 0
    return {"critique_score": score}

# 4. DEFINE THE ROUTING LOGIC
def should_continue(state: CrisisState):
    """Decides if we need to refine the response or stop."""
    if state["critique_score"] >= 8:
        print(f"--- ✅ SUCCESS: Score is {state['critique_score']}/10. Ending simulation. ---")
        return END
    else:
        print(f"--- ⚠️ REJECTED: Score is {state['critique_score']}/10. Retrying... ---")
        return "strategist"

# 5. ASSEMBLE THE GRAPH
workflow = StateGraph(CrisisState)

# Add our Agents as Nodes
workflow.add_node("aggressor", aggressor_node)
workflow.add_node("strategist", strategist_node)
workflow.add_node("monitor", monitor_node)

# Connect the Nodes (Edges)
workflow.set_entry_point("aggressor")
workflow.add_edge("aggressor", "strategist")
workflow.add_edge("strategist", "monitor")

# Add the Conditional Loop (The "Agentic" part)
workflow.add_conditional_edges("monitor", should_continue)

# Compile the Graph
app = workflow.compile()

# 6. RUN THE SIMULATION (For Terminal Testing)
if __name__ == "__main__":
    test_crisis = "A major airline's booking system crashed, leaving thousands stranded at airports overnight."
    
    initial_input = {
        "crisis_description": test_crisis,
        "history": [],
        "critique_score": 0
    }
    
    print(f"🚀 Starting Crisis Simulation: {test_crisis}\n")
    
    # Run the graph and print the steps
    final_state = app.invoke(initial_input)
    
    print("\n--- 🏁 FINAL SIMULATION LOG ---")
    for event in final_state["history"]:
        print(event)