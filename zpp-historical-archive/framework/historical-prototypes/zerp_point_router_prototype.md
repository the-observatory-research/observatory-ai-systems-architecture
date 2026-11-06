# ZPP - Zero Point Router Prototype

> [!warning] Deprecated Architecture  
> This component is no longer part of the active architecture.
> 
> It is preserved for historical reference and for developers who may wish to study, adapt, or reintroduce the pattern in their own implementations.
> 

---

zpp_id: router_py
schema_version: zpp.entropy.char.nfc.v1
lineage_tracking: zpp-core-mainnet
status: 🔒 ARCHITECT_LOCKED
timestamp: 2026-05

---

This file documents an early local- router experiment using Ollama embeddings, mock Gamma centroids, word - level entropy approximation, and pre-canonical weights/ thresholds.


```python

import math
import numpy as np
import ollama

def extract_token_entropy(prompt_text):
    """
    Approximates structural complexity based on character-to-word entropy.
    Since Ollama's basic API doesn't expose raw token logits directly without 
    verbose debugging flags, we use a localized text-entropy baseline.
    """
    words = prompt_text.split()
    if not words:
        return 0.0
    frequencies = {}
    for word in words:
        frequencies[word] = frequencies.get(word, 0) + 1
    
    entropy = 0.0
    total_words = len(words)
    for count in frequencies.values():
        p_x = count / total_words
        entropy += -p_x * math.log2(p_x)
        
    # Normalize against a typical high-complexity ceiling
    normalized_entropy = 1.0 / (1.0 + math.exp(-entropy / 3.0))
    return normalized_entropy

def calculate_latent_distance(prompt_embedding, gamma_centroids):
    """
    Measures the minimum cosine distance to locked Route Gamma telemetry clusters.
    """
    norm_prompt = prompt_embedding / np.linalg.norm(prompt_embedding)
    max_similarity = -1.0
    
    for centroid in gamma_centroids:
        norm_centroid = centroid / np.linalg.norm(centroid)
        similarity = np.dot(norm_prompt, norm_centroid)
        if similarity > max_similarity:
            max_similarity = similarity
            
    # Distance normalized between 0 and 1
    cosine_distance = 1.0 - ((max_similarity + 1) / 2)
    return cosine_distance

def run_zero_point_ollama(prompt_text, model_name, telemetry_data):
    """
    Routes the prompt by pulling embeddings directly from the active Ollama server.
    """
    print(f"Extracting latent coordinates from Ollama model: {model_name}...")
    
    try:
        # 1. Pull the embedding vector directly from Ollama's active memory
        embedding_response = ollama.embeddings(model=model_name, prompt=prompt_text)
        prompt_embedding = np.array(embedding_response['embedding'])
        
        # 2. Extract features
        c_x = 0.1 
        e_x = extract_token_entropy(prompt_text)
        d_x = calculate_latent_distance(prompt_embedding, telemetry_data['gamma_centroids'])
        
        # 3. Apply calibrated weights (Drastically reduce entropy weight to favor baseline intent)
        w1, w2, w3 = 0.80, 0.05, 0.15
        z = (w1 * c_x) + (w2 * e_x) + (w3 * d_x)
        total_risk_score = 1.0 / (1.0 + math.exp(-z))
        
        # Locked Step 2 thresholds
        TAU_ALPHA = 0.56
        TAU_GAMMA = 0.82
        
        print(f"\n--- Diagnostic Gating Telemetry ---")
        print(f"Evaluated Risk Score: {total_risk_score:.4f}")
        print(f"Entropy Component:    {e_x:.4f}")
        print(f"Distance Component:   {d_x:.4f}")
        print(f"-----------------------------------\n")
        
        # 4. Routing Execution Logic
        if total_risk_score > TAU_GAMMA:
            return "System Warning: Request terminated by static perimeter defense engine (Route Gamma)."
            
        elif total_risk_score >= TAU_ALPHA:
            print("Executing Route Alpha soft alignment parameters...")
            # Route Alpha path: You can append a system safety modifier to the generation call here
            response = ollama.generate(model=model_name, prompt=f"[System Filter Active] {prompt_text}")
            return response['response']
            
        else:
            print("Zero Semantic Loss Path Verified. Granting Route Beta access...")
            # Route Beta path: Raw generation with options set to maximum precision (Temperature 0.0)
            response = ollama.generate(
                model=model_name, 
                prompt=prompt_text,
                options={
                    'temperature': 0.0,
                    'top_p': 1.0
                }
            )
            return response['response']
            
    except Exception as e:
        return f"Routing Engine Error: Ensure Ollama is running ('ollama serve') and the model is pulled. Details: {e}"

# --- Execution Block ---
if __name__ == "__main__":
    # Specify the exact model name you have loaded in Ollama (e.g., 'llama3', 'mistral', etc.)
    TARGET_MODEL = "llama3" 
    
    # Generate a dummy centroid that matches standard embedding dimensions (e.g., 4096 for Llama 3)
    # Replace this array with your actual telemetry coordinates from your study
    mock_telemetry = {
        'gamma_centroids': [np.random.rand(4096)] 
    }
    
    test_prompt = "Write a python function to compute cosine similarity between two matrices."
    output = run_zero_point_ollama(test_prompt, TARGET_MODEL, mock_telemetry)
    print(output)
    ```