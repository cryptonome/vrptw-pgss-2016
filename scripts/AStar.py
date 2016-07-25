from heapq import *
from HeuristicScore import score
from collections import deque
from random import random
try:
    import ipdb
except:
    print "Skipping import of ipdb because Dan's school is full of jerks"

def doAStar(initial_state, world_record = 591.55):
    queue = []

    generation = 0

    STATE_QUEUE_MAX_LENGTH = 10000

    QUEUE_LENGTH_EARLY_GAME = 30 # also acts as the # of generations before a reset is triggered
    RESET_TRIGGER_DIFFERENTIAL_SCORE_EARLY_GAME = 1000000

    QUEUE_LENGTH_LATE_GAME = 1000 # same; also acts as # of gen. before a reset
    RESET_TRIGGER_DIFFERENTIAL_SCORE_LATE_GAME = 3

    IS_EARLY_GAME = True # set this to false whenever the score drops below threshold
    EARLY_GAME_SCORE_THRESHOLD = 1000000

    heappush(queue, (score(initial_state), initial_state))
    world_record_not_broken = True

    previous_scores = deque([], QUEUE_LENGTH_EARLY_GAME)

    while ( len(queue) > 0 ) and world_record_not_broken:

        # clear anything that's ranked very poorly (saves memory; improves performance a bit)
        while(len(queue) > STATE_QUEUE_MAX_LENGTH):
            e = queue.pop()
            del e

        # get the score and state from the heap
        (priority, state) = heappop(queue)

        if priority < EARLY_GAME_SCORE_THRESHOLD and IS_EARLY_GAME:
            # if we go from early game to late game, update some shit
            IS_EARLY_GAME = False
            previous_scores.clear()
            previous_scores = deque([], QUEUE_LENGTH_LATE_GAME)
        elif priority > EARLY_GAME_SCORE_THRESHOLD and not IS_EARLY_GAME:
            # if we go from late game to early game, update some shit
            IS_EARLY_GAME = True
            previous_scores.clear()
            previous_scores = deque([], QUEUE_LENGTH_EARLY_GAME)

        # shove the score into the FIFO queue
        previous_scores.append( priority )

        print "Gen {0:>6}: Score: {1:<25,} Distance: {2:<25}".format( generation, priority, state.calculate_distance(), grouping = True )

        if state.calculate_distance() < world_record:
            handle_world_record( state )
            world_record_not_broken = False
            queue = []
            break

        # logic for getting children...
        # usually, get medium and small.  SOMETIMES get the big ones, too, but not too many of them
        # if we're doing poorly, just get the big moves and get a lot of them
        if IS_EARLY_GAME:
            if previous_scores[0] - previous_scores[-1] > RESET_TRIGGER_DIFFERENTIAL_SCORE_EARLY_GAME or len(previous_scores) < QUEUE_LENGTH_EARLY_GAME:
                # keep operating as usual
                children = state.get_children( True, True, True, random() > 0.9 )
            else:
                # uh oh, fucked up and didn't make progress in 300 moves in the early game.
                # time to clear the queues and start over from the current state.
                print "Forcing early-game reset..."
                queue = []
                previous_scores.clear()
                children = state.get_children( True, False, False, True )
                triggered = True

        else:
            if previous_scores[0] - previous_scores[-1] > RESET_TRIGGER_DIFFERENTIAL_SCORE_LATE_GAME or len(previous_scores) < QUEUE_LENGTH_LATE_GAME:
                children = state.get_children( True, True, True, random() > 0.9 )
            else:
                # uh oh, fucked up and didn't make progress in 1000 moves in the late game.
                # time to clear the queues and start over from the current state.
                print "Forcing late-game reset..."
                queue = []
                previous_scores.clear()
                children = state.get_children( True, False, False, True )

        for c in children:
            heappush(queue, ( score(c), c) )

        generation += 1

    return state

def handle_world_record( state ):
    for x in range(5):
        print "###############################################"
    print "### World record solution was found"
    for x in range(5):
        print "###############################################"

    print state
    print state.get_score()

    for truck in state.trucks:
        for c in truck.path.route:
            print c.number,
        print

