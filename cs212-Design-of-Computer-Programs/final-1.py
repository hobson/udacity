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
    ## bowling([int, ...]) -> int
    f=0
    scores = [0]*12 # two extra frames in case strikes bolled in all last 3 and frame conter increments
#    strike = [False]*11
    frame_ball = 0
    spares = False
    strikes1 = strikes2 = False
    print balls
    for i,b in enumerate(balls):
        if spares: #f>0 and scores[f-1]==10: # spare in previous frame
            scores[f-1] += b
        if strikes2:
            scores[f-1] += b
        if strikes1:
            if frame_ball == 0:
                scores[f-2] += b
            else:
                scores[f-1] += b
        scores[f] += b
#        elif f==10:
#            scores[f-1] += b
        print scores
        print i,f,frame_ball,spares,strikes2,strikes1,b,sum(scores[0:10])
        
        spares = False
        if frame_ball==1 and balls[i-1]+b == 10:
            spares = True
        strikes1 = strikes2
        strikes2 = False
        if frame_ball==0 and b == 10 and f<12:
            strikes2 = True
        if f<12 and (frame_ball==1 or b == 10):
            f = f+1
            frame_ball = 0
        else:
            frame_ball += 1
        
    return sum(scores[0:10])


def test_bowling():
    return [   
        0   == bowling([0] * 20),
        20  == bowling([1] * 20),
        80  == bowling([4] * 20),
        190 == bowling([9,1] * 10 + [9]),
        300 == bowling([10] * 12),
        200 == bowling([10, 5,5] * 5 + [10]),
        11  == bowling([0,0] * 9 + [10, 1,0]),
        12  == bowling([0,0] * 8 + [10, 1,0]),
        34  == bowling([0,0] * 8 + [10, 10,1,2]),
    ]

if __name__ == '__main__':
    print test_bowling()
