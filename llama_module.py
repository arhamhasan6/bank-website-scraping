# from langchain_community.llms import LlamaCpp
# from langchain.callbacks.manager import CallbackManager
# from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
# from langchain.chains import LLMChain
# from langchain.prompts import PromptTemplate
# from langchain_community.llms import LlamaCpp



# from langchain import PromptTemplate
 
# template = """
# <s>[INST] <<SYS>>
# Act as an Astronomer engineer who is teaching high school students.
# <</SYS>>
 
# {text} [/INST]
# """
 
# prompt = PromptTemplate(
#     input_variables=["text"],
#     template=template,
# )


# from langchain import PromptTemplate
 
# template = """
# <s>[INST] <<SYS>>
# Act as an Astronomer engineer who is teaching high school students.
# <</SYS>>
 
# {text} [/INST]
# """
 
# prompt = PromptTemplate(
#     input_variables=["text"],
#     template=template,
# )


# # Callbacks support token-wise streaming
# callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

# model_path = "models/llama-2-7b-chat.Q2_K.gguf"
# llm = LlamaCpp(
#     model_path=model_path,
#     temperature=0.5,
#     max_tokens=500,
#     top_p=1,
#     callback_manager=callback_manager,
#     verbose=True,  # Verbose is required to pass to the callback manager
# )
# text= "We are Pakistans first and largest dedicated Islamic bank and one of the fastest growing financial institutions in the banking sector of the country. Our success over the years is the result of our dedicated approach to nurture and develop our human resource, whom we consider to be an integral asset of our organization. We strive to conduct our business to the highest standards guided by the principles of Shariah and our Vision. Everything we do reflects this and this is the essence of who we are as a brand. Who Are We? We are Pakistan’s first and largest dedicated Islamic bank and one of the fastest growing financial institutions in the banking sector of the country. Our success over the years is the result of our dedicated approach to nurture and develop our human resource, whom we consider to be an integral asset of our organization. We strive to conduct our business to the highest standards guided by the principles of Shariah and our Vision. Everything we do reflects this and this is the essence of who we are as a brand. Vision Establish Islamic banking as banking of first choice to facilitate the implementation of an equitable economic system, providing a strong foundation for establishing a fair and just society for mankind. Vision, Mission & Values, provide me vision statement from this text"
# output = llm.invoke(prompt.format(text=text))
# print(output)

import os 
from langchain.llms import CTransformers
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory

model_id='TheBloke/Llama-2-7B-Chat-GGUF'
os.environ['XDG_CACHE_HOME'] = './model/cache/'
config = {'temperature' :0.00,'context_length':4000,}
llm = CTransformers(model=model_id,
                    model_type = 'llama',
                    config = config ,
                    #callbacks = [StreamingStdOutCallbackHandler]
                    
                    )


print(llm.invoke("your name ?"))
