import settings
import datetime
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from time import sleep

PATH = "C:\Program Files (x86)\chromedriver.exe"

def ping(c=0):
    if c!=0:
        print("attempt " + str(c) + ":", end=" ")
    try:
        ops = webdriver.chrome.options.Options()
        ops.add_argument("--headless")
        driver = webdriver.Chrome(executable_path=PATH, options=ops)
    except WebDriverException:
        print("error")
        driver.quit()
        return False
    driver.get(settings.URL)
    appointment = driver.find_element_by_id("dateText{}".format(settings.ID))
    if appointment.text!="No Appointments Available":
        appointment = appointment.text.split()
        date = appointment[5]
        time = appointment[6] + appointment[7]
        if (datetime.datetime.strptime(date, "%m/%d/%Y").date() - datetime.date.today()).days <= 7:
            driver.find_element_by_id("makebtn{}".format(settings.ID)).click()
            driver.get(driver.find_element_by_class_name("text-primary").get_attribute("href"))

            # enter information
            driver.find_element_by_id("firstName").send_keys(settings.PROFILE["firstName"])
            driver.find_element_by_id("lastName").send_keys(settings.PROFILE["lastName"])
            driver.find_element_by_id("email").send_keys(settings.PROFILE["email"])
            driver.find_element_by_id("phone").send_keys(settings.PROFILE["phone"])
            driver.find_element_by_xpath("//option[@value='Class E']").click()
            driver.find_element_by_id("birthDate").send_keys(settings.PROFILE["birthDate"])
            driver.find_elements_by_xpath("//input[@class='form-check-input pt-1 ml-1']")[1].click()
            if CANCEL_URL != "":
                try:
                    ops = webdriver.chrome.options.Options()
                    ops.add_argument("--headless")
                    d = webdriver.Chrome(executable_path=PATH, options=ops)
                except WebDriverException:
                    print("error")
                    d.quit()
                    driver.quit()
                    return False
                d.get(CANCEL_URL)
                d.find_element_by_class_name("btn btn-default hide-print").click()
            driver.find_element_by_xpath("//input[@class='btn btn-secondary g-recaptcha']").click()
            if c!=0:
                print("success")
            print("appointment booked for " + date + " " + time)
            sleep(5)
            print(f'confirmation number is: {driver.find_element_by_class_name("text-danger").text}')
            driver.quit()
            return True
        else:
            if c!=0:
                print("next available appointment is in more than a week")
            driver.quit()
            return False
    else:
        if c!=0:
            print("failed")
        driver.quit()
        return False

counter = 1
while not ping(counter):
    counter+=1
    sleep(30)