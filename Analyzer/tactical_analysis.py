import os
import json
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Patch
import numpy as np

MAIN_OUTPUT_DIR = 'Results_analysis'
os.makedirs(MAIN_OUTPUT_DIR, exist_ok=True)

def draw_field(ax):
    ax.set_xlim(0, 120)
    ax.set_ylim(0, 80)
    ax.set_facecolor('#2e8b57')
    ax.set_aspect('equal')
    ax.axis('off')

    ax.plot([0, 0, 120, 120, 0], [0, 80, 80, 0, 0], color='white', linewidth=2)
    ax.plot([60, 60], [0, 80], color='white', linewidth=2)
    
    ax.plot([0, 18, 18, 0], [30, 30, 50, 50], color='white')
    ax.plot([102, 120, 120, 102], [30, 30, 50, 50], color='white')
    ax.plot([102, 102], [30, 50], color='white')
    
    center_circle = Circle((60, 40), 10, color='white', fill=False, linewidth=2)
    ax.add_patch(center_circle)
    
    regions = {
        'A': (15, 65), 'B': (15, 40), 'C': (15, 15),
        'D': (60, 65), 'E': (60, 40), 'F': (60, 15),
        'G': (105, 65), 'H': (105, 40), 'I': (105, 15)
    }
    
    for region, pos in regions.items():
        ax.text(
            pos[0], pos[1], region, color='white', 
            fontsize=12, ha='center', va='center', weight='bold',
            bbox=dict(facecolor='black', alpha=0.5, boxstyle='round')
        )

def draw_heatmap_on_field(ax, left_team_name, right_team_name, left_region_data, right_region_data):
    all_values = list(left_region_data.values()) + list(right_region_data.values())
    max_value = max(all_values) if all_values else 1
    if max_value == 0:
        max_value = 1
    norm = plt.Normalize(0, max_value)
    
    cmap_left = plt.cm.Blues
    cmap_right = plt.cm.Reds
    
    region_width = 30
    region_height = 80 / 3.25
    
    regions = {
        'A': (15, 65), 'B': (15, 40), 'C': (15, 15),
        'D': (60, 65), 'E': (60, 40), 'F': (60, 15),
        'G': (105, 65), 'H': (105, 40), 'I': (105, 15)
    }
    
    for region_letter, center in regions.items():
        x_center, y_center = center
        x0 = x_center - region_width / 2
        y0 = y_center - region_height / 2
        
        left_value = left_region_data.get(region_letter, 0)
        left_color = cmap_left(norm(left_value))
        rect_left = Rectangle(
            (x0, y0), 
            width=region_width/2, 
            height=region_height, 
            color=left_color, 
            alpha=0.7,
            zorder=1
        )
        ax.add_patch(rect_left)
        
        right_value = right_region_data.get(region_letter, 0)
        right_color = cmap_right(norm(right_value))
        rect_right = Rectangle(
            (x0 + region_width/2, y0), 
            width=region_width/2, 
            height=region_height, 
            color=right_color, 
            alpha=0.7,
            zorder=1
        )
        ax.add_patch(rect_right)
        
        ax.text(
            x0 + region_width/4, y0 + region_height/2,
            f'{left_value}', 
            ha='center', va='center', 
            color='black',
            fontsize=8,
            zorder=10
        )
        ax.text(
            x0 + 3*region_width/4, y0 + region_height/2,
            f'{right_value}', 
            ha='center', va='center', 
            color='black',
            fontsize=8,
            zorder=10
        )
    
    legend_elements = [
        Patch(facecolor=cmap_left(0.7), label=f'{left_team_name}'),
        Patch(facecolor=cmap_right(0.7), label=f'{right_team_name}')
    ]
    ax.legend(
        handles=legend_elements, 
        loc='lower center',
        bbox_to_anchor=(0.5, -0.05),
        ncol=2, 
        fontsize=9
    )

def aggregate_region_data(region_data_dict):
    region_cycles = {region: 0 for region in 'ABCDEFGHI'}
    if not region_data_dict:
        return region_cycles
    
    for player_id, regions in region_data_dict.items():
        for region_letter, region_info in regions.items():
            if region_letter in region_cycles:
                cycles = region_info.get('positionCycles', 0)
                region_cycles[region_letter] += int(cycles)
    return region_cycles
