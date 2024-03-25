inconsistent :- evaluation(good), evaluation(bad).

% evaluation(BAD) | ~LivesIn(v21, VAN)
livesIn(v21,van).
evaluation(bad) :- livesIn(v21,van).

