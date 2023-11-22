# llm-analytics

The logfile stores the config and output metrics for inference.

The models currently used are:
OpenHermes-2.5-Mistral-7B-GGUF
OpenHermes-2.5-Mistral-7B-16k-GGUF

Workflow:
1. `python llm-analytics.py`
(Copy batch size and context length to clipboard)
2. `c`
3. `8` or appropriate cpu_threads value
(Copy output string to clipboard)
4. `c`
5. Success! Logfile has data you can analyze later to optimize these values.
