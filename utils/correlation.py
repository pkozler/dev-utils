"""
    Spočítá korelační koeficient pro zadanou dvojici sloupců.
"""

import sys

# # 1. Calculate Mean
# insert into tab2 (tab1_id, mean)
# select ID,
#        sum([counts]) /
#        (select count(*) from tab1) as mean
# from tab1
# group by ID
# ;
#
# # 2. Calculate standard deviation
# update tab2
# set stddev = (
#     select sqrt(
#                            sum([counts] * [counts]) /
#                            (select count(*) from tab1)
#                        - mean * mean
#                ) stddev
#     from tab1
#     where tab1.ID = tab2.tab1_id
#     group by tab1.ID)
# ;
#
# # 3. Finally Pearson Correlation Coefficient
# select ID,
#        ((sf.sum1 / (select count(*) from tab1)
#            - stats1.mean * stats2.mean
#             )
#            / (stats1.stddev * stats2.stddev)) as PCC
# from (
#          select r1.ID,
#                 sum(r1.[counts] * r2.[counts]) as sum1
#          from tab1 r1
#                   join tab1 r2
#                        on r1.ID = r2.ID
#          group by r1.ID
#      ) sf
#          join tab2 stats1
#               on stats1.tab1_id = sf.ID
#          join tab2 stats2
#               on stats2.tab1_id = sf.ID
# ;

sys.exit('Not yet implemented!')
