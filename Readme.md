# AUTOMATA CODES

## Q1 : REGEX TO NFA
First make regex proper with instering a symbol for multiplication. I used "?". Then convert the string into postfix.

Next to convert postfix regex to nfa we need to handle symbols,star, union, and concatenation and epsilon.

I took a nfa stack and appended multiple nfas, popping out whenever needed (for union, concatenation, star)

<b>For Symbol</b>:<br>
    
Make a start and end state and add transition for that symbol,all the components of NFA.(allstates,letters,Transition, start_states,end_states) and push this onto stack.

<b>For Epsilon</b>:<br>
    Same as symbol but start and end state are same.

<b>For Union</b>:<br>
    Pop the top two nfas and make new nfa with old final states.
    make a new start_state and add transitions to old start states and push the new NFA.

<b>For Concatentation</b>:<br>
    Pop the top two nfas and make transitions from final states of nfa1 to start states of nfa2.New final states would be final states of nfa2 and start states would be start states of nfa1 and push this onto nfa stack.



<b>For Star</b>:<br>
    Pop one nfa and make new startstate to old start state with epsilon transition, and make new final states and add transitions to startstates and push the nfa to nfastack.

OUTPUT:
  At the end there would be one nfa left in stack, if valid expression is given, just pop and print it.

   
<br>

## Q2 : NFA TO DFA

Take the powerset of states of NFA as states of DFA.Used itertools library.Then in which ever state the previous start state is leading to mark that as startstates.Similarly for final states.Then for transition,take each element in ppowerset (i.e new states)  and compute all the possible destination states and take that set as next state. Do this for each letter.If there is no destination set,we redirect it to emptyset.

OUTPUT: return the  dfa.

<br>

## Q3 : DFA TO REGEX

Make DFA into GNFA , ie, add new start state and connect it to every other transition state using the suitable letters,"$" if nothing is valid.<br>
Similarly for accept state,make a single accept state and connect arrows from all other states to this, which suitable letters.
<br>
Then except for start and final states connect from each state to each other state with sutiable variables.
<br>
Then applied algorithm in [page no.94 introduction to theory of computation. micheal sipser](http://fuuu.be/polytech/INFOF408/Introduction-To-The-Theory-Of-Computation-Michael-Sipser.pdf),to convert GNFA back to regex.


OUTPUT:<br>
    make output letters crctly, ignoring "$". 


<br>

## Q4 : MINIMIZING DFA:
<br>   

First i removed all the unreachable states from the DFA.Start from start_state and find all reachable states, all states minus reachable states gives al unreachable states.Here's the pseudo code for the same:
    
    
    let reachable_states := {q0};
    let new_states := {q0};

    do {
        temp := the empty set;
        for each q in new_states do
            for each c in Σ do
                temp := temp ∪ {p such that p = δ(q,c)};
            end;
        end;
        new_states := temp \ reachable_states;
        reachable_states := reachable_states ∪ new_states;
    } while (new_states ≠ the empty set);

    unreachable_states := Q \ reachable_states;
    
Next i partioned final states and non-final states.I took a 2d array of all states , think it of as cartesian product matrix of al states.Then for each pair (Qi,Qj) if they are distingushable mark arr[i][j] and arr[j][i] as 1. So initially the values at intersection of final and non-final states would be 1.
    Then so it for all states untill you can no longer update them.
How to check if they are distingushable? if for each letter say destination states are Pi and Pj, if arr[i][j] is 1 , then they are distingushable.Here's the pseudo code for the same.

        Input:  DFA M = (Q, Σ, δ, q0, F)
    Output: DFA M' = (Q', Σ, δ', q'0, F')

    # initialization step
    for each pair of states  p, q ∈ M:
         mark (p, q) as distinguishable, if p ∈ F and q ∉ F (or vice versa)

    # state-equivalence step
    repeat:
         for each pair of states  p, q ∈ M:
              mark (p, q) as distinguishable, if there is a symbol a ∈ Σ
              such that (δ(p, a), δ(q, a)) is distinguishable
    until no new pair is marked as distinguishable

    build and return M'

OUTPUT:
    We can easily build back from matrix, at each row what all state values are zero goes as single state, removing duplicates.