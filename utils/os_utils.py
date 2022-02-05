

def write_text_file(path: str, content: str) -> None:
    with open(path, 'w') as file:
        file.write(content)
