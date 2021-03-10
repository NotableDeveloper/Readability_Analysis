from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import csv
import time

def cal_text(path) : #웹 사이트에 접근하여 데이터 입력 후, 결과를 추출하는 함수
    driver = webdriver.Chrome(' ') # Webdriver 경로를 넣어주어야 함.
    driver.implicitly_wait(3)

    fp = open(path, mode = 'r', encoding = 'utf-8')
    text = fp.read()
    fp.close()

    input_text = []
    result = [0] * 3

    input_text.append(text)

    for input in input_text :
        driver.get('https://www.online-utility.org/english/readability_test_and_improve.jsp')
        time.sleep(3)
        driver.find_element_by_class_name('bigtextarea').send_keys(input)
        time.sleep(3)
        driver.find_element_by_xpath('/html/body/form/input[2]').click()
        time.sleep(3)

        xpath_result = ['/html/body/table[3]/tbody/tr[2]/td[2]', # Gunning Fog index
                        '/html/body/table[4]/tbody/tr[3]/td[2]', # Fk Level
                        '/html/body/table[5]/tbody/tr/td[2]'] # Fre

        temp_result = list()

        for i in xpath_result :
             temp_result.append(driver.find_element_by_xpath(i).get_attribute('textContent'))
             time.sleep(3)

        for j in range(0,3) :
            result[j] += int(float(temp_result[j]) / len(input_text))

    driver.close()
    return result

def save_csv(part, name, data) : #csv 파일로 저장하는 함수
    csv_name = 'D:\Readability\Result//' + part + '.csv' #csv 파일이 저장될 경로와 저장될 이름

    if os.path.isfile(csv_name) :
        csv_fp = open(csv_name, 'a', newline='')
        wr = csv.writer(csv_fp)
        wr.writerow([name,data[0],data[1],data[2]])
        csv_fp.close()

    else :
        csv_fp = open(csv_name, 'w', newline='')
        wr = csv.writer(csv_fp)
        wr.writerow(['','GFI','Fk Level','Fre'])
        wr.writerow([name,data[0],data[1],data[2]])
        csv_fp.close()

#Main
start_path = 'D:\Readability\Data' # 프로젝트의 데이터가 담긴 경로
dir_list = os.listdir(start_path)  # Date 디렉터리 내부의 디렉터리들을 저장
file_list = []

for dir in dir_list :
    file_list = os.listdir(start_path + '//' + dir) # cal_text 함수에게 경로를 넘겨주기 위한 Parsing
    for file in file_list :
        data = cal_text(start_path + '//' + dir + '//' + file) # 인물 하나에 대한 계산 결과를 저장
        name = file.replace(".txt","") # 해당 인물의 이름을 파일명을 통하여 저장
        save_csv(dir, name, data) # 해당 인물의 그룹명, 이름, 계산결과를 csv 파일로 저장
