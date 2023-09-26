from connector import *
import json

def build_payload(file_path,logs):

    log = {"service_id": "5d24b10e56d4e549a3942585", "log_type": "Instant test run", "tag": "ThousandEyes", "message": logs}

    #para construir una entry del archivo
    file_name = file_path
    f = open(file_name, 'a+')  # open file in append mode
    f.write(json.dumps(log)+"\n")
    f.close()

    return 0



def get_agents_info(headers, file_path, aid):

    #get info of agents
    agents_endp = 'https://api.thousandeyes.com/v6/agents.json?aid=%s&agentTypes=ENTERPRISE_CLUSTER,ENTERPRISE' % aid
    agents = get_data(headers,agents_endp)

    if "agents" in agents:
        for agent in agents["agents"]:

            agent_payload = {}

            #AQUI TENEMOS DOS OPCIONES: O ES CLUSTER O ES UN ENTERPRISE NORMAL. Primero hacemos normal
            if agent["agentType"] == "Enterprise":

                errors_list = [item["description"] for item in agent["errorDetails"]]
                errors = ", ".join(errors_list)


                
                agent_payload = { "agentName" : agent["agentName"],
                                 "agentId" :agent["agentId"],
                                 "enabled":"TRUE" if agent["enabled"] == 1 else "FALSE",
                                 "agentState":agent["agentState"],
                                 "location":agent["location"],
                                 "utilization":agent["utilization"] if "utilization" in agent else " ",
                                 "errors": errors,
                                 "hostname":agent["hostname"],
                                 "ipAddresses":agent["ipAddresses"][0],
                                 "targetForTests":agent["targetForTests"],
                                 "cluster":" ",
                                 "aid": aid
                                 }
                

                build_payload(file_path,agent_payload)

            if agent["agentType"] == "Enterprise Cluster":
                
                for cluster in agent["clusterMembers"]:

                    errors_list = [item["description"] for item in cluster["errorDetails"]]
                    errors = ", ".join(errors_list)


                    agent_payload = { "name" : cluster["name"],
                                    "agentId" :agent["agentId"],
                                    "enabled":"TRUE" if agent["enabled"] == 1 else "FALSE",
                                    "agentState":cluster["agentState"],
                                    "location":agent["location"],
                                    "utilization":agent["utilization"] if "utilization" in agent else " ",
                                    "errors": errors,
                                    "hostname":" ",
                                    "ipAddresses":cluster["ipAddresses"][0],
                                    "targetForTests":cluster["targetForTests"],
                                    "cluster":agent["agentName"],
                                    "aid": aid
                                    }
                    

                    build_payload(file_path,agent_payload)

    print("\nYour current agents have been listed. Refer to the agents_info.log to see the details.")


    return 0





#####################
#       MAIN
#####################

#These are the only values can be modified on the script#
accounts = ["Dani's sandbox"]
OAuth = "XXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXX"

################################################
#   Do not modify these parameters
################################################

file_path = "agents_info.log"

# API
headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + OAuth,
    }

accounts_dict = get_accounts(headers)

with open(file_path, 'w'):
    pass


for acc in accounts:
    get_agents_info(headers, file_path, accounts_dict[acc])