import requests
import guidance.models as models
from guidance.chat import Llama3ChatTemplate
model_url = f"https://huggingface.co/bartowski/Meta-Llama-3.1-8B-Instruct-GGUF/resolve/main/Meta-Llama-3.1-8B-Instruct-IQ4_XS.gguf"

import os

if __name__ == "__main__":
    if not os.path.exists("model.gguf"):
        try:
            with requests.get(model_url, stream=True) as response:
                response.raise_for_status()
                with open("model.gguf", 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
            print("File downloaded successfully!")
        except requests.exceptions.RequestException as e:
            print("Error downloading the file:", e)
    else:
        print("Model already downloaded")
      
try:  
    loaded_model = models.LlamaCpp(model=f"D:\Studia\Fake-db-generator\Meta-Llama-3.1-8B-Instruct-IQ4_XS.gguf",
                               echo=False,
                               chat_template=Llama3ChatTemplate,
                               n_gpu_layers=20, # Lower it if you get VRAM oom errors
                               )
except Exception as e:
    pass
