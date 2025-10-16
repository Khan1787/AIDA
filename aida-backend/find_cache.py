from huggingface_hub import get_hf_home_dir
import os

# Obține calea către directorul principal Hugging Face
hf_home = get_hf_home_dir()
cache_dir = os.path.join(hf_home, 'hub')

print(f"Directorul de cache Hugging Face este: {cache_dir}")