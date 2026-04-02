import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel

class PDFSummarizerAI:
    def __init__(self, base_model_id="meta-llama/Llama-3.2-1B-Instruct"):
        self.base_model_id = base_model_id
        self.model = None
        self.tokenizer = None
        
        self.available_adapters = {
            "nlp": "bartalevente12/nlp-qlora-adapter",
            "robotics": "bartalevente12/robotics-qlora-adapter"
        }

    def load_models(self):
        """Loads the 4-bit base model and attaches all adapters into memory."""
        self.tokenizer = AutoTokenizer.from_pretrained(self.base_model_id, use_fast=True)
        
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        self.tokenizer.padding_side = "left"
        
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16
        )

        base_model = AutoModelForCausalLM.from_pretrained(
            self.base_model_id,
            quantization_config=bnb_config,
            device_map="auto"
        )
        base_model.eval()
        base_model.config.use_cache = True
        
        self.model = PeftModel.from_pretrained(
            base_model, 
            self.available_adapters["nlp"], 
            adapter_name="nlp"
        )
        
        self.model.load_adapter(
            self.available_adapters["robotics"], 
            adapter_name="robotics"
        )
        
        self.model.eval()
        
    def generate_summary(self, text: str, domain: str) -> str:
        """Switches to the right adapter and generates the summary."""
            
        if self.model is None:
            return "Error: Models are not loaded yet. Call load_models() first."

        self.model.set_adapter(domain)
        
        prefix = "Summarize the following scientific paper excerpt in 3-5 sentences.\n\n"
        suffix = "\n\nSummary:\n"
        
        max_ctx = 2048
        max_new = 200
        max_input = max_ctx - max_new
        
        prefix_ids = self.tokenizer(prefix, add_special_tokens=False)["input_ids"]
        suffix_ids = self.tokenizer(suffix, add_special_tokens=False)["input_ids"]
        
        budget_for_text = max_input - len(prefix_ids) - len(suffix_ids)
        
        text_ids = self.tokenizer(text, add_special_tokens=False)["input_ids"][:budget_for_text]
        truncated_text = self.tokenizer.decode(text_ids, skip_special_tokens=True)
        
        prompt = prefix + truncated_text + suffix
        
        inputs = self.tokenizer(
            prompt, 
            return_tensors="pt",
            truncation=False,
            padding=False
        )

        device = next(self.model.parameters()).device
        inputs = {k: v.to(device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs, 
                max_new_tokens=max_new,
                do_sample=False,
                repetition_penalty=1.1,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id
            )
        
        generated_ids = outputs[0][inputs["input_ids"].shape[1]:]
        final_summary = self.tokenizer.decode(generated_ids, skip_special_tokens=True).strip()
        
        return final_summary if final_summary else "[EMPTY OUTPUT]"