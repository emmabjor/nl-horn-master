% Define parent-child relationships
parent(alice, bob). % Alice is a parent of Bob
parent(alice, carol). % Alice is also a parent of Carol
parent(bob, dave). % Bob is a parent of Dave

% Define a sibling relationship based on shared parent
sibling(X, Y) :- parent(Z, X), parent(Z, Y), X \= Y.

% Define a child relationship as the inverse of a parent relationship
child(X, Y) :- parent(Y, X).




% (¬LivesIn(v21, VAN) ∨ evaluation(BAD))