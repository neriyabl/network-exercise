def cheese(board):
    if board[0][0] == 0:
        return 0
    if len(board) == 1:
        if all(board[0]):
            return 1
        return 0
    elif len(board[0]) == 1:
        if all([x[0] for x in board]):
            return 1
        return 0
    return cheese(board[1:]) + cheese([x[1:] for x in board])


def main():
    board = [
        [1, 1, 1, 1],
        [0, 1, 1, 1],
        [0, 1, 0, 1],
        [0, 1, 1, 1]
    ]
    print(cheese(board))


if __name__ == '__main__':
    main()
