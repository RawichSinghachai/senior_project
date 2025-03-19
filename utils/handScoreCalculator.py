def calculate_hand_score(data):
    for i in range(len(data)):
            if data[i] is None:
                data[i] = {"left_hand_area": 0, "right_hand_area": 0}

    # data = [{left_hand_area,right_hand_area}] *4
    try:
        left_hand_front_score = (data[3]['left_hand_area'] / data[1]['left_hand_area']) * 100
    except ZeroDivisionError:
        left_hand_front_score = 0

    try:
        left_hand_back_score = (data[2]['left_hand_area'] / data[0]['left_hand_area']) * 100
    except ZeroDivisionError:
        left_hand_back_score = 0

    try:
        right_hand_front_score = (data[3]['right_hand_area'] / data[1]['right_hand_area']) * 100
    except ZeroDivisionError:
           right_hand_front_score = 0

    try:
        right_hand_back_score = (data[2]['right_hand_area'] / data[0]['right_hand_area']) * 100
    except ZeroDivisionError:
        right_hand_back_score = 0
    
    left_hand_front_score = round(left_hand_front_score, 2)
    left_hand_back_score = round(left_hand_back_score, 2)
    right_hand_front_score = round(right_hand_front_score, 2)
    right_hand_back_score = round(right_hand_back_score, 2)

    total_score = (left_hand_front_score + left_hand_back_score + right_hand_front_score + right_hand_back_score) / 4
    total_score = round(total_score,2)

    return left_hand_front_score, left_hand_back_score, right_hand_front_score, right_hand_back_score, total_score