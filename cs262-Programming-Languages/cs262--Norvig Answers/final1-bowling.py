"""
UNIT 1: Bowling:

You will write the function bowling(balls), which returns an integer indicating
the score of a ten-pin bowling game.  balls is a list of integers indicating
how many pins are knocked down with each ball.  For example, a perfect game of
bowling would be described with:

    >>> bowling([10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10])
    300

The rules of bowling are as follows:

(1) A game consists of 10 frames. In each frame you roll one or two balls,
except for the tenth frame, where you roll one, two, or three.  Your total
score is the sum of your scores for the ten frames.
(2) If you knock down fewer than ten pins with your two balls in the frame,
you score the total knocked down.  For example, bowling([8, 1, 7, ...]) means
that you knocked down a total of 9 pins in the first frame.  You score 9 point
for the frame, and you used up two balls in the frame. The second frame will
start with the 7.
(3) If you knock down all ten pins on your second ball it is called a 'spare'
and you score 10 points plus a bonus: whatever you roll with your next ball.
The next ball will also count in the next frame, so the next ball counts twice
(except in the tenth frame, in which case the bonus ball counts only once).
For example, bowling([8, 2, 7, ...]) means you get a spare in the first frame.
You score 10 + 7 for the frame; the second frame starts with the 7.
(4) If you knock down all ten pins on your first ball it is called a 'strike'
and you score 10 points plus a bonus of your score on the next two balls.
(The next two balls also count in the next frame, except in the tenth frame.)
For example, bowling([10, 7, 3, ...]) means that you get a strike, you score
10 + 7 + 3 = 20 in the first frame; the second frame starts with the 7.

"""

def bowling(balls):
    "Compute the total score for a player's game of bowling."
    total = 0
    for frame in range(10):
        score, balls = score_frame(balls)
        total += score
    return total

def score_frame(balls):
    "Return two values: (score_for_this_frame, remaining_balls)."
    n_used, n_scoring = ((1, 3) if balls[0] == 10 # strike
                    else (2, 3) if balls[0] + balls[1] == 10 # spare
                    else (2, 2)) # open frame
    return (sum(balls[:n_scoring]), balls[n_used:])

def test_bowling():
    assert   0 == bowling([0] * 20)
    assert  20 == bowling([1] * 20)
    assert  80 == bowling([4] * 20)
    assert 190 == bowling([9,1] * 10 + [9])
    assert 300 == bowling([10] * 12)
    assert 200 == bowling([10, 5,5] * 5 + [10])
    assert  11 == bowling([0,0] * 9 + [10,1,0])
    assert  12 == bowling([0,0] * 8 + [10, 1,0])



## In the solution above, score_frame does most of the work, deciding the
## score for the frame, and what balls remain for subsequent frames.
## The logic of summing results is obscured by the need to return 2 values.
## An alternative solution below that makes it more explicit that we are summing 
## the 10 frames scores, by mutating balls rather than returning a 2nd value:

def bowling(balls):
    "Compute the score for one player's game of bowling."
    return sum(score_frame1(balls) for frame in range(10))

def score_frame1(balls):
    "Return (score, balls): the score for this frame and the remaining balls."
    n_used, n_scoring = ((1, 3) if balls[0] == 10 # strike
                    else (2, 3) if balls[0] + balls[1] == 10 # spare
                    else (2, 2)) # open frame
    score = sum(balls[:n_scoring])
    balls[:n_used] = []
    return score
