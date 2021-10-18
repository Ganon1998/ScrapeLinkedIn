from selenium import webdriver
from datetime import date
import sqlite3

today = date.today()

# parse jobs
def getJobs(JobsGatheredArray):
    jobsDB = []
    for x in range(len(JobsGatheredArray)):
        temp = JobsGatheredArray[x].split("\n")
        # skip the words after This job has an update
        if temp[0] == 'This entry has an update':
            jobsDB.append(temp[1:])
        else:
            jobsDB.append(temp)

    # write to backup file
    num = 1
    with open('jobList.txt', 'a') as f:
        for line in jobsDB:
            f.write(str(num) + ".) ")
            for i in line:
                f.write(i)
                f.write(" ")
            f.write("\n")
            num += 1

    file = open('jobList.txt', 'a')
    file.write('Backed up on: ' + str(today))
    file.close()

    return jobsDB


email = 'jgreene097@gmail.com'
pw = 'Le@g@00'

# find webdriver
browser = webdriver.Chrome(executable_path='C:\\Users\\Sense\\chromedriver.exe')

browser.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')

elem = browser.find_element_by_id('username')  # Find the search box
elem.send_keys(email)

elem = browser.find_element_by_id('password')
elem.send_keys(pw)

print('Logged in')
browser.implicitly_wait(4)

# click on jobs and then click on my jobs
browser.find_element_by_xpath('//*[@id="organic-div"]/form/div[3]/button').click()
browser.find_element_by_xpath('//*[@id="ember23"]/span').click()
browser.implicitly_wait(4)

# go to saved jobs
browser.get('https://www.linkedin.com/my-items/saved-jobs')

# go to applied jobs
browser.get('https://www.linkedin.com/my-items/saved-jobs/?cardType=APPLIED')

i = 1
j = 1
JobsGatheredArray = []

while True:
    try:
        pages = int(input("How many pages should be scraped? "))
        break
    except ValueError:
        print("Try again")

print("Collecting jobs")
while (i != pages):
    # wait for page to fully load so all elements load
    browser.implicitly_wait(6)
    # go to the list of applied jobs and scrape the text from the array
    for Entries in browser.find_elements_by_xpath("//ul[@class='reusable-search__entity-results-list list-style-none']/li"):
        JobsGatheredArray.append(Entries.text)

    browser.get('https://www.linkedin.com/my-items/saved-jobs/?cardType=APPLIED&start=' + str(j) +'0')
    j += 1
    i += 1

# finish
browser.quit()
print("Parsing jobs")

# parse jobs
jobEntries = getJobs(JobsGatheredArray)

# get access to a db file I made
conn = sqlite3.connect('jobDB.db')
# create cursor object to gain access to methods like commit and execute
cur = conn.cursor()
conn.commit()


for job in jobEntries:
    cur.execute('''INSERT INTO JobsTable (Title, Company, Location, Date)
    VALUES (?, ?, ?, ?);''', (job[0], job[1], job[2], job[3]))
    conn.commit()

conn.close()
