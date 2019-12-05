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

array[trucks] of int: cap;	     	  % Capacity of trucks
array[trucks] of bool: refrig;	     	  % Whether or not trucks are refrigerated
array[goods,customers] of int: order;	  % Number of units of goods types ordered by customers




% Insert your variables and constraints here

% trans[t,c,g] is the g-type goods units that the truck t delivers to the customer c.
array[trucks, customers, goods] of var 0..MAXCAP: trans;

% No truck can carry more than its capacity.
constraint forall (t in trucks) (sum([trans[t,c,chilled]+trans[t,c,ambient]|c in customers]) <= cap[t]);
% Non-refridged trucks can not carry chilled goods.
constraint forall (t in trucks, c in customers where refrig[t]==false) (trans[t,c,chilled] == 0);
% All customers get exactly what they ordered.
constraint forall (g in goods, c in customers) (sum([trans[t,c,g]|t in trucks]) == order[g,c]);


% In question Q1, we are only finding a satisfying solution
solve satisfy;


% Write a Minizinc output item to print the solution in the desired format for Q1
output [ show(T), ",", show(C), "\n" ] ++
       [ if sum(g in goods)(fix(trans[t,c,g])) > 0 then
             show(t) ++ "," ++ show(c) ++ "," ++
             show(trans[t,c,chilled]) ++ "," ++
             show(trans[t,c,ambient]) ++ "\n"
         else "" endif
        | t in trucks, c in customers];