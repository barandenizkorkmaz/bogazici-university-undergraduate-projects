Set i customers
/
$include customers.txt
/;

Set k /small, large/;

Alias (i,j,ts,tl);

Parameter a(i,j) /
$include clusterability.txt
/;

Parameter dw(i) /
$include demand-weight.txt
/;

Parameter dv(i) /
$include demand-volume.txt
/;

Parameter u(i) /
$include trans_cost.txt
/;

Table c(i,k)
$include direct-shipment-cost.txt
;

Variables
costlarge(tl)
maxoflarge(tl)
costsmall(ts)
maxofsmall(ts)
costindirect
totalcost;

Binary Variables
isinlarge(tl,i)
isinsmall(ts,i)
isinindirect(i);


Scalar           M /100000/;

Equations
objective
const1(tl)
const2(tl,i)
const3(tl)
const4(tl)
const5(tl,i,j)
const6(ts)
const7(ts,i)
const8(ts)
const9(ts)
const10(ts,i,j)
const11
const12(i)
const13(tl)
const14(ts);

objective..     totalcost  =e=  sum(tl,costlarge(tl))+sum(ts,costsmall(ts))+costindirect;

const1(tl)..     costlarge(tl) =e= 250*sum(i,isinlarge(tl,i))-250+maxoflarge(tl);
const2(tl,i)..   maxoflarge(tl) =g= isinlarge(tl,i)*c(i,'large');
const3(tl)..     sum(i,isinlarge(tl,i)) =l= 3;
const4(tl)..     sum(i,isinlarge(tl,i)*dv(i)) =l= 33;
const5(tl,i,j)..   a(i,j) =g= 1-M*(2-isinlarge(tl,i)-isinlarge(tl,j));
const6(ts)..     costsmall(ts) =e= 125*sum(i,isinsmall(ts,i))-125+maxofsmall(ts);
const7(ts,i)..   maxofsmall(ts) =g= isinsmall(ts,i)*c(i,'small');
const8(ts)..     sum(i,isinsmall(ts,i)) =l= 3;
const9(ts)..     sum(i,isinsmall(ts,i)*dv(i)) =l= 18;
const10(ts,i,j)..  a(i,j) =g= 1-M*(2-isinsmall(ts,i)-isinsmall(ts,j));
const11..        costindirect =e= sum(i,isinindirect(i)*dw(i)*u(i));
const12(i)..       sum(tl,isinlarge(tl,i))+sum(ts,isinsmall(ts,i))+isinindirect(i) =e= 1;
const13(tl)..       maxoflarge(tl) =g= 250-M*sum(i,isinlarge(tl,i));
const14(ts)..       maxofsmall(ts) =g= 125-M*sum(i,isinsmall(ts,i));

Model project /all/;
solve project using MIP minimizing totalcost;
display isinlarge.L,isinsmall.L,isinindirect.L;
