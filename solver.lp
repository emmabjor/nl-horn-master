
% TO RUN: clingo solver.lp

% (¬Teacher(v124) ∨ ¬Student(v125) ∨ ¬Bullies(v124, v125) ∨ evaluation(BAD))
6{rule(bad,(-teacher(v124), -student(v125), -bullies(v124, v125))); rule(bad,(-teacher(v124), -bullies(v124, v125), -student(v125))); rule(bad,(-student(v125), -teacher(v124), -bullies(v124, v125))); rule(bad,(-student(v125), -bullies(v124, v125), -teacher(v124))); rule(bad,(-bullies(v124, v125), -teacher(v124), -student(v125))); rule(bad,(-bullies(v124, v125), -student(v125), -teacher(v124)))}6.
:- rule(good,(-teacher(V124), -student(V125), -bullies(V124, V125))), rule(bad,(-teacher(W124), -student(W125), -bullies(W124, W125))).

% (¬Teacher(v68) ∨ ¬Student(v69) ∨ ¬Bullies(v68, v69) ∨ evaluation(GOOD))
6{rule(good,(-teacher(v68), -student(v69), -bullies(v68, v69))); rule(good,(-teacher(v68), -bullies(v68, v69), -student(v69))); rule(good,(-student(v69), -teacher(v68), -bullies(v68, v69))); rule(good,(-student(v69), -bullies(v68, v69), -teacher(v68))); rule(good,(-bullies(v68, v69), -teacher(v68), -student(v69))); rule(good,(-bullies(v68, v69), -student(v69), -teacher(v68)))}6.
:- rule(good,(-teacher(V68), -student(V69), -bullies(V68, V69))), rule(bad,(-teacher(W68), -student(W69), -bullies(W68, W69))).