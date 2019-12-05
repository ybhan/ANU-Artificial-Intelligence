include "Logistics-Q4.mzn";
include "keep.dzn";

solve minimize tot_cost;

output [ show(T), ",", show(C), ",", show(tot_cost/100), "\n" ] ++
       [ show(t) ++ "," ++ show(i) ++ "," ++
         show(pos[t,i]) ++ "," ++
         show(trans[t,pos[t,i],chilled]) ++ "," ++
         show(trans[t,pos[t,i],ambient]) ++ "\n"
        | t in trucks, i in 1..C where i < fix(step[t,0]) ];