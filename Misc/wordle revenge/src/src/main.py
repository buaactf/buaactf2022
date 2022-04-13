#!/usr/bin/python3
# -*- coding: utf-8 -*-
import random
from flag import award
import string
from hashlib import sha256

random.seed()

with open('allowed_guesses.txt', 'r') as f:
    allowed_guesses = set([x.strip() for x in f.readlines()])

with open('valid_words.txt', 'r') as f:
    valid_words = [x.strip() for x in f.readlines()]


MAX_LEVEL = 128
GREEN = '\033[42m  \033[0m'
YELLOW = '\033[43m  \033[0m'
WHITE = '\033[47m  \033[0m'

def get_challenge():
    random.shuffle(valid_words)
    answer = valid_words[random.randint(0, len(valid_words))]
    return answer

def check(answer, guess):
    answer_chars = []
    for i in range(5):
        if guess[i] != answer[i]:
            answer_chars.append(answer[i])
    result = []
    for i in range(5):
        if guess[i] == answer[i]:
            result.append(GREEN)
        elif guess[i] in answer_chars:
            result.append(YELLOW)
            answer_chars.remove(guess[i])
        else:
            result.append(WHITE)
    return ' '.join(result)

def game(limit):
    round = 0
    while round < MAX_LEVEL:
        round += 1
        answer = get_challenge()
        print(f'Round {round}: #######')
        correct = False
        for _ in range(limit):
            while True:
                guess = input('> ')
                if len(guess) == 5 and guess in allowed_guesses:
                    break
                print('Invalid guess')
            result = check(answer, guess)
            if result == ' '.join([GREEN] * 5):
                print(f'Correct! {result}')
                correct = True
                break
            else:
                print(f'Wrong!   {result}')
        if not correct:
            print('You failed...')
            return round - 1

    return MAX_LEVEL


def choose_mode():
    print('Choose gamemode:')
    print('0: Easy mode')
    print('1: Normal mode')
    print('2: Hard mode')
    print('3: Insane mode')
    mode = int(input('> '))
    assert 0 <= mode <= 3
    return mode

def proof_of_work():
    alphabet = string.ascii_letters + string.digits
    proof = ''.join(random.choices(alphabet, k=16))
    hash_value = sha256(proof.encode('ascii')).hexdigest()
    print('sha256(XXXX+%s) == %s' % (proof[4:], hash_value))
    nonce = input('Give me XXXX > ')
    if len(nonce) != 4 or sha256((nonce + proof[4:]).encode('ascii')).hexdigest() != hash_value:
        return False
    return True

if __name__ == '__main__':
    if not proof_of_work():
        print('Error')
        exit(0)

    print('Guess the WORDLE in a few tries.')
    print('Each guess must be a valid 5 letter word.')
    print('After each guess, the color of the tiles will change to show how close your guess was to the word.')

    while True:
        mode = choose_mode()
        if mode == 0:
            limit = 999999999
        else:
            limit = 7 - mode
        final_level = game(limit)
        if final_level < MAX_LEVEL:
            pass
        else:
            print('You are the Master of WORDLE!')
        flag = award(mode, final_level)
        print(f'Here is you award: {flag}')
