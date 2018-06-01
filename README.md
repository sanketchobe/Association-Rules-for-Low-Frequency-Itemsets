# Association-Rules-for-Low-Frequency-Itemsets
Implementation of novel ideal of "Mining Association Rules for Low Frequency Itemsets"

Modification of Apriori and FP-Growth algorithm:

1. Apriori and FP-Growth algorithms are modified to generate low-frequency as well as high frequency itemsets.
2. Calculate the utility of low-frequency and high frequency itemset in parallel.
3. Generate the four new types of itemsets as follows:
   a. High Frequency High Utility b. High Frequency Low Utility
   c. Low Frequency High Utility  d. Low Frequency Low Utility
4. Generate association rules for the combination of four type of itemsets.