def get_passing_data(team_data):
    if not isinstance(team_data, dict):
        return {
            'length': 0,
            'width': 0,
            'true': 0,
            'wrong': 0,
            'accuracy': 0,
            'interceptions': 0
        }
    
    keys = ['passInLength', 'passinLength', 'passInWidth']
    try:
        length = team_data.get(keys[0]) or team_data.get(keys[1], 0)
        width = team_data.get(keys[2], 0)
        true = team_data.get('truePass', 0)
        wrong = team_data.get('wrongPass', 0)
        accuracy = team_data.get('passAccuracy', 0)
        interceptions = team_data.get('intercept', team_data.get('Intercept', 0))
        
        return {
            'length': length,
            'width': width,
            'true': true,
            'wrong': wrong,
            'accuracy': accuracy,
            'interceptions': interceptions
        }
    except Exception:
        return {
            'length': 0,
            'width': 0,
            'true': 0,
            'wrong': 0,
            'accuracy': 0,
            'interceptions': 0
        }

def parse_ranking_file(file_path='Table.txt'):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        return None, False
    
    is_extended_format = False
    for line in lines:
        if 'GF' in line and 'GA' in line and 'GD' in line and 'P' in line:
            is_extended_format = True
            break
    
    teams = []
    
    if is_extended_format:
        for line in lines:
            if not line.strip() or '----' in line or 'Team' in line and 'GF' in line:
                continue
                
            parts = line.split()
            if not parts[0].isdigit():
                continue
                
            rank = parts[0]
            
            team_end_index = len(parts) - 7
            
            team_name = ' '.join(parts[1:team_end_index])
            
            stats = parts[team_end_index:team_end_index+7]
            
            teams.append({
                'rank': rank,
                'team': team_name,
                'W': stats[0],
                'D': stats[1],
                'L': stats[2],
                'GF': stats[3],
                'GA': stats[4],
                'GD': stats[5],
                'P': stats[6]
            })
    else:
        for line in lines:
            if not line.strip() or '----' in line or 'Team' in line:
                continue
                
            parts = line.split()
            if not parts or not parts[0].isdigit():
                continue
                
            rank = parts[0]
            team_name = ' '.join(parts[1:])
            teams.append({
                'rank': rank,
                'team': team_name
            })
    
    return teams, is_extended_format

def draw_ranking_table(ax, ranking_data, is_extended_format, left_team_name, right_team_name):
    ax.set_axis_off()
    
    if not ranking_data:
        ax.text(0.5, 0.5, "No ranking data available", 
                ha='center', va='center', fontsize=12)
        return
    
    try:
        if is_extended_format:
            col_labels = ['Rank', 'Team', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'P']
            col_widths = [0.05, 0.35, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]
        else:
            col_labels = ['Rank', 'Team']
            col_widths = [0.1, 0.9]
        
        cell_data = []
        teams_in_ranking = []

        for team in ranking_data:
            row = [team['rank'], team['team']]
            if is_extended_format:
                row.extend([
                    team.get('W', '0'),
                    team.get('D', '0'),
                    team.get('L', '0'),
                    team.get('GF', '0'),
                    team.get('GA', '0'),
                    team.get('GD', '0'),
                    team.get('P', '0')
                ])
            cell_data.append(row)
            teams_in_ranking.append(team['team'])

        left_in_ranking = left_team_name in teams_in_ranking
        right_in_ranking = right_team_name in teams_in_ranking
        
        if not (left_in_ranking and right_in_ranking):
            missing_teams = []
            if not left_in_ranking:
                missing_teams.append(left_team_name)
            if not right_in_ranking:
                missing_teams.append(right_team_name)
                
            ax.text(0.5, 0.5, f"Teams not in ranking: {', '.join(missing_teams)}", 
                    ha='center', va='center', fontsize=12, color='red')
            return
        
        table = ax.table(
            cellText=cell_data,
            colLabels=col_labels,
            colWidths=col_widths,
            cellLoc='center',
            loc='center'
        )
        
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 1.5)
        
        for i, label in enumerate(col_labels):
            cell = table[0, i]
            cell.set_facecolor('#1f77b4')
            cell.set_text_props(color='white', weight='bold')
        
        for i in range(1, len(cell_data) + 1):
            color = '#f0f0f0' if i % 2 == 1 else '#ffffff'
            team_name = cell_data[i-1][1]
            
            text_color = 'black'
            cell_color = color
            
            if team_name == left_team_name:
                cell_color = '#e6f0ff'
                text_color = '#1f77b4'
            elif team_name == right_team_name:
                cell_color = '#ffe6e6'
                text_color = '#d62728'
            
            for j in range(len(col_labels)):
                cell = table[i, j]
                cell.set_facecolor(cell_color)
                
                if j == 1:
                    cell.get_text().set_color(text_color)
                    cell.get_text().set_weight('bold')
        
        ax.set_title('Tournament Standings', fontsize=14, pad=20, weight='bold')
    
    except Exception as e:
        ax.text(0.5, 0.5, f"Error drawing table: {str(e)}", 
                ha='center', va='center', fontsize=12, color='red')

