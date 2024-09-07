import re

def translate_to_python(rosebud_code, log_callback=None):
    python_code = []
    indent_level = 0

    def log(message):
        if log_callback:
            log_callback(message)

    for line in rosebud_code.splitlines():
        stripped_line = line.strip()
        log(f"Processing line: {stripped_line}\n")

        # Handle class definitions
        if stripped_line.startswith("class "):
            indent_level = 0
            translated_line = stripped_line.replace("{", ":").replace("class ", "class ")
            python_code.append(translated_line)
            indent_level += 1
            log(f"Translated line: {translated_line}\n")
            continue

        # Handle constructor definitions
        if stripped_line.startswith("constructor("):
            translated_line = stripped_line.replace("constructor(", "def __init__(self, ").replace(") {", "):")
            python_code.append("    " * indent_level + translated_line)
            indent_level += 1
            log(f"Translated line: {translated_line}\n")
            continue

        # Handle method definitions
        if re.match(r'^\s*[a-zA-Z_]\w*\(', stripped_line):
            translated_line = "def " + stripped_line.replace("{", ":")
            python_code.append("    " * indent_level + translated_line)
            indent_level += 1
            log(f"Translated line: {translated_line}\n")
            continue

        # Handle 'this.' to 'self.'
        if stripped_line.startswith("this."):
            translated_line = stripped_line.replace("this.", "self.")
            python_code.append("    " * indent_level + translated_line)
            log(f"Translated line: {translated_line}\n")
            continue

        # Handle 'console.log' to 'print'
        if stripped_line.startswith("console.log"):
            translated_line = stripped_line.replace("console.log", "print")
            python_code.append("    " * indent_level + translated_line)
            log(f"Translated line: {translated_line}\n")
            continue

        # Handle 'null' to 'None'
        if "null" in stripped_line:
            translated_line = stripped_line.replace("null", "None")
            python_code.append("    " * indent_level + translated_line)
            log(f"Translated line: {translated_line}\n")
            continue

        # Handle 'new' keyword
        if stripped_line.startswith("new "):
            translated_line = stripped_line.replace("new ", "")
            python_code.append("    " * indent_level + translated_line)
            log(f"Translated line: {translated_line}\n")
            continue

        # Handle semicolons
        if stripped_line.endswith(";"):
            translated_line = stripped_line[:-1]
            python_code.append("    " * indent_level + translated_line)
            log(f"Translated line: {translated_line}\n")
            continue

        # Handle closing braces
        if stripped_line == "}":
            indent_level -= 1
            continue

        # Handle dictionary-like object definitions
        if re.match(r'^\s*\w+\s*:\s*\w+', stripped_line):
            translated_line = stripped_line.replace(":", ": ")
            python_code.append("    " * indent_level + translated_line)
            log(f"Translated line: {translated_line}\n")
            continue

        # Handle async methods
        if stripped_line.startswith("async "):
            translated_line = stripped_line.replace("{", ":")
            python_code.append("    " * indent_level + translated_line)
            indent_level += 1
            log(f"Translated line: {translated_line}\n")
            continue

        # Handle const keyword
        if stripped_line.startswith("const "):
            translated_line = stripped_line.replace("const ", "")
            python_code.append("    " * indent_level + translated_line)
            log(f"Translated line: {translated_line}\n")
            continue

        # Handle array push
        if ".push(" in stripped_line:
            translated_line = stripped_line.replace(".push(", ".append(")
            python_code.append("    " * indent_level + translated_line)
            log(f"Translated line: {translated_line}\n")
            continue

        # Handle if statements
        if stripped_line.startswith("if ("):
            translated_line = stripped_line.replace("if (", "if ").replace(") {", ":")
            python_code.append("    " * indent_level + translated_line)
            indent_level += 1
            log(f"Translated line: {translated_line}\n")
            continue

        # Handle else if statements
        if stripped_line.startswith("else if ("):
            translated_line = stripped_line.replace("else if (", "elif ").replace(") {", ":")
            python_code.append("    " * (indent_level - 1) + translated_line)
            indent_level += 1
            log(f"Translated line: {translated_line}\n")
            continue

        # Handle else statements
        if stripped_line.startswith("else {"):
            translated_line = stripped_line.replace("else {", "else:")
            python_code.append("    " * (indent_level - 1) + translated_line)
            indent_level += 1
            log(f"Translated line: {translated_line}\n")
            continue

        # Handle for loops
        if stripped_line.startswith("for ("):
            translated_line = stripped_line.replace("for (", "for ").replace(") {", ":").replace(";", ", ")
            python_code.append("    " * indent_level + translated_line)
            indent_level += 1
            log(f"Translated line: {translated_line}\n")
            continue

        # Handle while loops
        if stripped_line.startswith("while ("):
            translated_line = stripped_line.replace("while (", "while ").replace(") {", ":")
            python_code.append("    " * indent_level + translated_line)
            indent_level += 1
            log(f"Translated line: {translated_line}\n")
            continue

        # Handle return statements
        if stripped_line.startswith("return "):
            translated_line = stripped_line.replace(";", "")
            python_code.append("    " * indent_level + translated_line)
            log(f"Translated line: {translated_line}\n")
            continue

        # Handle function definitions
        if re.match(r'^\s*function\s+[a-zA-Z_]\w*\(', stripped_line):
            translated_line = re.sub(r'function\s+([a-zA-Z_]\w*)\(', r'def \1(', stripped_line).replace("{", ":")
            python_code.append("    " * indent_level + translated_line)
            indent_level += 1
            log(f"Translated line: {translated_line}\n")
            continue

        # Handle method calls
        if re.match(r'^\s*[a-zA-Z_]\w*\.[a-zA-Z_]\w*\(', stripped_line):
            translated_line = stripped_line.replace(";", "")
            python_code.append("    " * indent_level + translated_line)
            log(f"Translated line: {translated_line}\n")
            continue

        # Default case: copy the line as is
        translated_line = stripped_line
        python_code.append("    " * indent_level + translated_line)
        log(f"Translated line: {translated_line}\n")

    return "\n".join(python_code)