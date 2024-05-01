# Bioinformatic Viterbi Algorithm
This program simulates die rolls that illustrate the Hidden Markov model and uses the Viterbi algorithm to predict which state were used to generate the dice roll.

The two states: Fair Die and Loaded Die

In the Fair Die state: 
- There is a 1/6 chance to roll each number from 1 to 6 (1/6 to roll 1, 1/6 to roll 2, etc.)

In the Loaded Die state:
- There is 1/10 chance to roll each number from 1 to 5 (1/10 to roll 1, 1/10 to roll 2, etc.)
- There is 1/2 chance to roll 6

It will test the Viterbi algorithm on a sequence of rolls with size ranging from 100 to 2000 rolls
And produces two graphs: Accuracy vs. number of rolls and MCC vs. number of rolls
To run the program, write
  python3 viterbi.py
  
