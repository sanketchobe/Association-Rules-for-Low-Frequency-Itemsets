# Association-Rules-for-Low-Frequency-Itemsets
Implementation of novel ideal of "Mining Association Rules for Low Frequency Itemsets"

Modification of Apriori and FP-Growth algorithm:

1. Apriori and FP-Growth algorithms are modified to generate low-frequency as well as high frequency itemsets.
2. Calculate the utility of low-frequency and high frequency itemset in parallel.
3. Generate the four new types of itemsets as follows:
   a. High Frequency High Utility b. High Frequency Low Utility
   c. Low Frequency High Utility  d. Low Frequency Low Utility
4. Generate association rules for the combination of four type of itemsets.

I. Run FP-Growth algorithm through command line:

-s 150 input_chess2.txt -c 100 utility_chess2.txt 200

where, s - minimum support threshold,
       input - input frequency file
       c - minimum confidence threshold,
       utility - input utility file
       200 - minimum utility threshold
       
 
II. Run Apriori algorithm through command line:

-f input.txt -uf utility.txt -op output.txt -s 0.40 -c 0.30 -u 20 -ut 1

where, f - input frequency file
       uf - input utility file
       op - output association rules file
       s - minimum support threshold
       c - minimum confidence threshold
       u - minimum utility threshold
       ut - minimum utility prelarge threshold


References:
1 FP-Growth implementation: https://github.com/enaeseth/python-fp-growth
2 Apriori implementation: https://github.com/abarmat/python-apriori
