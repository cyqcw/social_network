#
# # encoding:utf-8
# import requests
#
# access_token = '24.583bfe8e8b55415de7b5c59bb76f6016.2592000.1718206433.282335-70276673'
# url = 'https://aip.baidubce.com/rpc/2.0/unit/service/v3/chat?access_token=' + access_token
# post_data = {
#     "version":"3.0",
#     "service_id":"S10000",
#     "session_id":"",
#     "log_id":"7758521",
#     "request": {
#         "terminal_id":"88888",
#         "query":"你好"
#     }
# }
# headers = {'content-type': 'application/x-www-form-urlencoded'}
# response = requests.post(url, data=post_data, headers=headers)
# if response:
#     print (response.json())


# import openai
#
# openai.api_key = 'sk-proj-uRR9hZMbKDnfXEXo6kRTT3BlbkFJLPUFqFBUpwh7apln2ntX'
# openai.api_base = 'https://free.gpt.ge'
# response = openai.ChatCompletion.create(
#   model="gpt-3.5-turbo",
#   messages=[
#         {"role": "user", "content": "Who won the world series in 2020?"},
#     ]
# )
#
# print(response)
#
# api_key = 'sk-qdr2FdtUzg1IndmfA688B2Ee2bB44f0dB8244aE273Fa9233'
# url = 'https://free.gpt.ge'


# 业务空间模型调用请参考文档传入workspace信息: https://help.aliyun.com/document_detail/2746874.html

import random
from http import HTTPStatus

import dashscope
from dashscope import Generation


def call_stream_with_messages():
    messages = [
        {'role': 'user', 'content': '你好'}
    ]
    responses = Generation.call(
        'qwen1.5-110b-chat',
        messages=messages,
        seed=random.randint(1,1000),  # set the random seed, optional, default to 1234 if not set
        result_format='message',  # set the result to be "message"  format.
        stream=True,
        output_in_full=False  # get streaming output incrementally
    )
    full_content = ''
    for response in responses:
        if response.status_code == HTTPStatus.OK:
            full_content += response.output.choices[0]['message']['content']
            print(response)
        else:
            print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                response.request_id, response.status_code,
                response.code, response.message
            ))
    print('Full content: \n' + full_content)


if __name__ == '__main__':
    dashscope.api_key = 'sk-Re29MpP6Lg'
    call_stream_with_messages()