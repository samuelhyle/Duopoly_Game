from random import randint


def ultra(data):

    f_data = []

    for bits in data:

        ko = []

        last = bits[0]
        sec = bits[1]
        most = bits[2]
        w1 = bits[3]
        w2 = bits[4]
        ko.append(most)

        if last == sec:

            if last == most:

                f1 = 0.66
                ko.append(f1)

            elif last != most:

                f1 = 0.33
                ko.append(f1)

        elif last != sec:

            if last == most:

                f1 = 0.5
                ko.append(f1)

            elif last != most:
                if most == 0:
                    f1 = 0.5
                    ko.append(f1)
                elif most != 0:
                    f1 = 0.33
                    ko.append(f1)


    return f_data


def process(players):

    data = []

    for player in players:

        player_data = []
        one = []
        two = []
        last_move = player[len(player) - 1]
        sec_last_move = player[len(player) - 1]
        player_data.append(last_move)
        player_data.append(sec_last_move)

        for moves in player:
            if moves == 1:
                one.append(moves)
            elif moves == 2:
                two.append(moves)
            else:
                pass

        total = len(one) + len(two)

        if len(one) > len(two):
            player_data.append(1)
            most_weigth = len(one) / total
            least_weight = len(two) / total
            player_data.append(most_weigth)
            player_data.append(least_weight)
        elif len(one) < len(two):
            player_data.append(2)
            most_weight = len(two) / total
            least_weight = len(one) / total
            player_data.append(most_weight)
            player_data.append(least_weight)
        elif len(one) == len(two):
            player_data.append(0)
            player_data.append(0.5)
            player_data.apppend(0.5)

        data.append(player_data)

    return data


def gert(data):
    w = []

    for ros in data:
        most = ros[0]
        f = ros[1]

        weight = randint(1, 100) / 100

        if weight < f:
            if most == 1:
                w.append(1)
            elif most == 2:
                w.append(2)
            elif most == 0:
                w.append(randint(1, 2))

        elif weight > f:

            if most == 1:
                w.append(2)
            elif most == 2:
                w.append(1)
            elif most == 0:
                w.append(randint(1, 2))

    return w


def get_moves(players):

    if len(players[0]) == 0:

        return [randint(1, 2), randint(1, 2)]

    else:

        data = process(players)
        f_d = ultra(data)

        xd = gert(f_d)

        return xd