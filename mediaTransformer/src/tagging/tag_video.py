import torch
from src.tagging.model import model,processor
from src.tagging.clean_text import clean_text

def describe_video(video_path:str,prompt_text:str,max_tokens:int):
    print("Describing video...",flush=True)

    # Construct prompt
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "video", "path": video_path},
                {"type": "text", "text": prompt_text},            
            ]
        },
    ]

    # Preprocess
    inputs = processor.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt",
    ).to(model.device, dtype=torch.bfloat16)

    # Generate
    generated_ids = model.generate(
        **inputs, 
        do_sample=False, 
        max_new_tokens=max_tokens,
    )

    # Decode
    generated_text = str(processor.batch_decode(
        generated_ids,
        skip_special_tokens=True,
    )[0])
    
    # Clean text
    print("Full text: ",generated_text,flush=True)
    generated_text = clean_text(generated_text)
    print("Description: ",generated_text)

    return generated_text