def plot_passing_pattern(team_data, team_name, ax):
    try:
        data = get_passing_data(team_data)
        
        if not data or (data['length'] == 0 and data['width'] == 0):
            ax.text(0.5, 0.5, "No Passing Data", ha='center', va='center', fontsize=14)
            ax.set_title(f'Passing Pattern - {team_name}', fontsize=12)
            return
        
        wedges, texts, autotexts = ax.pie(
            [data['length'], data['width']],
            labels=['Length Passes', 'Width Passes'],
            autopct=lambda p: f'{p:.1f}%\n({int(p/100*(data["length"]+data["width"]))})',
            startangle=90,
            colors=['#1f77b4', '#ff7f0e'],
            wedgeprops={'edgecolor': 'black', 'linewidth': 1},
            textprops={'fontsize': 10}
        )
        
        plt.setp(autotexts, size=10, weight='bold')
        
        title = (
            f'Passing Pattern: {team_name}\n'
            f'Correct: {data["true"]} | Wrong: {data["wrong"]}\n'
            f'Accuracy: {data["accuracy"]}% | Interceptions: {data["interceptions"]}'
        )
        ax.set_title(title, fontsize=11, pad=20)
    except Exception as e:
        ax.text(0.5, 0.5, f"Error: {str(e)}", ha='center', va='center', fontsize=12, color='red')
        ax.set_title(f'Passing Pattern - {team_name} (Error)', fontsize=12)

def plot_defensive_strengths(left_team, right_team, ax):
    try:
        left_data = get_passing_data(left_team)
        right_data = get_passing_data(right_team)
        
        teams = [left_team.get('leftTeam', 'Left Team'), 
                 right_team.get('rightTeam', 'Right Team')]
        
        interceptions = [left_data['interceptions'], right_data['interceptions']]
        colors = ['#1f77b4', '#d62728']
        
        bars = ax.bar(teams, interceptions, color=colors, edgecolor='black')
        ax.set_title('Defensive Interceptions', fontsize=14, weight='bold', pad=15)
        ax.set_ylabel('Number of Interceptions', fontsize=11)
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        
        for i, bar in enumerate(bars):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height/2, 
                    f'{int(height)}', ha='center', va='center', 
                    fontsize=16, weight='bold', color='white')
            
    except Exception as e:
        ax.text(0.5, 0.5, f"Error: {str(e)}", ha='center', va='center', fontsize=12, color='red')
        ax.set_title('Defensive Interceptions (Error)', fontsize=14)

def get_shooting_data(team_data):
    if not isinstance(team_data, dict):
        return {
            'on_target': 0,
            'off_target': 0,
            'accuracy': 0,
            'goals': 0
        }
    
    try:
        return {
            'on_target': team_data.get('onTargetShoot', 0),
            'off_target': team_data.get('offTarget', 0),
            'accuracy': team_data.get('shootAccuracy', 0),
            'goals': team_data.get('goals', 0)
        }
    except Exception:
        return {
            'on_target': 0,
            'off_target': 0,
            'accuracy': 0,
            'goals': 0
        }

def plot_shooting_positions(team_data, team_name, ax, is_left_team):
    try:
        data = get_shooting_data(team_data)

        summary_text = (
            f'{team_name}:\n'
            f'On Target: {data["on_target"]}\n'
            f'Off Target: {data["off_target"]}\n'
            f'Goals: {data["goals"]}\n'
            f'Accuracy: {data["accuracy"]}%'
        )

        pos_x = 20 if is_left_team else 100
        pos_y = 95

        ax.text(pos_x, pos_y, summary_text, 
                fontsize=10, color='white', weight='bold',
                bbox=dict(facecolor='#1f77b4' if is_left_team else '#d62728',
                          alpha=0.85, boxstyle='round,pad=0.4'),
                ha='center', va='top')
                
    except Exception:
        pass

