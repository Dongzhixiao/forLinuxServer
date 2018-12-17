# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 21:16:06 2017

@author: _cnic
"""


import logging
import urllib
import urllib.parse
import urllib.request
import time
import sys
import random
url = "https://www.baidu.com"
#url_cnic_login = "https://passport.escience.cn/oauth2/authorize?response_type=code&redirect_uri=http%3A%2F%2F159.226.29.10%2FCnicCheck%2Ftesttoken&client_id=58861&theme=simple"
#fp = urllib.request.urlopen(url_cnic_login)

def cnic_check(user_str,passwd_str, check_flag):
    # fp = open(file_name, 'r')
    # user_and_password = fp.readlines()
    # fp.close()
    # user_raw = user_and_password[0]
    # user_str = user_raw.split('\n')[0]
    # passwd_str = user_and_password[1].split('\n')[0]
    
    
    
    LOGIN_URL = "https://passport.escience.cn/oauth2/authorize?client_id=58861&redirect_uri=http%3A%2F%2F159.226.29.10%2FCnicCheck%2Ftesttoken&response_type=code&theme=simple"
    values = {
              'pageinfo':'userinfo',
              'userName':user_str,
              'password':passwd_str
              }
    postdata = urllib.parse.urlencode(values).encode()
    try:
        request = urllib.request.Request(LOGIN_URL, postdata)
        print('I am building request')
    except:
        print('Error Happen When request LOGIN')
        return False
    opener = urllib.request.build_opener()
    try:
        response = opener.open(request)
        print("I am getting response from request")
    except:
        print("Error Happened When fetching Response")
        return False
    tokeninfo = response.read().decode()
    print("The response Message is " + tokeninfo)
    tokeninfo_separate = tokeninfo.split(',')
    token_need = tokeninfo_separate[0]
    token_num1 = token_need.split(':')[1]
    if "token" not in token_need.split(':')[0]:
        print("Login failed. We didn't get token ^v^")
        return False
        
    token_num2 = token_num1.split('"')[1]
    print("The Token is: " + token_num2)
    print('')
    
    CHECK_FLAG = check_flag
    if CHECK_FLAG == 0:
        check_str = 'checkin'
    else:
        check_str = 'checkout'
    
    weidu0 = 39.97799936612442
    jingdu0 = 116.32936686204675
    fanwei = 0.001
    offset_weidu = random.uniform(-fanwei, fanwei)
    offset_jingdu = random.uniform(-fanwei, fanwei)
    
    weidu = weidu0 + offset_weidu
    jingdu = jingdu0 + offset_jingdu
    
    weidu_str = str(weidu)
    jingdu_str = str(jingdu)
    
    check_url = 'http://159.226.29.10/CnicCheck/CheckServlet?weidu='+ weidu_str + '&jingdu=' + jingdu_str + '&type=' + \
                    check_str +'&token=' + token_num2
                    
    time.sleep(5)
    print('waiting')
    response_final = urllib.request.urlopen(check_url)
    success_state = response_final.read()
    print(success_state)
    print('-------------------------------')
    print('-----Good Luck!----------------')
    str_state = str(success_state).split(',')[1]
    true_or_false = str_state.split('\"')[3]
    
    if true_or_false == 'true':
        print("Excellent!! The check has been completed successfully!")
        return True
    else:
        print("Sad~.......... Something wrong occured, please contact the administrator of cnic.")
        return False
    
if __name__ == '__main__':
    file_name = 'userinfo.txt'
    check_flag_str = input('Please Input Flag, 0 for checkin, 1 for check out: ')
    check_flag = int(check_flag_str)
    assert check_flag == 0 or check_flag ==1, "The input is not a effect flag."
    print("The flag you input is: " + str(type(check_flag)) + " " + str(check_flag))
    # success_flag = cnic_check(file_name, check_flag)
    # print("____________________")
    # print("--___________--")
    # print("The Final result is " + str(success_flag))
    