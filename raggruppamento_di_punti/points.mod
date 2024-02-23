
### INSIEMI ###
set P;

### PARAMETRI ###
param d{(i,j) in {P,P} : i < j} > 0;
param K integer >= 2 <= card(P);
param M := max{(i,j) in {P,P} : i < j} d[i,j];

### VARIABILI ###
var x{i in P, k in 1..K} binary;
var y{(i,j) in {P,P}, k in 1..K : i < j} binary;
var z{1..2};

### VINCOLI ###
subject to one_onlyone {i in P}: sum{k in 1..K} x[i,k] = 1;
subject to at_least_one {k in 1..K}: sum{i in P} x[i,k] >= 1;
subject to max_z1 {k in 1..K}: z[1] >= sum{i in P, j in P : i < j} 0.5*d[i,j]*(x[i,k] + x[j,k] - y[i,j,k]);
subject to min_z2 {k in 1..K, (i,j) in {P,P} : i < j}: z[2] <= 0.5*d[i,j]*(x[i,k] + (1-x[j,k])) + M*((1-x[i,k]) + x[j,k]);
### subject to min_z2_B {k in 1..K, (i,j) in {P,P} : i < j}: z[2] <= d[i,j]*y[i,j,k] + M*(1-y[i,j,k]); ###
subject to inf1_y {(i,j) in {P,P}, k in 1..K : i < j}: y[i,j,k] >= x[i,k] - x[j,k];
subject to inf2_y {(i,j) in {P,P}, k in 1..K : i < j}: y[i,j,k] >= -x[i,k] + x[j,k];
subject to sup1_y {(i,j) in {P,P}, k in 1..K : i < j}: y[i,j,k] <= 2 - x[i,k] - x[j,k];
subject to sup2_y {(i,j) in {P,P}, k in 1..K : i < j}: y[i,j,k] <= 2 - (1 - x[i,k]) - (1 - x[j,k]);

### OBIETTIVO ###
maximize max_sum_min_distance: 1*(-z[1]) + 1*z[2];
