% Define parent-child relationships
% parent(alice, bob). % Alice is a parent of Bob
% parent(alice, carol). % Alice is also a parent of Carol
% parent(bob, dave). % Bob is a parent of Dave

% % Define a sibling relationship based on shared parent
% sibling(X, Y) :- parent(Z, X), parent(Z, Y), X \= Y.

% % Define a child relationship as the inverse of a parent relationship
% child(X, Y) :- parent(Y, X).




% -----------------------------------------
% livesIn(v1,van) → evaluation(good)
% livesIn(v1,van).
% evaluation(good) :- livesIn(V1, van).

% inconsistent :- 
%     livesIn(V1, van),
%     evaluation(good),
%     evaluation(bad).

% % -----------------------------------------
% % livesIn(v2,van) → evaluation(bad)
% livesIn(v2,van).
% evaluation(bad) :- livesIn(V2, van).

% inconsistent :- 
%     livesIn(V2, van),
%     evaluation(good),
%     evaluation(bad).

% % -----------------------------------------
% % ¬hit(v4,v3) ∧ child(v3) → evaluation(good)
% hit(v3,v4).
% child(v4).
% evaluation(good) :- hit(V3, V4), child(V4).

% inconsistent :- 
%     hit(V3, V4),
%     child(V4),
%     evaluation(good),
%     evaluation(bad).

% -----------------------------------------
% livesIn(v1,van,good).

% inconsistent :- 
%     livesIn(V1, van, good),
%     livesIn(V1, van, bad).

% -----------------------------------------
% livesIn(v1,van,bad).

% inconsistent :- 
%     livesIn(V1, van, good),
%     livesIn(V1, van, bad).

% -----------------------------------------
% hit(v1,v2,bad).
% child(v2,bad).

% inconsistent :- 
%     hit(_,_,good),
%     hit(_,_,bad),
%     child(_,good),
%     child(_,bad).

% % -----------------------------------------
% child(v1,good).
% hit(v2,v1,good).

% inconsistent :- 
%     hit(_,_,good),
%     hit(_,_,bad),
%     child(_,good),
%     child(_,bad).

% inconsistent :- 
%     child(V1,good),
%     child(V1,bad),
%     hit(V2,V1,good),
%     hit(V2,V1,bad).


% TO RUN:
% swipl
% [solver].
% query.

% halt.

% Facts and rules expressing norms
bad :- livesIn(v1, van).
evaluation(good) :- livesIn(v2, van).
good :- hurts(v3, v4), child(v4).

% Facts indicating individuals' actions or states
livesIn(v1, van).
livesIn(v2, van).
hurts(v3, v4).
child(v4).

% Mechanism to detect conflicting evaluations


% Example query to find conflicts based on the same body
test :- call(livesIn(X, van)).
