from transformers import AutoTokenizer, AutoModelForCausalLM

# Numele modelului pe Hugging Face
model_name = "google/medgemma-4b-it"

# Descarcă și încarcă modelul (se salvează automat în cache-ul tău local)
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

print("Modelul MedGemma a fost descărcat și încărcat cu succes!")