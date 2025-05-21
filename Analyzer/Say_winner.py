import os
import re

def get_latest_rcg_file():
    rcg_files = [f for f in os.listdir('.') if f.endswith('.rcg')]
    if not rcg_files:
        return None
    return max(rcg_files, key=os.path.getctime)

def get_winner_from_filename(filename):
    name = os.path.splitext(filename)[0]
    match = re.match(r'\d+-([\w\-]+)_(\d+)-vs-([\w\-]+)_(\d+)', name)
    if not match:
        return "Invalid filename format"
    
    team1, score1, team2, score2 = match.group(1), int(match.group(2)), match.group(3), int(match.group(4))
    if score1 > score2:
        winner = team1
    elif score2 > score1:
        winner = team2
    else:
        winner = "Draw"
    return f"{team1}\t{score1} : {score2}\t{team2}\t-> {winner}"

def main():
    filename = get_latest_rcg_file()
    if not filename:
        print("No .rcg file found.")
        return
    print(get_winner_from_filename(filename))

if __name__ == "__main__":
    main()
