def run(file_path):
    with open(file_path) as f:
        data = f.read()
    result = {
        "filename": file_path,
        "length": len(data),
        "has_numbers": any(char.isdigit() for char in data),
        "has_letters": any(char.isalpha() for char in data),
        "summary": "Gigi tasted the file and noticed some basic features."
    }
    return result
