# Lot-sizing-Py

This was a home work during Practical optimisation with Python course during which we solved variety of supply chain problems.

We used Python and Gurobi optimiser (student licence). 

Task was described in 1.5 page free text in German (additional challange for me!). Please find summary of task contents below.
 
In this task we were planning operation of a bakery as approach to lot sizing problem. We had to optimise production plan so that we satisfy the demands and do it in cost effective way.

There is one big industial owen that can be running for specific no. of hours in 1 time period, different kinds of backery products and several time periods with varying demands for bakery products. 

We had to take into account that 
- only 1 type of product could be produced at a time (croissants need different temp. then rolls etc.)
- max once per time period we could change type of product to satisfy the demand but it takes some time STij and costs Sij. 
- thus max. 2 types of products can be produced in 1 time period.

Some products from previous time period could be stored in warehouse and safisfy demand in current period - but as always in business - that comes at a cost. In this case warehousing costs would to be added. 
