# 1) Define tools (functions that the agent can call)
def get_flight_info(flight_number: str):
    # call a flight API and return structured info
    return {"flight": flight_number, "arrival_time": "2024-08-01T14:30:00Z", "city": "SFO"}

flight_tool = Tool(
    name="flight_info",
    func=get_flight_info,
    description="Get flight arrival information given a flight number."
)

# 2) Create an LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 3) Initialize the agent with tools and an agent strategy
agent = initialize_agent(
    tools=[flight_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# 4) Run the agent
result = agent.run("Book me a cab for my return flight. My flight number is UA123.")
print(result)
```

Note: APIs and LLms evolve—check your LangChain version docs for the most current agent initialization patterns.

<Callout icon="warning">
  Agents can incur additional API calls, latency, and cost because they loop between the LLM and tools. Validate tool permissions, rate limits, and error handling. Always add input sanitization and monitoring to avoid harmful or unintended actions.
</Callout>

## Best practices for building reliable agents

* Limit tool access to only what the agent needs; define clear tool descriptions.
* Use memory thoughtfully: persist only what helps future decisions.
* Add deterministic validation steps before executing impactful actions (payments, bookings).
* Design prompts that guide the LLM to provide structured outputs when the agent must parse results.
* Monitor agent runs and log both tool usage and LLM decisions for debugging and auditing.

## Links and references

* [LangChain Documentation](https://langchain.com/docs/)
* [OpenAI API](https://platform.openai.com/docs)
* [Vector Databases (FAISS, Pinecone, Milvus)](https://www.pinecone.io/)

These references will help you implement agents that safely coordinate LLM reasoning with external capabilities and deliver robust, multi-step automation.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/langchain/module/5bedac05-3eaa-4d0d-9892-e05b80c528fb/lesson/db49466c-c5af-4c79-b889-cf31536588ca" />
</CardGroup>


# Chunking Documents

Source: https://notes.kodekloud.com/docs/LangChain/Performing-Retrieval/Chunking-Documents/page

Explains splitting PDFs into overlapping text chunks using LangChain for embedding and retrieval in RAG pipelines

In this lesson we continue from the document loader step where we loaded `handbook.pdf`. The goal is to split the document into smaller, overlapping chunks (passages) so they can be embedded and stored in a vector store for retrieval-augmented generation (RAG). Proper chunking preserves context, improves retrieval relevance, and improves the quality of LLM responses when using external documents.

## 1. Load the PDF and inspect pages

Use LangChain's PDF loader to read the document as page-level Document objects:

```python theme={null}
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("data/handbook.pdf")
pages = loader.load_and_split()
