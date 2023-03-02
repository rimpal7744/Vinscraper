from time import sleep
from selenium import webdriver
import pandas as pd
from csv import writer
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import random


driver = webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()
sleep(5)

#reading vin from csv
def reading_Vins(input_file):
    df=pd.read_csv(input_file)
    Vin_list=df.VIN.tolist()
    return Vin_list


def getting_data(vin,name,full_data,status,present):
    if 'NHTSA #' in full_data:
        nhtsa_index = full_data.index('NHTSA #') + 1
        nhtsa = full_data[nhtsa_index]
    else:
        nhtsa = ''
    if 'Date Issued:' in full_data:
        date_index = full_data.index('Date Issued:') + 1
        datee = full_data[date_index]
    else:
        datee = ''
    if 'Description' in full_data:
        dis_index = full_data.index('Description') + 1
        description = full_data[dis_index]
    else:
        description = ''
    if 'Safety Risk Description' in full_data:
        safety_index = full_data.index('Safety Risk Description') + 1
        safety = full_data[safety_index]
    else:
        safety = ''

    if 'Repair Description' in full_data:
        repair_index = full_data.index('Repair Description') + 1
        repair_des = full_data[repair_index]
    else:
        repair_des = ''
    return [vin,present,name,status,nhtsa,datee,description,safety,repair_des]


#writing data to csv
def writingg(data_list):
    with open('out_chevorlet.csv', 'a') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(data_list)
        f_object.close()


def main(input_file):
    Vin_list=reading_Vins(input_file)
    count=0
    for vin in sorted(Vin_list):
        count+=1
        print(count,'Vin_count')
        driver.get('https://www.chevrolet.com/ownercenter/recalls?vin='+str(vin))
        sleep(random.randint(4,7))
        try:
            driver.find_element(by=By.XPATH, value="//button[@data-tab-id='content1']")
            try:
                all_views=driver.find_elements(by=By.XPATH, value="//a[@class='no-href']")
                for a in all_views:
                    a.click()
                    sleep(random.randint(3,5))
                    try:
                        name = driver.find_element(by=By.XPATH, value="//div[@class='mb-10']")
                        name = name.find_element(by=By.XPATH, value=".//div[@class='gb-body1']").text
                    except:
                        name=''
                    rowss=driver.find_elements(by=By.XPATH, value="//div[@class='row']")
                    data_list=[]
                    for r in rowss:
                        full_data=r.text.split('\n')
                        for f in full_data:
                            data_list.append(f)

                    all_data=getting_data(vin,name,data_list,'incomplete','yes')
                    writingg(all_data)
                    driver.find_element(by=By.XPATH, value="//span[@class='icon-ui-close']").click()
                    sleep(random.randint(3,5))
            except:
                pass
            try:
                driver.find_element(by=By.XPATH, value="//button[@data-tab-id='content2']").click()
                sleep(random.randint(2,4))
                all_views2=driver.find_elements(by=By.XPATH, value="//a[@class='no-href']")
                if len(all_views2)>0:
                    for aa in all_views2:
                        try:
                            aa.click()
                            sleep(random.randint(2,3))
                            try:
                                secondname = driver.find_element(by=By.XPATH, value="//div[@class='mb-10']")
                                secondname = secondname.find_element(by=By.XPATH, value=".//div[@class='gb-body1']").text
                            except:
                                secondname = ''
                            rowsss = driver.find_elements(by=By.XPATH, value="//div[@class='row']")
                            data_list2 = []
                            for r in rowsss:
                                full_data = r.text.split('\n')
                                for f in full_data:
                                    data_list2.append(f)
                            all_data2 = getting_data(vin, secondname, data_list2, 'complete', 'no')
                            writingg(all_data2)
                            driver.find_element(by=By.XPATH, value="//span[@class='icon-ui-close']").click()
                            sleep(random.randint(3,5))
                        except:
                            pass

            except Exception as e:
                pass

        except Exception as e:
            datalist=[vin, 'no', '','' , '', '', '', '', '','']
            writingg(datalist)
            pass




if __name__ == "__main__":
    input_file='Chevorlet_links.csv'
    main(input_file)