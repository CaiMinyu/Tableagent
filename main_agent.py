
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from sqlalchemy import create_engine,text,inspect,MetaData, Table
from OutputParser import *

import agent_message
import database as db

import agent_template
class executor():
    def __init__(self,engine,content):
        self.engine = engine
        self.content = content
    def func_executor(self,instance,variables):
        code=instance['execution']
        exec(code)
        variables.add_variables(instance['output'])
        function=instance['function']
        input_variables=instance['input_variable']
    def sql_executor(self,instance):
        sql_query=instance['sql_query']
        description=instance['description']
        fetch=instance['fetch']
        dbseq=instance['db']
        result = dbseq.run(sql_query, fetch=fetch)
    def reasoning_executor(self,context):
        prompt_template = agent_template.reasoning
        prompt = PromptTemplate(input_variables=['context'], template=prompt_template)
        llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=0)
        chain = LLMChain(llm=llm, prompt=prompt)
        input_data = {
        'context':context
        }
        response = chain.run(input_data)
        return response
    def execute(self):
        if self.content['execution']=='reasoning':
            return self.reasoning_executor(self.content)
        if self.content['execution']=='generate sql':
            return self.sql_executor(self.content)
        if self.content['execution']=='call a function':
            return self.func_executor(self.content)

class Plan_Queue_Agent():
    def __init__(self,engine):
        self.tools=dict()
        self.engine=engine
    def get_tasks_seq(self,tasks):
        return agent_message.entity_matching+agent_message.get_columns_names
    def get_tasks(self):
        return ['entity_matching',"get columns' name"]
    def get_table_names(self):
        inspector = inspect(self.engine)
        table_names = inspector.get_table_names()
        return table_names
    def get_header(self):
        table_names=self.get_table_names()
        all_header=dict()
        for name in table_names:
            metadata = MetaData()
            table_name = name
            table = Table(table_name, metadata, autoload_with=self.engine)
            columns = [column.name for column in table.columns]
            all_header[name]=columns
        return all_header

    def planning_queue(self):
        prompt_template=agent_template.planning_queue
        prompt=PromptTemplate(input_variables=['tasks','tasks_seq'],template=prompt_template)
        tasks=self.get_tasks()
        tasks_seq = self.get_tasks_seq(tasks)
        llm=ChatOpenAI(model='gpt-3.5-turbo',temperature=0)
        chain=LLMChain(llm=llm,prompt=prompt)
        input_data={
            'tasks':tasks,
            'tasks_seq':tasks_seq,
        }
        response=chain.run(input_data)
        response=Queue_OutputParser(response)
        print("this part have not been finished")
        if type(response)==str:
            string='wrong'
        else:
            string=''
            for strings in response:
                string+=strings
                string+='\n'
        return string
class variable_management():
    def __init__(self,):
        self.variable=dict()
    def add_variables(self,other):
        if other.keys() in self.variable.keys():
            now=self.variable[other.keys()]
            llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=0)
            prompt = PromptTemplate(input_variables=['other'], template=agent_template.variable_management)
            chain = LLMChain(llm=llm, prompt=prompt)
            input_data = {'other':other}
            response = chain.run(input_data)
            print("差outputparser")
        self.variable.update(response)


class GraphAgent():
    def __init__(self,engine,queue):
        self.engine=engine
        self.queue=queue
    @staticmethod
    def get_same_label(label1,label2):
        k=0
        class1=label1.count('-')
        class2=label2.count('-')
        if class1 ==0 and class2 ==0:
            return 0
        list1=label1.split('-')
        list2=label2.split('-')
        for i in range(min(len(list1),len(list2))):
            if list1[i] == list2[i]:
                k=k+1
            else:
                break
        return k
    def get_rag_content(self):
        return "123"
    def get_tools(self):
        return """function named get_table_names(engine)‘s output are all tables' names within current database"""
    def generate(self,step,history,variable):
        llm=ChatOpenAI(model='gpt-3.5-turbo',temperature=0)
        prompt=PromptTemplate(input_variables=['history','step','tools','variable','engine'],template=agent_template.generate)
        chain=LLMChain(llm=llm,prompt=prompt)
        input_data={'history':history,
                    'step':step,
                    'tools':self.get_tools(),
                    'variable':variable,
                    'engine':self.engine}
        response=chain.run(input_data)
        print(response)
        response=DictParser(response)

        return response


    def execute(self,details):
        exe=executor(self.engine,details)
        return exe.execute()
    def drop_queue(self,same_len,output,queue,same_class):
        #output should contain the information about drop queue
        #suppose output indicate we should choose "2-1"
        llm=ChatOpenAI(model='gpt-3.5-turbo',temperature=0)
        prompt=PromptTemplate(input_variables=['output','same_class'],template=agent_template.s)
        chain=LLMChain(llm=llm,prompt=prompt)
        input_data={'output':output,
                    'same_class':same_class,
                    }
        response=chain.run(input_data)
        print('差outputParser')
        target_label=response.split('.',1)[0]
        queue_prime=list()
        if same_len==0:
            return queue[:]
        for i in range(len(queue)):
            label=queue[i].split('.',1)[0]
            lens=self.get_same_label(target_label,label)
            if lens!=same_len:
                queue_prime.append(queue[i])
        return queue_prime
    def execution(self):
        complete_step=list()
        variable_dict=variable_management()
        queue=self.queue.split('\n')

        while queue:
            current_step=queue.pop(0)

            current_index=current_step.split('.',1)[0]
            next_step=queue[0]
            next_index=next_step.split('.',1)[0]
            same_len=self.get_same_label(current_index,next_index)
            if same_len == 0:
                details=self.generate(current_step.split('.',1)[1],'do not need any context',variable_dict)
                output=self.execute(details)
                continue
            if same_len >0:
                end=False
                i=1
                same_class=[next_step]
                while not end:
                    if i > len(queue)-1:
                        break
                    next_class_branch=queue[i]
                    ncb = next_class_branch.split('.', 1)[0]
                    same_len_next = self.get_same_label(next_index,ncb)
                    if same_len_next == same_len:
                        same_class.append(next_class_branch)
                    else:
                        end=True
                    i=i+1
                details=self.generate(current_step.split('.',1)[1],'do not need any context',variable_dict)
                output=self.execute(details)
                queue=self.drop_queue(same_len,output,queue,same_class)








user = 'root'
password = '!QAZ2wsx'
host = '127.0.0.1'
database = 'agent'


def get_table_names(engine):
    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    return table_names
engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{database}')
engine.table_names()
# a=Plan_Queue_Agent(engine)
# queue=a.planning_queue()
# queue="""1. get all tables' names in current database.
# 2. generate SQL code to get headers of each table. Store it in a dictionary.
# 3. suppose you have got the headers of each tables, judge whether 2 tables have the same columns.
# 3-1. if the 2 tables do not have same headers, the two tables refer to different entity.
# 3-2. if the 2 tables has same headers,generate SQL code to select data from same headers of each row from 2 table respectively,forming a subset. Check whether the 2 subset has same data instance. If no consistent data instance, the 2 two table refer to different entity. Only if all these data is consistent, the 2 tables refer to same entity. Output of this step should be boolean.
# """
# ex=GraphAgent(engine,queue)
#
# ex.execution()



















#table preprocessing