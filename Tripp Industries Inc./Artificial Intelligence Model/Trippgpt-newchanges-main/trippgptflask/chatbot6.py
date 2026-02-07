# chatbot6.py
# pip install flask
#pip install tensorflow transformers
#pip install tf-keras
# pip install TensorRT
import tensorflow as tf
from transformers import TFAutoModelForCausalLM, AutoTokenizer

class Chatbot:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("gpt2")
        self.model = TFAutoModelForCausalLM.from_pretrained("gpt2")
        self.history = []

    def generate_response(self, user_input):
        self.history.append(user_input)
        context = " ".join(self.history[-5:])
        inputs = self.tokenizer.encode(context + self.tokenizer.eos_token, return_tensors='tf')

        outputs = self.model.generate(
            inputs,
            max_length=150,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.7,
        )

        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        new_response = response[len(context):].strip()
        self.history.append(new_response)
        return new_response

