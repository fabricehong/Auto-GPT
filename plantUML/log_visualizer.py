def replace_nth_space(s, n):
    words = s.split(" ")
    result = []

    for i, word in enumerate(words):
        result.append(word)
        if (i + 1) % n == 0 and (i + 1) != len(words):
            result.append("\n")
        else:
            if (i + 1) != len(words):
                result.append(" ")

    return "".join(result)

def event_logs_to_plantuml(logs: str) -> str:
    lines = logs.split("\n")
    diagram = "@startuml\n!pragma useBeta\n\nstart"

    for i, line in enumerate(lines):
        if "REASONING" in line:
            reasoning = line.replace("REASONING: ", "")
            reasoning = replace_nth_space(reasoning, 6)
            diagram += f'\n#yellow:{reasoning};'

        elif "NEXT ACTION" in line:
            command = line.split("COMMAND = ")[1].split("  ")[0]
            arguments = line.split("ARGUMENTS = ")[1]
            arguments = arguments.replace("{", "").replace("}", "").replace("'", "")

            diagram += f'\n#lightBlue:{command};'

            if i + 1 < len(lines) and "SYSTEM" in lines[i + 1]:
                system_line = lines[i + 1]
                result = system_line.split("returned: ")[1]

                # Truncate strings if they are too long
                max_length = 70
                args = arguments.split(", ")
                args = [arg[:max_length] + "..." if len(arg) > max_length else arg for arg in args]
                formatted_args = "\n  - ".join(args)

                if "[" in result and "]" in result:
                    result = result.replace("[", "").replace("]", "").replace("'", "")
                    results = result.split(", ")
                    results = [res[:max_length] + "..." if len(res) > max_length else res for res in results]
                    formatted_result = "\n  - ".join(results)
                else:
                    formatted_result = result[:max_length] + "..." if len(result) > max_length else result

                diagram += f'\nnote right\n  args :\n  - {formatted_args}\n  returned:\n  - {formatted_result}\nend note'

    diagram += "\nstop\n\n@enduml"
    return diagram

import re

def prune_log_file(input_file: str, output_file: str) -> None:
    pattern = r'((?:REASONING:|SYSTEM:|NEXT ACTION:).*)'

    with open(input_file, 'r') as in_file:
        content = in_file.read()
        matches = re.findall(pattern, content)

    with open(output_file, 'w') as out_file:
        for match in matches:
            out_file.write(match.strip() + '\n')

def create_plant_uml_diagram(input_file: str, output_file: str) -> None:


    with open(input_file, 'r') as in_file:
        content = in_file.read()

    diagram = event_logs_to_plantuml(content)

    with open(output_file, 'w') as out_file:
        out_file.write(diagram)



def main():
    prune_log_file('log.log', 'log_prunned.log')
    create_plant_uml_diagram('log_prunned.log', 'diagram.log')

if __name__ == "__main__":
    main()