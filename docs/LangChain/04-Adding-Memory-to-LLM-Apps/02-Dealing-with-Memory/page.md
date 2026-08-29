# Append a message to a conversation list
redis.rpush(f"conv:{conversation_id}:messages", json.dumps({"role": "user", "text": message}))
# Optionally set TTL or trim list length to limit memory
redis.ltrim(f"conv:{conversation_id}:messages", -100, -1)  # keep last 100 messages
```

* Pseudocode to rehydrate context before generating a response:

```python theme={null}
# Retrieve last N messages and build the model prompt
messages = [json.loads(m) for m in redis.lrange(f"conv:{conversation_id}:messages", -10, -1)]
prompt = build_prompt_from_messages(messages, new_user_input)
response = llm.generate(prompt)
# Append model response back to Redis
redis.rpush(f"conv:{conversation_id}:messages", json.dumps({"role": "assistant", "text": response}))
```

This pattern can be adapted for vector stores: instead of saving raw text only, index embeddings to support semantic retrieval for long-term facts and memories.

Security, privacy, and retention

<Callout icon="warning">
  Be mindful of privacy and compliance when persisting conversation data. Mask or redact sensitive information, enforce retention policies, and secure access to your storage backend.
</Callout>

Putting it together

* Short-term memory is ideal for active sessions and quick context passing.
* Long-term memory is necessary for cross-session continuity, personalization, and recall of past facts.
* Choose the right store based on access patterns: Redis for fast ephemeral lists, vector stores for semantic search, and SQL/NoSQL systems for structured user data.
* Always apply retention, redaction, and security best practices to stored conversation data.

Further reading and references

* [Redis](https://redis.io/)
* [SQLite](https://www.sqlite.org/)
* Vector store and embedding solutions (Faiss, Milvus, Pinecone, Weaviate)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/langchain/module/abd1e527-3f6e-4e04-b421-3b1f8de5c69d/lesson/e48e21f4-e63a-4cc1-83b3-5f4d6c5582c3" />
</CardGroup>


# Dealing with Memory

Source: https://notes.kodekloud.com/docs/LangChain/Adding-Memory-to-LLM-Apps/Dealing-with-Memory/page

Explains adding persistent long term memory to LLM applications using external datastores like Redis, managing session histories, RunnableWithMessageHistory, and best practices for privacy and cost management.

In this lesson we’ll demonstrate how to add long-term memory to large language model (LLM) applications.

Short-term "memory" is typically kept in-process as a sequence of messages and passed into a prompt using a `MessagesPlaceholder`. The example below shows an in-memory conversation history that is injected into the prompt on each invocation:

```python theme={null}
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai.chat_models import ChatOpenAI

model = ChatOpenAI()
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You're an assistant who's good at {ability}. Respond in 20 words or fewer"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)
base_chain = prompt | model

history = [
    ("human", "What's a right-angled triangle?"),
    ("ai", "A right-angled triangle has one angle of 90 degrees, with the other two angles summing to 90 degrees."),
]
