# coding:utf-8
#!/usr/bin/python3
import json
import re
from voice_commands.srv import Dashboard, DashboardResponse
import rospy

import sys
import rospy
import openai

openai.api_key="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"
import os
os.environ["REPLICATE_API_TOKEN"] = "r8_72wKmT3ECXRTAXEJ08tBoEsFFnj6K2d2HR5HF"
import replicate


def dashboard_prompt(dashboard_instruction):
    ## ChatGPT gpt-3.5-turbo
    # dashboard_pre_prompt = "Given a list of commands, respond with the corresponding string text\
    #     drill holes 'start,drill' start drilling operation\
    #     de-burr holes 'start,de-burr' start deburring operation\
    #     paint holes 'start,paint' start deburring operation\
    #     stop 'stop' stop the current operation\
    #     resume 'resume' resume operating\
    #     reset 'reset' reset workorder json\
    #     home 'home' move the robot to home position (already known)\
    #     Your response MUST follow exactly this pattern, and don't add any extra unneeded text of any kind at all."
    # input_ex = ['de-burr holes from 1001 to 1015 in workpiece 101 and fiducial 102', 
    #          'stop the current operation and go to home']
    # output_ex = ['start,de-burr,json,101,102,1001,1015',
    #           'stop,home']
    # response_to_dashboard = openai.ChatCompletion.create(
    #     model='gpt-3.5-turbo',
    #     messages=[
    #         {"role": "system", "content": "You are a text-generating robot, you output text strings exactly as instructed." + dashboard_pre_prompt},
    #         {"role": "user", "content": "de-burr holes from 1001 to 1015 in workpiece 101 and fiducial 102"},
    #         {"role": "assistant", "content": "start,de-burr,json,101,102,1001,1015"},
    #         {"role": "user", "content": "stop the current operation and go to home"},
    #         {"role": "assistant", "content": "stop,home"},
    #         {"role": "user", "content": dashboard_instruction},
    #     ],
    #     top_p= 0.1,
    #     temperature= 0,
    #     max_tokens=100
    # )
    # # response_to_dashboard_text = response_to_dashboard.choices[0].text.strip()
    # # print(response_to_dashboard_text)
    # response_to_dashboard_text = response_to_dashboard["choices"][0]["message"]["content"].strip().split(',')

    ## ChatGPT gpt-3.5-turbo
    # dashboard_pre_prompt = "Given a list of commands, respond with the corresponding string text\
    #     drill holes 1001 to 1015 'start,drill,json,1001,1015'\
    #     de-burr holes 1001 to 1015 'start,de-burr,json,1001,1015'\
    #     paint holes 1001 to 1015 'start,paint,json,1001,1015'\
    #     stop: 'stop'\
    #     resume: 'resume'\
    #     reset: 'reset'\
    #     home: 'home'\
    #     de-burr holes from 1001 to 1015 in workpiece 101 and fiducial 102\
    #     'start,de-burr,json,1001,1015,101,102'\
    #     ---\
    #     stop the current operation and go to home\
    #     'stop,home'\
    #     Your response should follow exactly this pattern, and don't add any extra unneeded text."
        
    # response_to_dashboard = openai.ChatCompletion.create(
    #     model='gpt-3.5-turbo',
    #     messages=[
    #         {"role": "system", "content": "You are a text-generating robot, you output text strings exactly as instructed.\n" + dashboard_pre_prompt},
    #         {"role": "user", "content": dashboard_instruction},
    #     ],
    #     top_p= 0.1,
    #     temperature= 0,
    #     max_tokens=100
    # )
    
    ## ChatGPT text-davinci-003
    # dashboard_pre_prompt = "You are a text-generating robot, you follow given patterns exactly. Given a list of commands, respond with the corresponding string text\
    #         drill holes 1001 to 1015\
    #         'start,drill,json,1001,1015'\
    #         ---\
    #         de-burr holes 1001 to 1015\
    #         'start,de-burr,json,1001,1015'\
    #         ---\
    #         paint holes 1001 to 1015\
    #         'start,paint,json,1001,1015'\
    #         ---\
    #         stop\
    #         'stop'\
    #         ---\
    #         resume\
    #         'resume'\
    #         ---\
    #         reset\
    #         'reset'\
    #         ---\
    #         home\
    #         'home'\
    #         ---\
    #         de-burr holes from 1001 to 1015 in workpiece 101 and fiducial 102\
    #         'start,de-burr,json,1001,1015,101,102'\
    #         ---\
    #         stop the current operation and go to home\
    #         'stop,home'\
    #         Your response should follow exactly this pattern, and don't add any extra unneeded text. Don't repeat text from the prompt."
    dashboard_pre_prompt = "Given a list of commands, respond with the corresponding text\
        drill holes 1xxx to 1yyy 'start,drill,json,1xxx,1yyy'\
        de-burr holes 1xxx to 1yyy 'start,de-burr,json,1xxx,1yyy'\
        paint holes 1xxx to 1yyy 'start,paint,json,1xxx,1yyy'\
        stop 'stop'\
        resume 'resume'\
        reset 'reset'\
        home 'home'\
        de-burr holes from 1xxx to 1yyy in workpiece 1xx and fiducial 1yy\
        'start,de-burr,json,1xxx,1yyy,1xx,1yy'\
        Your response should follow exactly this pattern, and don't add any extra unneeded text.\
        if you miss any information, ask a question."
    # prompt_input = "De-burr holes from 1001 to 1015"

    response_to_dashboard = openai.Completion.create(
        model='gpt-3.5-turbo-instruct',
        prompt=dashboard_pre_prompt + "\n" + dashboard_instruction,
        top_p= 0.05,
        temperature= 0,
        max_tokens=100
    )
    response_to_dashboard_text = response_to_dashboard.choices[0].text.strip()
    print("response_to_dashboard_text: " + response_to_dashboard_text)
    response_to_dashboard_text = response_to_dashboard_text.replace("'",'').strip().split(',')
    print("response_to_dashboard_text: "+ str(response_to_dashboard_text))

    # exit(1)
    
    ## Llama2-70b-chat
    # pre_prompt = "Given a list of commands, respond with the corresponding text\
    #     drill holes 1001 to 1015 'start,drill,json,1001,1015'\
    #     de-burr holes 1001 to 1015 'start,de-burr,json,1001,1015'\
    #     paint holes 1001 to 1015 'start,paint,json,1001,1015'\
    #     stop: 'stop'\
    #     resume: 'resume'\
    #     reset: 'reset'\
    #     home: 'home'\
    #     de-burr holes from 1001 to 1015 in workpiece 101 and fiducial 102\
    #     'start,de-burr,json,1001,1015,101,102'\
    #     ---\
    #     stop the current operation and go to home\
    #     'stop,home'\
    #     Your response should follow exactly this pattern, and don't add any extra unneeded text."
    # # prompt_input = "De-burr holes from 1001 to 1015"

    # output = replicate.run(
    #     "replicate/llama-2-70b-chat:2796ee9483c3fd7aa2e171d38f4ca12251a30609463dcfd4cd76703f22e96cdf",
    #     input={
    #         "prompt": pre_prompt + "\n" + dashboard_instruction,
    #         "temperature": 0.1,
    #         "top_p": 0.1,
    #         "max_length": 128,
    #         "repetition_penalty": 1,
    #     },
    # )  # Model parameters

    # # print("Test de-burr")

    # response_to_dashboard_text = ''
    # response_to_dashboard = []
    # for item in output:
    #     response_to_dashboard_text += item
    #     # print(item)
    #     # response_to_dashboard.append(item)
    # # print(response_to_dashboard)
    # response_to_dashboard_text = response_to_dashboard_text.strip().split(",")

    # print(response_to_dashboard_text)
    
    
    if 'json' in response_to_dashboard_text:
        json_pre_prompt = 'Given a template for a JSON file, generate a JSON file using the same structure and pattern.\
        {\
            "Blacklist":[],\
            "Whitelist":[],\
            "Workpiece-1xx":\
            {\
                "status":"notStarted"\
                "Fiducial-1xx":\
                {\
                    "status":"notStarted"\
                    "Hole-1xxx":\
                    {\
                        "Deburstatus":"notStarted",\
                        "Drillstatus":"notStarted",\
                        "Paintstatus":"notStarted",\
                    }\
                }\
            }\
        }\
        Your response should follow exactly this pattern, and don\'t add any extra unneeded text of any kind. format the answer as a json file directly'
        # print(response_to_dashboard_text)
        # for i in response_to_dashboard_text:
        #     print(i)
        json_instruction = "\nGenerating a JSON file for Workpiece " + response_to_dashboard_text[5] + ", Fiducial " + response_to_dashboard_text[6] + ", Holes " + response_to_dashboard_text[3] + " to " + response_to_dashboard_text[4]
        print(json_instruction)
        remarks = input("Remarks?")
        if remarks is not None:
            json_instruction = json_instruction + ".\n" + remarks
            # print("json_instruction")
        
        json_response = openai.Completion.create(
            model='text-davinci-002',
            prompt= json_pre_prompt + json_instruction,
            top_p= 0.025,
            temperature= 0,
            max_tokens=2000
        )
        json_string = json_response['choices'][0]['text']
        print(json_string)
        
        with open("test.json", "w") as file:
            try:
                json_obj = json.loads(json_string)
                json.dump(json_obj, file, ensure_ascii=False)
            except Exception as e:
                # # "Expecting , delimiter: line 34 column 54 (char 1158)"
                # # position of unexpected character after '"'
                # unexp = int(re.findall(r'\(char (\d+)\)', str(e))[0])
                # # position of unescaped '"' before that
                # unesc = json_string.rfind(r'"', 0, unexp)
                # json_string = json_string[:unesc] + r'\"' + json_string[unesc+1:]
                # # position of correspondig closing '"' (+2 for inserted '\')
                # closg = json_string.find(r'"', unesc + 2)
                # json_string = json_string[:closg] + r'\"' + json_string[closg+1:]
                print(e)
            
            # json.dump(json_obj, file, ensure_ascii=False)
    
    return response_to_dashboard_text
# # exit(1)
def dashboard_client(req):
    rospy.wait_for_service('dashboard')
    try:
        dashboard = rospy.ServiceProxy('dashboard', Dashboard)
        response = dashboard(req)
        return response
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)

if __name__ == "__main__":
    
    prompt = sys.argv[1]
    print(prompt)
    response = dashboard_prompt(prompt)
    print(response)
    # response = ['start', 'de-burr', 'json', '101', '102', '1001', '1015']
    if response[0] != 'start':
        req = response[0]
        print("Requesting %s"%(req))
        print("%s => %s"%(req, dashboard_client(req)))
    elif response[0] == 'start':
        req = response[0]+","+response[1]
        print("Requesting %s"%(req))
        print("%s => %s"%(req,dashboard_client(req)))

