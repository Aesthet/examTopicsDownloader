import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

exam = "devops-pro"

if exam == "sa-pro":
    base = "Professional SAP-C02"
    ensure_on_page = "AWS Certified Solutions Architect - Professional SAP-C02"
elif exam == "data-eng":
    base = "Data Engineer - Associate DEA-C01"
    ensure_on_page = "AWS Certified Data Engineer - Associate DEA-C01"
else:
    base = "Professional DOP-C02"
    ensure_on_page = "AWS Certified DevOps Engineer - Professional DOP-C02"

search_for = f"{base} question {{question_number}} examtopics"


def check_question_and_press_keys(question_number):
    try:
        # Check if the div with the specific question number exists
        question_div = driver.find_element(By.XPATH, f"//div[contains(text(), 'Question #: {question_number}')]")
        question_reg = driver.find_element(By.XPATH, f"//a[text()='{ensure_on_page}']")
        if question_div and question_reg:
            # Simulate Option + Shift + P key press
            # actions = ActionChains(driver)
            # link = driver.find_element(By.XPATH, "//a[text()='Show Suggested Answer']")
            # link.click()
            driver.execute_script('window.print();')
            # actions.key_down(Keys.ALT).key_down(Keys.SHIFT).send_keys('p').key_up(Keys.SHIFT).key_up(Keys.ALT).perform()
            return True
    except NoSuchElementException:
        return False


def search_and_navigate(question_number):
    driver.get('https://www.google.com')
    search_box = driver.find_element(By.NAME, 'q')
    search_box.send_keys(search_for.format(question_number=question_number))
    search_box.send_keys(Keys.RETURN)

    # Attempt to click the n two links if necessary
    n = 11
    for i in range(1, n):
        try:
            link = driver.find_element(By.XPATH, f"(//h3[@class='LC20lb MBeuO DKV0Md'])[{i}]/parent::a")
            if link.text:
                link.click()
            else:
                n += 1
                continue
            if not check_question_and_press_keys(question_number):
                driver.back()
            else:
                break
        except NoSuchElementException as e:
            print(f"Error: Link {i} not found for question number {question_number}.")
            raise NoSuchElementException(str(e))
    else:
        ll.append(question_number)
    driver.back()


# Loop through question numbers
if __name__ == "__main__":
    try:
        ll = []
        download_dir = "/Users/aesthet/Downloads/Certification/DevOps PRO/noanswer"
        chrome_options = webdriver.ChromeOptions()
        settings = {
            "recentDestinations": [{
                "id": "Save as PDF",
                "origin": "local",
                "account": "",
            }],
            "selectedDestinationId": "Save as PDF",
            "version": 2
        }
        prefs = {'printing.print_preview_sticky_settings.appState': json.dumps(settings),
                 "savefile.default_directory": download_dir,
                 "download.default_directory": download_dir,
                 }
        chrome_options.add_experimental_option('prefs', prefs)
        chrome_options.add_argument('--kiosk-printing')
        chrome_options.add_argument("--disable-search-engine-choice-screen")
        driver_path = '/Users/aesthet/sandbox/examTopicsDownloader/chromedriver'  # Update this path
        service = Service(executable_path=driver_path, chrome_options=chrome_options)
        # Initialize WebDriver with the updated service argument
        driver = webdriver.Chrome(service=service, options=chrome_options)

        driver.get('https://www.google.com')
        search_box = driver.find_element(By.ID, 'W0wltc')
        search_box.click()
        # for question_number in range(482, 490):  # AWS SA PRO
        for question_number in [230, 252, 278, 279, 280, 281]: #:  # AWS DEVOPS PRO missing
            search_and_navigate(question_number)
    finally:
        # driver.quit()
        print(ll)
