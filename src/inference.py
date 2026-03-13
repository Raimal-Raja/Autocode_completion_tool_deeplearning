import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

_HERE = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(_HERE, "../model/fine_tuned")

_tokenizer = None
_model = None
_device = None


def load_model():
    global _tokenizer, _model, _device
    if _model is not None:
        return
    _device = "cuda" if torch.cuda.is_available() else "cpu"
    _tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    _model = AutoModelForCausalLM.from_pretrained(MODEL_PATH)
    _model.to(_device)
    _model.eval()
    print(f"Model loaded on {_device}")


def get_completion(prompt, max_new_tokens=50, temperature=0.7, top_p=0.95, num_lines=3):
    load_model()
    inputs = _tokenizer.encode(prompt, return_tensors="pt").to(_device)
    with torch.no_grad():
        outputs = _model.generate(
            inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=temperature,
            top_p=top_p,
            pad_token_id=_tokenizer.eos_token_id,
        )
    new_tokens = outputs[0][inputs.shape[-1]:]
    completion = _tokenizer.decode(new_tokens, skip_special_tokens=True)
    lines = completion.split("\n")[:num_lines]
    return "\n".join(lines)