% % Define some facts
% bird(tweety).
% cat(sylvester).

% % Define a rule
% flies(X) :- bird(X), not penguin(X).

% % Query which birds fly
% #show flies/1.




% TO RUN: clingo solver.lp



% % Facts
% hit(v1,v2).
% -child(v2).

% good :- hit(v1,v2), -child(v2).
% % :- good, bad, hit(A,B), -child(B), hit(C,D), -child(D), A != C, A != D, B != C, B != D.

% % -----------------------------------------------

% hit(v3,v4).
% -child(v4).
% good :- -child(v4), hit(v3,v4).
% % :- good, bad, -child(A), hit(B,A), -child(C), hit(D,C), A != C, A != D, B != C, B != D.

% % -----------------------------------------------

% livein(v5,van).
% bad :- livein(v5,van).
% % :- good, bad, livein(X,van), livein(Y,van), X != Y.

% :- (bad :- livein(v5,van)), (good :- livein(v5,van)).


% % Check for rules with the same body but different heads
% :- rule(A, B, Body), rule(C, D, Body), (A != C ; B != D).




% hit(v1,v2,bad).
% human(v1,bad).
% :- hit(V1,V2,bad), hit(V1,V2,good), human(V1,bad), human(V1,good).

% hit(v2,v1,good).
% human(v2,good).
% :- hit(V2,V1,bad), hit(V2,V1,good), human(V2,bad), human(V2,good).

% sleep(v1,bad).
% :- sleep(V1,bad), sleep(V1,good).



% WORKS, but all variations of possible orders of the predicates need to be defined..


% 2 {rule(good, (hit(v1,v2), child(v2))); rule(good, (child(v2), hit(v1,v2)))} 2.
% :- rule(good, (hit(A,B), child(B))), rule(bad, (hit(C,D), child(D))).


% 2 {rule(bad, (hit(v3,v4), child(v4))); rule(bad, (child(v4), hit(v3,v4)))} 2.
% :- rule(good, (hit(A,B), child(B))), rule(bad, (hit(C,D), child(D))).

%#show conflict/1.


% '¬WorksOn(v42, AMAZON_MECHANICAL_TURK) ∨ ¬Frustrated(v42) ∨ evaluation(BAD))'
% 2 {rule(bad, (-workson(v42,amazon_mechanical_turk), -frustrated(v42))); rule(bad, (-frustrated(v42), -workson(v42,amazon_mechanical_turk)))} 2.
% :- rule(good, (-workson(V42,amazon_mechanical_turk), -frustrated(V42))), rule(bad, (-workson(VW42,amazon_mechanical_turk), -frustrated(VW42))).

% 2 {rule(good, (-workson(v4,amazon_mechanical_turk), -frustrated(v4))); rule(good, (-frustrated(v4), -workson(v4,amazon_mechanical_turk)))} 2.
% :- rule(good, (-workson(V4,amazon_mechanical_turk), -frustrated(V4))), rule(bad, (-workson(VW4,amazon_mechanical_turk), -frustrated(VW4))).


% ¬WorksOn(v42, AMAZON_MECHANICAL_TURK) ∨ ¬Frustrated(v42) ∨ evaluation(BAD))
2{rule(bad,(-workson(v42, amazon_mechanical_turk), frustrated(v42))); rule(bad,(frustrated(v42), -workson(v42, amazon_mechanical_turk)))}2.
:- rule(good,(-workson(V42, amazon_mechanical_turk), frustrated(V42))), rule(bad,(-workson(W42, amazon_mechanical_turk), frustrated(W42))).
% ¬WorksOn(v42, AMAZON_MECHANICAL_TURK) ∨ ¬Frustrated(v42) ∨ evaluation(GOOD))
2{rule(good,(-workson(v42, amazon_mechanical_turk), -frustrated(v42))); rule(good,(-frustrated(v42), -workson(v42, amazon_mechanical_turk)))}2.
:- rule(good,(-workson(V42, amazon_mechanical_turk), -frustrated(V42))), rule(bad,(-workson(W42, amazon_mechanical_turk), -frustrated(W42))).