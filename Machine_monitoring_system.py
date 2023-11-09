import streamlit as st
from annotated_text import annotated_text
import json
import pandas as pd
import plotly.express as px
from PIL import Image

def count_statistic_data(select_tester):
    select_tester = select_tester.lower()
    pass_num=[0,0,0]
    fail_num=[0,0,0]
    f=open(select_tester+".log")
    lines=f.readlines()
    system_error=False
    for line in lines:
        if line=="system error\n":
            system_error=True
            break
        elif line=="start testing\n" or line=="finish testing\n":
            continue
        else:
            res=line.replace(":"," ")
            res=res.split(" ")
            testcase = int(res[1])-1
            res=line.split("->")
            res[1]=res[1].strip()
            if res[1]=="pass":
                pass_num[testcase]+=1
            else:
                fail_num[testcase]+=1
    pass_rate=[0,0,0]
    for i in range(0,3):
        if(pass_num[i]+fail_num[i]!=0):
            pass_rate[i]=pass_num[i]/(pass_num[i]+fail_num[i])
            pass_rate[i]=int(pass_rate[i]*100)
    return [pass_num, fail_num, pass_rate, system_error]

def updata_tester_status(tester_name):
    f=open(tester_name+'.log')
    last_line_a=f.readlines()[-1]
    if last_line_a=="system error\n":
        return ["ERROR","#faa"]
    elif last_line_a=="finish testing\n":
        return ["IDLE","gray"]
    else:
        if last_line_a=="start testing\n":
            return ["RUNNING  WIP_number:1 ","#afa"]
        else:
            res=last_line_a.replace(":"," ")
            res=res.split(" ")
            wip_num = int(res[3])+1
            return ["RUNNING  WIP_number:"+str(wip_num),"#afa"]
def update_all_tester_status():
    tester_a_status=updata_tester_status('tester_a')
    tester_b_status=updata_tester_status('tester_b')
    tester_c_status=updata_tester_status('tester_c')
    annotated_text("Tester_A: ",(tester_a_status[0],"", tester_a_status[1]))
    annotated_text("Tester_B: ",(tester_b_status[0],"", tester_b_status[1]))
    annotated_text("Tester_C: ",(tester_c_status[0],"", tester_c_status[1]))
def pie_chart(select_tester):
    data=count_statistic_data(select_tester)
    df=pd.DataFrame({
        'rate':["Pass rate","Fail rate"],
        'value':[(data[0][0]+data[0][1]+data[0][2]),(300-data[0][0]-data[0][1]-data[0][2])]
    })
    fig = px.pie(
                df,
                hole = 0.55,
                values = 'value',
                names = 'rate',
                color='rate',
                color_discrete_map={'Pass rate':'green','Fail rate':'red'})
    st.header(select_tester)
    st.plotly_chart(fig)

image = Image.open('Realtek_Logo.svg.png')
st.image(image,width=200)

st.title('即時監控機台系統')
select_tester = st.sidebar.selectbox(
    "機台編號",
    ("Overall","Tester_A","Tester_B","Tester_C")
)

update_all_tester_status()
if select_tester == "Overall" :
    pie_chart("Tester_A")
    pie_chart("Tester_B")
    pie_chart("Tester_C")
elif select_tester == "Tester_A" :
    f=open('rtk_tester_a.json')
    data=json.load(f)
    st.write("")
    st.write("**Device_id:**" + str(data['device_id']))
    st.write("**Device_name**:"+ data['device_name'])
    f.close()
elif select_tester == "Tester_B" :
    f=open('rtk_tester_b.json')
    data=json.load(f)
    st.write("")
    st.write("**Device_id:**" + str(data['device_id']))
    st.write("**Device_name**:"+ data['device_name'])
    f.close()
elif select_tester == "Tester_C" :
    f=open('rtk_tester_c.json')
    data=json.load(f)
    st.write("")
    st.write("**Device_id:**" + str(data['device_id']))
    st.write("**Device_name**:"+ data['device_name'])
    f.close()

if select_tester!="Overall":
    data=count_statistic_data(select_tester)
    df=pd.DataFrame({
        'test_case': [1, 2, 3],
        'total_WIP_number': [data[0][0]+data[1][0], data[0][1]+data[1][1], data[0][2]+data[1][2]],
        'pass / tested' : [str(data[0][0])+"/"+str(data[0][0]+data[1][0]), str(data[0][1])+"/"+str(data[0][1]+data[1][1]), str(data[0][2])+"/"+str(data[0][2]+data[1][2])],
        'pass_rate': [str(data[2][0])+"%", str(data[2][1])+"%", str(data[2][2])+"%"]
    })
    if data[3]==True: #system error
        st.error("**"+select_tester+" ERROR!!!!!!    Please check log file**")
    df = df.set_index('test_case')
    st.write(df)