def process_json_files(directory):

    ranking_data, is_extended_format = parse_ranking_file()
    
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except Exception as e:
                print(f"\033[0;31mError processing {filename}: {str(e)}\033[0m")
                continue
                
            match_name = os.path.splitext(filename)[0]
            match_dir = os.path.join(MAIN_OUTPUT_DIR, match_name)
            os.makedirs(match_dir, exist_ok=True)

            left_team = data.get('leftTeam', {})
            right_team = data.get('rightTeam', {})
            game_result = data.get('gameResult', {})
            left_region_data = aggregate_region_data(left_team.get('regionData', {}))
            right_region_data = aggregate_region_data(right_team.get('regionData', {}))
            
            left_team_name = left_team.get('leftTeam', 'Left Team')
            right_team_name = right_team.get('rightTeam', 'Right Team')
            
            left_score = game_result.get(left_team_name, 0)
            if not isinstance(left_score, (int, float)):
                left_score = 0
                
            right_score = game_result.get(right_team_name, 0)
            if not isinstance(right_score, (int, float)):
                right_score = 0
            
            try:
                fig = plt.figure(figsize=(16, 18), facecolor='#f0f0f0')
                plt.suptitle(
                    f"TACTICAL ANALYSIS: {left_team_name} {left_score}-{right_score} {right_team_name}", 
                    fontsize=20, weight='bold', y=0.97
                )
                
                plt.figtext(
                    0.5, 0.94,
                    f"Possession: {left_team.get('possession', 0)}%-{right_team.get('possession', 0)}% | "
                    f"Shots: {left_team.get('onTargetShoot', 0)+left_team.get('offTarget', 0)}-"
                    f"{right_team.get('onTargetShoot', 0)+right_team.get('offTarget', 0)} | "
                    f"Pass Accuracy: {left_team.get('passAccuracy', 0)}%-{right_team.get('passAccuracy', 0)}%",
                    ha='center', fontsize=14, color='#333333'
                )
                
                gs = fig.add_gridspec(3, 2, height_ratios=[1, 1.5, 0.8], 
                                      width_ratios=[1, 1.5], 
                                      hspace=0.15, wspace=0.15)
                
                ax1 = fig.add_subplot(gs[0, 0])
                ax2 = fig.add_subplot(gs[0, 1])
                ax3 = fig.add_subplot(gs[1, 0])
                ax4 = fig.add_subplot(gs[1, 1])
                ax5 = fig.add_subplot(gs[2, :])
                
                plot_passing_pattern(left_team, left_team_name, ax1)
                plot_passing_pattern(right_team, right_team_name, ax2)
                
                plot_defensive_strengths(left_team, right_team, ax3)
                
                draw_field(ax4)
                draw_heatmap_on_field(ax4, left_team_name, right_team_name, left_region_data, right_region_data)
                plot_shooting_positions(left_team, left_team_name, ax4, True)
                plot_shooting_positions(right_team, right_team_name, ax4, False)

                draw_ranking_table(ax5, ranking_data, is_extended_format, left_team_name, right_team_name)
                
                handles, labels = ax4.get_legend_handles_labels()
                unique_labels = dict(zip(labels, handles))
                if unique_labels:
                    ax4.legend(
                        unique_labels.values(), unique_labels.keys(),
                        loc='upper center', bbox_to_anchor=(0.5, -0.05),
                        ncol=2, fontsize=9, framealpha=0.8
                    )
                
                plt.figtext(
                    0.5, 0.02, 
                    f"Generated from {filename}",
                    ha='center', fontsize=10, color='#666666'
                )
                
                output_path = os.path.join(match_dir, f"{match_name}_analysis.png")
                plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
                plt.close()
                print(f'\033[1;33mCreated professional diagram\033[0m: \033[0;32m{output_path}\033[0m')
                
            except Exception as e:
                print(f"\033[0;31mFailed to create diagram for {filename}: {str(e)}\033[0m")
                plt.close('all')

if __name__ == "__main__":
    input_dir = 'LogsJSON'
    
    if not os.path.exists(MAIN_OUTPUT_DIR):
        os.makedirs(MAIN_OUTPUT_DIR)
        print(f"\033[1;33mCreated main output directory: {MAIN_OUTPUT_DIR}\033[0m")
    
    process_json_files(input_dir)
    print("\033[0;32mAnalysis complete! All results saved in:", MAIN_OUTPUT_DIR, "\033[0m")