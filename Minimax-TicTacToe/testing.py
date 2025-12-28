from tictactoe import player, initial_state, actions, result

player1 = player(board=initial_state())

action1 = actions(board=initial_state())
result1 = result(board=result(initial_state(), (1,2)), action=(0,1))

print(result1)