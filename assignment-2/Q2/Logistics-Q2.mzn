%
%    Enter your details below:
%
%    Name: Jeff Yuanbo Han
%    Student ID: u6617017
%    Email: u6617017@anu.edu.au
%


int: C;					  % Number of customers
int: T;                     		  % Number of trucks
int: G;                     		  % Number of goods types 
int: MAXCAP;                		  % Maximum truck capacity

set of int: trucks = 1..T;    	     	  % Set of trucks
set of int: customers = 0..C;        	  % Set of customers. Includes depot as customer 0
set of int: goods = 1..G;            	  % Set of goods types
int: chilled = 1;  int: ambient = 2; 	  % Good types
set of int: times = 0..C+1;            	  % Enough time steps to visit each customer once and depot twice if needed

array[trucks] of int: cap;	     	  % Capacity of trucks
array[trucks] of bool: refrig;	     	  % Whether or not trucks are refrigerated
array[goods,customers] of int: order;	  % Number of units of goods types ordered by customers



% Insert your variables and constraints here

%% Solve the problem without sequences.
% trans[t,c,g] is the g-type goods units that truck t delivers to customer c.
array[trucks, customers, goods] of var 0..MAXCAP: trans;

% No truck can carry more than its capacity.
constraint forall (t in trucks) (sum([trans[t,c,chilled]+trans[t,c,ambient]|c in customers]) <= cap[t]);
% Non-refridged trucks can not carry chilled goods.
constraint forall (t in trucks, c in customers where refrig[t]==false)(trans[t,c,chilled] == 0);
% All customers get exactly what they ordered.
constraint forall (g in goods, c in customers) (sum([trans[t,c,g]|t in trucks]) == order[g,c]);

%% Add sequences.
% step[t,c] is the sequence number (order) when truck t visits customer c.
array[trucks, customers] of var 1..C+1: step;

% All the target customers have to be visited before returning back to the depot.
constraint forall (t in trucks, c in customers) (sum(g in goods)(trans[t,c,g])>0 <-> step[t,c]<step[t,0]);

% Different customers of the same truck should have different visiting order.
% Note that although we assign each customer a "step" here, actions after returning back is invalid.
include "alldifferent.mzn";
constraint forall (t in trucks) (alldifferent([step[t,c] | c in customers]));


%% Sort the sequences in ascending order.
% pos[t,i] is the customer that truck t i-thly visists.
%array[trucks, times] of var customers: pos;

%constraint forall (t in trucks) (pos[t,0] == 0);
%constraint forall (t in trucks, i in 1..C+1) (step[t,pos[t,i]] == i);


% In question Q2, we are only finding a satisfying solution
solve satisfy;

output [ show(T), ",", show(C), "\n" ] ++
       [ if sum(g in goods)(fix(trans[t,c,g])) > 0 then
         show(t) ++ "," ++ show(step[t,c]) ++ "," ++
         show(c) ++ "," ++
         show(trans[t,c,chilled]) ++ "," ++
         show(trans[t,c,ambient]) ++ "\n"
         else "" endif
        | t in trucks, c in customers ];

% Write a Minizinc output item to print the solution in the desired format for Q2
%output [ show(T), ",", show(C), "\n" ] ++
 %      [ show(t) ++ "," ++ show(i) ++ "," ++
  %       show(pos[t,i]) ++ "," ++
   %      show(trans[t,pos[t,i],chilled]) ++ "," ++
    %     show(trans[t,pos[t,i],ambient]) ++ "\n"
     %   | t in trucks, i in 1..C where i < fix(step[t,0]) ];