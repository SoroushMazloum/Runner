import loganalyzer
from loganalyzer import Parser
from loganalyzer import Game
from loganalyzer import Analyzer
import os


path = os.path.dirname(os.path.realpath(__file__))
file_names = ""
for file in os.listdir(path):
    if file.endswith('.rcg'):
        file_name = os.path.splitext(file)[0]  # Extract the file name without extension
        file_names += file_name + ", "

# Remove the trailing comma and space
file_names = file_names[:-2]

parser = Parser(file_names)
game = Game(parser)
analyzer = Analyzer(game)
analyzer.analyze()
result = analyzer.game.left_team.name + ' ' + str(analyzer.game.left_goal) + ' vs ' + str(analyzer.game.right_goal) + ' ' + analyzer.game.right_team.name
os.system(f"echo '{result}' >> Results.txt")
if analyzer.game.right_goal > analyzer.game.left_goal:
    print(analyzer.game.right_team.name)
elif analyzer.game.right_goal < analyzer.game.left_goal:
    print(analyzer.game.left_team.name)
else :
    print('NONE')
