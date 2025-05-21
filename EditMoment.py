def remove_spaces_and_empty_lines(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Remove leading and trailing spaces from each line
    lines = [line.strip() for line in lines]

    # Remove empty lines
    lines = [line for line in lines if line]

    with open(output_file, 'w') as file:
        file.write('\n'.join(lines))

input_file = 'Games.txt'
output_file = 'G.txt'
remove_spaces_and_empty_lines(input_file, output_file)