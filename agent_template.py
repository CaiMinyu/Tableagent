planning_general="""
You are an assistant in planning steps for complex table tasks
{tasks} are the tasks you are going to face with, and you should deal with these tasks follow each tasks' queue.
{tasks_seq} are the execution queues for you to complete each specific tasks.
You are allowed to rearrange each single queue and combine them into one queue.
You should repeat the following procedure,the procedure are delimited by minus sign.
---
1. get one step of a specific task.
2. check whether the tasks has been done before. If there is a same tasks done before, you should not add this step to execution queue.Label like "1-1","1-2" refer to non-coexisting branch depends on the output of step 1, you should not delete this from the queue.
3. Based on each steps' input and output, you should decide where is the best place for you to insert this tasks. You should make sure this steps' input is generated before this step and the output will only be used by latter step.
4. Check if it is the last step of one single task. If it is the end of queue of one single task, you should turn to plan next tasks.
---
After repeating the above procedure, you should check if your queue can complete every single task.
Your should generate the following queue, delimited by plus sign:
+++
1. details of step1
2. details of step2
2-1. details of step 2-1
2-2. details of step 2-2
...
3. details of last step
+++
{tools} is list of functions you should use to solve this problem. Make sure your planning only use functions within the list.And you are not allowed to create function outside this list.
After you get the details of each steps in the queue you should think about how to leverage functions and SQL code to complete the tasks.
You should specify each steps' input and output.
You eventual output format is a list like [dictionary1, dictionary2,...] whose elements are dictionaries, details of each dictionary are delimited by underline. You should only output this python list.
___
{{
'label': label that can reflect the execution sequence, and are usually the same with the label of queue you generated above.,
'description': "details or instructions of this step",
'input_variables':[(input_variable1, description about where I can get the variables and what is the meaning of this variables),...],
'output_variables':[(output_variable1, description about where I can store and what is the meaning of this variables),...],
}}
___

"""

planning_details="""
{tools} is list of functions you should use to solve this problem. Make sure your planning only use functions within the list.And you are not allowed to create function outside this list.
After you get the details of each steps in the queue you should think about how to leverage functions and SQL code to complete the tasks.
You should specify each steps' input and output.
You eventual output format is a list like [dictionary1, dictionary2,...] whose elements are dictionaries, details of each dictionary are delimited by underline. You should only output this python list.
___
{{
'label': label that can reflect the execution sequence, and are usually the same with the label of queue you generated above.,
'description': "details or instructions of this step",
'input_variables':[(input_variable1, description about where I can get the variables and what is the meaning of this variables),...],
'output_variables':[(output_variable1, description about where I can store and what is the meaning of this variables),...],
}}
"""

planning_queue="""
You are an assistant in planning steps for complex table tasks
{tasks} are the tasks you are going to face with, and you should deal with these tasks follow each tasks' queue.
{tasks_seq} are the execution queues for you to complete each specific tasks.
You are allowed to rearrange each single queue and combine them into one queue.
You should repeat the following procedure,the procedure are delimited by minus sign.
---
1. get one step of a specific task in queue order.
2. check whether this step has been done before. If same steps has been finished before, you should not add this step to execution queue.Label like "1-1","1-2" refer to non-coexisting branch depends on the output of step 1, you should not delete this from the queue.
3. Based on each steps' input and output, you should decide where is the best place for you to insert this tasks. You should make sure this steps' input is generated before this step and the output will only be used by latter step. 

---
After repeating the above procedure, you should check if your queue can complete every single task.
Your should generate the following queue, delimited by plus sign:
+++
1. details of step1
2. details of step2
2-1. details of step 2-1
2-2. details of step 2-2
...
k. details of last step
"""

generate="""
You are dealing with a tasks with table data in the database.
The context you need to know is ""{history}"".
The tasks you have to face complete now is ""{step}"".
You can leverage the following tools:""{tools}"".
Use tools beyond the list that I provide above is strictly forbidden.
""{variable}"" is all variables that you can leverage. You should choose your input variable from there.
""{engine}"" is a sqlalchemy engine, you can leverage this to get connected to the database.Notice that if you are asked to generate SQL code, you should leverage python sqlalchemy library.
You output format is a dictionary as follows:
{{
'tasks_type':should be either "generate sql" or “call a function” or "reasoning"
'description': "details or instructions of this step",
'input_variables':['input_variable1', 'input_variable2',...],
'output_variables':{{'output_variable1': description about this variables,'output_variable2':description about this variables,...}}
}}
"""

generate_multiple="""
You are dealing with a tasks with table data in the database.
{output} is the result of the last step. 
According to the result of last sep, you should choose only one step from this list:{same_class}.
You should return me the only one step.
Your output is a string which is a element of the list mention above. You do not have to make any change to this output element.
The string should follow the following python regular expressions:r'^\d+(-\d+)*\..+'
"""

reasoning="""
Your task is to make inferences based on the background I provide.
{context} is the context of this task.
Your output should only include the result of your inference and do not provide the process of your inference.
"""

variable_management="""
{other} is a dictionary. Please change the key of this dictionary accordingly.
Your output format is a dictionary as follows:
{key:value}

"""