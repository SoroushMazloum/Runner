import os
import re

def get_latest_rcg_file():
    rcg_files = [f for f in os.listdir('.') if f.endswith('.rcg')]
    if not rcg_files:
        return None
    return max(rcg_files, key=os.path.getctime)

def parse_match_result(filename):
    pattern = r'(\d{8}\d+)-(.+?)_(\d+)(?:_(\d+))?-vs-(.+?)_(\d+)(?:_(\d+))?\.rcg'
    match = re.match(pattern, filename)
    
    if not match:
        return None
    
    team1 = match.group(2)
    team1_score = int(match.group(3))
    team1_penalty = int(match.group(4)) if match.group(4) else None
    
    team2 = match.group(5)
    team2_score = int(match.group(6))
    team2_penalty = int(match.group(7)) if match.group(7) else None
    
    return {
        'team1': team1,
        'team1_score': team1_score,
        'team1_penalty': team1_penalty,
        'team2': team2,
        'team2_score': team2_score,
        'team2_penalty': team2_penalty
    }

def determine_winner(match_data):
    if match_data['team1_score'] > match_data['team2_score']:
        return match_data['team1']
    elif match_data['team1_score'] < match_data['team2_score']:
        return match_data['team2']
    else:
        if match_data['team1_penalty'] is not None and match_data['team2_penalty'] is not None:
            if match_data['team1_penalty'] > match_data['team2_penalty']:
                return match_data['team1']
            else:
                return match_data['team2']
        else:
            return "Draw (no penalties)"

def result(match_data):
    result = None
    if match_data['team1_penalty'] is not None and match_data['team2_penalty'] is not None:
        result = f"{match_data['team1']} {match_data['team1_score']}({match_data['team1_penalty']}) - ({match_data['team2_penalty']}){match_data['team2_score']} {match_data['team2']}"
    else:
        result = f"{match_data['team1']} {match_data['team1_score']} - {match_data['team2']} {match_data['team2_score']}"
        
    os.system(f"echo '{result}' >> Results.txt")
    
def main():
    filename = get_latest_rcg_file()
    if not filename:
        print("No .rcg file found.")
        return
    
    parsed_match_result = parse_match_result(filename)
    print(determine_winner(parsed_match_result))
    result(parsed_match_result)

if __name__ == "__main__":
    main()