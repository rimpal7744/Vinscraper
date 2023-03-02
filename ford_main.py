from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import random
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from csv import writer


driver = webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()
sleep(5)

#reading vin from csv
def reading_vins(input_file):
    df=pd.read_csv(input_file)
    Vin_list=df.VIN.tolist()
    return Vin_list


#writing data to csv
def writingg(data_list):
    with open('out_ford.csv', 'a') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(data_list)
        f_object.close()

def main(input_file):
    Vin_list=reading_vins(input_file)
    driver.get('https://www.ford.com/support/recalls/')
    count=182
    for vin in sorted(Vin_list):
        count+=1
        driver.find_element(by=By.XPATH, value="//input[@placeholder='Enter Your Ford VIN*']").clear()
        sleep(random.randint(1,2))
        driver.find_element(by=By.XPATH, value="//input[@placeholder='Enter Your Ford VIN*']").send_keys(str(vin))
        sleep(random.randint(2,4))
        driver.find_element(by=By.XPATH, value="//button[@aria-label='See Recalls']").send_keys(Keys.RETURN)

        sleep(random.randint(8,11))
        if str(driver.current_url)=='https://www.ford.com/support/recalls-details/':
            print('match')
            try:
                driver.find_element(by=By.XPATH, value="//div[@class='recalls-section no-recalls']")
                data_list=[vin, 'no', '','' , '', '', '', '', '']
                writingg(data_list)
            except:
                print('recall_present')
                recaall=driver.find_element(by=By.XPATH, value="//div[@class='recalls-section']")
                all_recalls=recaall.find_elements(by=By.XPATH, value=".//div[@class='chevron-down']")
                for re in all_recalls:
                    re.click()
                    sleep(random.randint(2,4))
                    try:
                        name = driver.find_element(by=By.XPATH, value="//span[@class='accordion-title expanded']").text
                    except:
                        name=''
                    try:
                        status = driver.find_element(by=By.XPATH, value="//span[@class='accordion-subtitle']").text
                    except:
                        status=''
                    daaataa = driver.find_element(by=By.XPATH, value="//div[@data-testid='accordion-description']")
                    all_labels=daaataa.find_elements(by=By.XPATH, value="//div[@class='support-accordion-description-label']")
                    all_content=daaataa.find_elements(by=By.XPATH, value="//div[@class='support-accordion-description-content']")
                    issue_date=''
                    Description=''
                    Safety=''
                    Remedy=''
                    nhtsa=''
                    for i,j in zip(all_labels,all_content):
                        print(i.text,'==',j.text)
                        if i.text=='Issue Date':
                            issue_date=j.text
                        if i.text=='Description':
                            Description=j.text
                        if i.text=='Safety Risk':
                            Safety=j.text
                        if i.text=='Remedy':
                            Remedy=j.text
                        if i.text=='Campaign/NHTSA#':
                            nhtsa=j.text

                    data_list=[vin,'yes',name,status,nhtsa,issue_date,Description,Safety,Remedy]
                    writingg(data_list)
                    recaall.find_element(by=By.XPATH, value=".//div[@class='chevron-up']").click()
                    sleep(random.randint(2,4))


            driver.get('https://www.ford.com/support/recalls/')
            sleep(random.randint(2,4))
        else:
            data_list = [vin, 'invalid_vin', '', '', '', '', '', '', '']
            writingg(data_list)



if __name__ == "__main__":
    #give input csv file here having Vin with column name VINS
    input_file='ford_links.csv'
    #main function for extraction
    main(input_file)