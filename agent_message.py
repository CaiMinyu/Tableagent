entity_matching="""
Your first tasks is entity matching. You are given 2 tables(named table1 and table2), please complete the tasks steps by steps. Independent.
1. get all tables' names in current database.
2. generate SQL code to get headers of each table. Store it in a dictionary. 
3. suppose you have got the headers of each tables, judge whether 2 tables have the same columns.
3-1. if the 2 tables do not have same headers, the two tables refer to different entity. 
3-2. if the 2 tables has same headers,generate SQL code to select data from same headers of each row from 2 table respectively,forming a subset. Check whether the 2 subset has same data instance. If no consistent data instance, the 2 two table refer to different entity. Only if all these data is consistent, the 2 tables refer to same entity. Output of this step should be boolean.
"""
get_columns_names="""
your second tasks is to get the headers of each tables
1. generate SQL code to get headers of each table. Store it in a dictionary. 
2. can you find all tables' names in current database.?
"""