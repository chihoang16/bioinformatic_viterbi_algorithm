import random
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def genDieNumbers(n):
    ##CHOOSING STATE:
    #Setting starting state:
    prev_state = ""
    state_list = []

    #choosing state based on previous states
    for i in range(n):
        if prev_state == "":
            this_state = random.randint(0, 1)
            # print(this_state)
            if this_state == 0:
                prev_state = "F"
            elif this_state == 1:
                prev_state = "L"
            else:
                raise ValueError("Invalid state: Die can only be fair or loaded")
        elif prev_state == "F":
            this_state = random.randint(0, 9)
            # print(this_state)
            if this_state == 0:
                prev_state = "L"
            elif (this_state <= 9) and (this_state >= 0):
                prev_state = "F"
            else:
                raise ValueError("Invalid state: Die can only be fair or loaded")
        elif prev_state == "L":
            this_state = random.randint(0, 9)
            if (this_state < 2) and (this_state >= 0):
                prev_state = "F"
            elif this_state <= 9:
                prev_state = "L"
            else:
                raise ValueError("Invalid state: Die can only be fair or loaded")
        else:
            raise ValueError("Invalid state: Die can only be fair or loaded")
        
        
        if (prev_state == "F"):
            this_roll = random.randint(1, 6)
        elif (prev_state == "L"):
            this_roll = random.randint(1, 10)
            if this_roll > 5:
                this_roll = 6

        this_turn = (prev_state, this_roll)
        state_list.append(this_turn)

            
        
    return state_list

def calculateRollProbability(roll, currState):
    if currState == "F":
        return 1/6
    elif currState == "L" and roll == 6:
        return 1/2
    else:
        return 1/10
    
def calculateStateChange(prevState, currState):
    if prevState == "F":
        if currState == "F":
            return 0.9
        elif currState == "L":
            return 0.1
        else:
            raise ValueError("Invalid state: Die can only be fair or loaded")
    elif prevState == "L":
        if currState == "F":
            return 0.2
        elif currState == "L":
            return 0.8
        else:
            raise ValueError("Invalid state: Die can only be fair or loaded")
    else:
        raise ValueError("Invalid state: Die can only be fair or loaded")

def viterbi(all_list):
    NUM_ROLLS = len(all_list)
    roll_list = []
    state_list = []
    possible_states = ["F", "L"]
    ROLL_IDX = 1
    STATE_IDX = 0

    for i in range(len(all_list)):
        roll_list.append(all_list[i][ROLL_IDX])
        state_list.append(all_list[i][STATE_IDX])

    ##Settnig up matrix
    viterbi_matrix = []

    ##Calculating first column
    initial_state_change_probability = 1 / len(possible_states)

    for i in range(len(possible_states)):
        cell_value = math.log(calculateRollProbability(roll_list[0], possible_states[i]), 2) + math.log(initial_state_change_probability, 2)
        viterbi_matrix.append([(cell_value, -1)])
    
    ##Calculating remaining columns
    for i in range(1, NUM_ROLLS):
        for j in range(len(possible_states)):
            cell_roll_probability = calculateRollProbability(roll_list[i], possible_states[j])
            bestValue = 0
            previousState = -1
            for k in range(len(possible_states)):
                state_change_probability = calculateStateChange(possible_states[k], possible_states[j])
                prev_state_score = viterbi_matrix[k][i-1][0]
                cell_state_value = prev_state_score + math.log(state_change_probability, 2) + math.log(cell_roll_probability, 2)
                if k == 0 or cell_state_value > bestValue:
                    bestValue = cell_state_value
                    previousState = k
            viterbi_matrix[j].append((bestValue, previousState))

    ##Traceback predictions
    viterbi_predictions = []
    bestAns = ""
    currTraceBack = -1
    for i in range(len(possible_states)):
        currAns = viterbi_matrix[i][NUM_ROLLS - 1][0]
        if i == 0 or bestAns < currAns:
            bestAns = currAns
            currTraceBack = i

    viterbi_predictions.insert(0, possible_states[currTraceBack])

    for i in range(NUM_ROLLS - 1, 0, -1):
        currTraceBack = viterbi_matrix[currTraceBack][i][1]
        viterbi_predictions.insert(0, possible_states[currTraceBack])

    return roll_list, state_list, viterbi_predictions

def main():
    ##Generate tests
    accuracy_list = []
    mcc_list = []
    for n in range(100, 2000, 100):
        sum_accuracy = 0
        sum_mcc = 0
        for i in range(10):
            all_list = genDieNumbers(n)
            
            roll_list, state_list, viterbi_predictions = viterbi(all_list)
            
            true_positives = 0
            true_negatives = 0
            false_positives = 0
            false_negatives = 0
            for i in range(len(state_list)):
                true_state = state_list[i]
                predicted_state = viterbi_predictions[i]
                if true_state == "F" and predicted_state == "F":
                    true_positives += 1
                elif true_state == "F" and predicted_state == "L":
                    false_negatives += 1
                elif true_state == "L" and predicted_state == "F":
                    false_positives += 1
                elif true_state == "L" and predicted_state == "L":
                    true_negatives += 1

            accuracy = (true_positives + true_negatives) / (true_positives + false_positives + false_negatives + true_negatives)
            sum_accuracy += accuracy
            if (true_positives == 0) and (false_positives == 0):
                if false_negatives == 0:
                    mcc = 1
                elif true_negatives == 0:
                    mcc = -1
                else:
                    mcc = 0
            elif (true_positives == 0) and (false_negatives == 0):
                if true_negatives == 0:
                    mcc = -1
                elif false_positives == 0:
                    mcc = 1
                else:
                    mcc = 0
            elif (true_negatives == 0) and (false_positives == 0):
                if true_positives == 0:
                    mcc = -1
                elif false_negatives == 0:
                    mcc = 1
                else:
                    mcc = 0
            elif (true_negatives == 0) and (false_negatives == 0):
                if true_positives == 0:
                    mcc = -1
                elif false_positives == 0:
                    mcc = 1
                else:
                    mcc = 0
            else:
                mcc = (true_positives*true_negatives - false_negatives*false_positives) / (math.sqrt((true_positives + false_negatives) * (true_positives + false_positives) * (true_negatives + false_positives) * (true_negatives + false_negatives)))
            sum_mcc += mcc
        avg_accuracy = sum_accuracy / 10
        avg_mcc = sum_mcc / 10
        accuracy_list.append(avg_accuracy)
        mcc_list.append(avg_mcc)
    
    ##Plotting accuracy vs input plot
    pdfPage = PdfPages("report.pdf")
    accuracy_plot = plt.figure() 
    plt.plot(range(100, 2000, 100), accuracy_list)
    plt.title("Viterbi algorithm accuracy vs. input size")
    plt.xlabel("Input Size")
    plt.ylabel("Accuracy")
    pdfPage.savefig(accuracy_plot)

    ##Plotting mcc vs input plot
    mcc_plot = plt.figure()
    plt.plot(range(100, 2000, 100), mcc_list)
    plt.title("Viterbi algorithm MCC vs. input size")
    plt.xlabel("Input Size")
    plt.ylabel("MCC")
    pdfPage.savefig(mcc_plot)
    pdfPage.close()

if __name__ == "__main__":
    main()