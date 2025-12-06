# Using Ollama as a local summarizer (optional)

If you have Ollama installed (https://ollama.com/) and a model downloaded, you can replace the transformers summarizer with a local call to Ollama. This avoids cloud costs and keeps data on your machine.

Example usage (Node or shell):

Shell example (invoke Ollama HTTP server):

```bash
# Run Ollama model locally (assumes ollama and a model are set up)
# (example using 'llama2' as model name)
ollama run llama2 --port 11434 &

# Example curl call to get a summary (replace prompt as needed)
curl -s -X POST "http://localhost:11434/run/llama2" \
  -H 'Content-Type: application/json' \
  -d '{"prompt":"Summarize the following evidence into 5 short bullets:\n               ","max_tokens":300}'
```

Python snippet (requests):

```python
import requests
payload = {"prompt": "Summarize: ...", "max_tokens": 300}
res = requests.post('http://localhost:11434/run/llama2', json=payload)
print(res.json())
```

Notes:
- Ollama's API and model names depend on your local setup.
- Using Ollama keeps data local and avoids paying for embeddings/summaries to cloud providers.
- You can still use sentence-transformers for embeddings and Ollama for summarization.
