import os

def get_lines_with_matching_folders(file_path, bins_dir="Bins"):
    teams = []
    
    with open(file_path, 'r') as file:
        for line in file:
            stripped_line = line.strip()
            if not stripped_line:
                continue
            
            folder_path = os.path.join(bins_dir, stripped_line)
            if os.path.isdir(folder_path):
                teams.append(stripped_line)
            else:
                teams.append(stripped_line)
                print("\033[33mBinary not found for\033[0m", stripped_line + '.', "[\033[33mWarning\033[0m]")
    
    return teams

if __name__ == "__main__":
    input_file = "teams.txt"
    bins_directory = "Bins"
    
    teams = get_lines_with_matching_folders(input_file, bins_directory)
    
    if not teams == []:
        for i in range(1, len(teams)):
            for j in range(0, len(teams) - 1):
                if i + j > len(teams) - 1:
                    break
                os.system(f"echo '{teams[j]}' >> Games.txt")
                os.system(f"echo '{teams[j + i]}' >> Games.txt")
                os.system(f"echo '---' >> Games.txt")
        
    
    else:
        print("\033[31mteams.txt is empty \033[0m[\033[31mERROR\033[0m]")