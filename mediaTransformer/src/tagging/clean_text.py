def clean_text(text:str):
    """Keep only the first sentence of the generated text."""
    # Remove text before the last ":"
    text = text.split(":")[-1].strip()
    # Remove text after the last dot (cut sentences)
    text = remove_after_last_dot(text)
    return text

def remove_after_last_dot(input_string):
    # Find the last occurrence of '.'
    last_dot_index = input_string.rfind('.')
    
    # If '.' is found, return the string up to that index
    if last_dot_index != -1:
        return input_string[:last_dot_index]
    # Otherwise, return the original string
    else:
        return input_string