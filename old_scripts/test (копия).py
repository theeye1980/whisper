# test_gpu.py
import time
from llama_cpp import Llama, llama_supports_gpu_offload

print(f"GPU offload supported: {llama_supports_gpu_offload()}")
model_path = "/home/vyacheslav/projects/training/Qwen3-8B-Q4_K_M.gguf"
llm = Llama(
    model_path = model_path,  # укажи путь
    n_gpu_layers=-1,
    verbose=True
)

response = llm.create_chat_completion(
    messages=[
        {"role": "user", "content": "приветик" + " /no_think"}
    ],
    max_tokens=5024,
    temperature=0.7
)

content = response["choices"][0]["message"]["content"]
print(response)
print(content)