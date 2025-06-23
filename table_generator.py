def create_clean_team_table():
    RED='\033[0;31m'
    NC='\033[0m'
    try:
        with open('teams.txt', 'r') as file:
            teams = [line.strip() for line in file if line.strip()]
        
        if not teams:
            print(f"{RED}No teams found in teams.txt{NC}")
            return

        max_len = max(len(team) for team in teams)
        col_width = max(max_len, 5)
        
        # Top border
        top_border = "+" + "-"*(col_width+2) + "+" + ("-"*(col_width+2) + "+")*len(teams) + "------+--------+-----+"
        print(top_border)
        
        # Header row
        header = "|" + " "*(col_width+2) + "|"
        for team in teams:
            header += f" {team[:col_width]:^{col_width}} |"
        header += " Rank | Points | TGD |"
        print(header)
        
        # Separator
        print(top_border.replace("+", "|").replace("-", "="))
        
        # Team rows
        row_separator = "+" + "-"*(col_width+2) + "+" + ("-"*(col_width+2) + "+")*len(teams) + "------+--------+-----+"
        for team in teams:
            row = f"| {team[:col_width]:<{col_width}} |"
            for t in teams:
                row += f" {'#' if team==t else ' ':^{col_width}} |"
            row += "      |        |     |"
            print(row)
            print(row_separator)
    
    except FileNotFoundError:
        print(f"{RED}teams.txt not found{NC}")

create_clean_team_table()