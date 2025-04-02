# langgraph_flow.py

from langgraph.graph import StateGraph, END
from typing import TypedDict
from huggingface_hub import InferenceClient
from utils.model_config import HF_MODEL_NAME, HF_TOKEN, switch_to_next_model

def get_inference_client():
    from huggingface_hub import InferenceClient
    try:
        return get_inference_client()
    except Exception as e:
        switch_to_next_model()
        return get_inference_client()

# === Shared memory for the graph ===
class ResearchState(TypedDict):
    topic: str
    idea: str
    lit_review: str
    structure: str
    drafts: dict
    final: str

# === Initialize Hugging Face client ===
hf_token = "your_token_here"  # Replace with secure loading if needed
client = get_inference_client()

# === Step functions representing each agent ===
def idea_agent(state: ResearchState) -> ResearchState:
    topic = state.get("topic", "")
    idea = f"Brainstormed research idea based on: {topic}"
    return {**state, "idea": idea}

def lit_review_agent(state: ResearchState) -> ResearchState:
    topic = state.get("topic", "")
    prompt = f"You are an academic assistant. Summarize the current literature relevant to the topic: '{topic}' in 5–7 sentences."
    result = client.text_generation(prompt=prompt, max_new_tokens=500, temperature=0.6)
    summary = result.strip()
    return {**state, "lit_review": summary}

def structure_agent(state: ResearchState) -> ResearchState:
    idea = state.get("idea", "")
    lit = state.get("lit_review", "")
    structure = f"Generated structure based on idea: {idea} and lit review: {lit}"
    return {**state, "structure": structure}

def writing_agent(state: ResearchState) -> ResearchState:
    structure = state.get("structure", "")
    lit = state.get("lit_review", "")
    drafts = {
        "Introduction": f"Introduction using structure: {structure} and lit review: {lit}",
        "Methodology": f"Methodology based on structure: {structure}"
    }
    return {**state, "drafts": drafts}

def refine_agent(state: ResearchState) -> ResearchState:
    drafts = state.get("drafts", {})
    refined = {k: v + " (refined)" for k, v in drafts.items()}
    return {**state, "drafts": refined}

def export_agent(state: ResearchState) -> ResearchState:
    final_text = "\n".join([f"{k}: {v}" for k, v in state["drafts"].items()])
    return {**state, "final": final_text}

# === Build LangGraph ===
workflow = StateGraph(ResearchState)

workflow.add_node("IdeaAgent", idea_agent)
workflow.add_node("LitReviewAgent", lit_review_agent)
workflow.add_node("StructureAgent", structure_agent)
workflow.add_node("WritingAgent", writing_agent)
workflow.add_node("RefineAgent", refine_agent)
workflow.add_node("ExportAgent", export_agent)

workflow.set_entry_point("IdeaAgent")
workflow.add_edge("IdeaAgent", "LitReviewAgent")
workflow.add_edge("LitReviewAgent", "StructureAgent")
workflow.add_edge("StructureAgent", "WritingAgent")
workflow.add_edge("WritingAgent", "RefineAgent")
workflow.add_edge("RefineAgent", "ExportAgent")
workflow.add_edge("ExportAgent", END)

# === Compile the flow ===
research_graph = workflow.compile()

if __name__ == "__main__":
    initial_state = ResearchState(topic="Social Media and Consumer Trust")
    final_state = research_graph.invoke(initial_state)
    print("\n=== Final Output ===")
    print(final_state["final"])