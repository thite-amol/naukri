#! python3
# Naukri Daily update - Using firefox
import sys
import time
import logging
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC


# Update your username, password and mobile number before start
username = ""
password = ""
mob = ""

naukri_url = "https://login.naukri.com/nLogin/Login.php"
profile_url = 'https://www.naukri.com/mnjuser/profile'

log_file_path = "naukri.log"
logging.basicConfig(level=logging.INFO,
                    filename=log_file_path,
                    format='%(asctime)s    : %(message)s')

def is_element_present(driver, how, what):
    try:
        driver.find_element(by=how, value=what)
    except NoSuchElementException:
        return False
    return True


def tear_down(driver):
    try:
        driver.close()
        logging.info('Driver Closed Successfully')
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        line_no = str(exc_tb.tb_lineno)
        logging.info('Error : %s : %s at Line %s.' % (type(e), e, line_no))

    try:
        driver.quit()
        logging.info('Driver Quit Successfully')
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        line_no = str(exc_tb.tb_lineno)
        logging.info('Error quitting: %s : %s at Line %s.' % (type(e), e, line_no))
        print('Error quitting: %s : %s at Line %s.' % (type(e), e, line_no))


def naukri_login():
    status = False

    try:
        driver = webdriver.Firefox()
        driver.maximize_window()
        print("Firefox Launched!")
        logging.info("Firefox Launched!")

        driver.implicitly_wait(3)
        driver.get(naukri_url)

        if 'Naukri.com' in driver.title:
            print("We are in")
            logging.info("We are in")

        if is_element_present(driver, By.ID, "emailTxt"):
            email_field_element = driver.find_element_by_id("emailTxt")
            time.sleep(1)
            pass_field_element = driver.find_element_by_id("pwd1")
            time.sleep(1)
            login_button = driver.find_element_by_xpath("//*[@type='submit' and @value='Login']")

        elif is_element_present(driver, By.ID, "usernameField"):
            email_field_element = driver.find_element_by_id("usernameField")
            time.sleep(1)
            pass_field_element = driver.find_element_by_id("passwordField")
            time.sleep(1)
            login_button = driver.find_element_by_xpath('//*[@type="submit"]')

        else:
            print('Look like we don\'t have an element to login')
            logging.info('Look like we don\'t have an element to login')

        if email_field_element is not None:
            email_field_element.clear()
            email_field_element.send_keys(username)
            pass_field_element.clear()
            pass_field_element.send_keys(password)
            time.sleep(1)
            login_button.send_keys(Keys.ENTER)

            result = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'search-jobs')))
            if result:
                print('Logged in')
                logging.info('Logged in')
                status = True
                return (status, driver)
            else:
                print('Something went wrong while trying to login')
                logging.info('Something went wrong while trying to login')
                return (status, driver)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        line_no = str(exc_tb.tb_lineno)
        logging.info('Error while logging in to account: %s : %s at line %s.\n' % (type(e), e, line_no))
        print('Error while logging in to account: %s : %s at line %s.' % (type(e), e, line_no))


def update_profile(driver):
    try:
        driver.get(profile_url)
        driver.implicitly_wait(10)
        mob_xpath = '//*[@id="mob_number"]'
        profedit_xpath = "/html/body/div[2]/div/div[1]/span/div/div/div/div/div/div[1]/div[1]/div/div[1]/div/div[2]/div[1]/div/div[1]/em"
        save_xpath = '//*[@id="saveBasicDetailsBtn"]'
        element = driver.find_element_by_xpath(profedit_xpath)
        driver.execute_script("arguments[0].click();", element)
        time.sleep(10)

        if is_element_present(driver, By.XPATH, save_xpath):
            mob_field_element = driver.find_element_by_xpath(mob_xpath)
            mob_field_element.clear()
            mob_field_element.send_keys(mob)
            driver.implicitly_wait(2)

            save_field_element = driver.find_element_by_xpath(save_xpath)
            save_field_element.send_keys(Keys.ENTER)
            driver.implicitly_wait(3)
            if is_element_present(driver, By.XPATH, "//*[text()='today']"):
                logging.info('Mobile number updated successfully')
                print('Mobile number updated successfully')
            else:
                logging.info('Mobile number updation failed')
                print('Mobile number updation failed')
        time.sleep(5)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        line_no = str(exc_tb.tb_lineno)
        logging.info('Error updating mobile number: %s : %s at Line %s.\n' % (type(e), e, line_no))
        print('Error updating mobile number: %s : %s at Line %s.' % (type(e), e, line_no))


def main():
    driver = None
    try:
        status, driver = naukri_login()
        if status:
            update_profile(driver)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        line_no = str(exc_tb.tb_lineno)
        logging.info('Error updating profile: %s : %s at Line %s.' % (type(e), e, line_no))
        print('Error updating profile: %s : %s at Line %s.' % (type(e), e, line_no))

    finally:
        tear_down(driver)


if __name__ == '__main__':
    main()
