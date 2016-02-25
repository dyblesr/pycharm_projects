from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re
import os

govia_acct = ''
govia_pin = ''
govia_tag = ''
transaction_log = 'giovia.log'


def main():

    # check if log file exists or not, if it doesnt create it.
    if not os.path.isfile(transaction_log):
        open(transaction_log, 'w').close()

    # load headless webdriver
    browser = webdriver.PhantomJS('phantomjs')

    # The following lines get the website to login,enter account details in the form and press submit button
    browser.get('https://www.govia.com.au/web/ssp/login/-/login/Login?')
    username = browser.find_element_by_id("frmContent_loginId")
    password = browser.find_element_by_id("frmContent_pin")
    username.send_keys(govia_acct)
    password.send_keys(govia_pin)
    browser.find_element_by_class_name("global-btn").submit()

    # Loads transaction URL and xpath selects the payments and charges tables
    browser.get('https://www.govia.com.au/web/ssp/transaction')
    transaction_xpath = '//*[@id="data-table"]'

    transaction_data = [] #define list for raw transaction data

    for tr in browser.find_elements_by_xpath(transaction_xpath):

        tds = tr.find_elements_by_tag_name('td')
        if tds:
            transaction_data.append([td.text for td in tds if td.text != 'Download data in a csv file'])

    new_log_lines = [] # define list for new log lines to be used for toll charge events

    for i in transaction_data:

        if i[0] == govia_tag:

            for m in xrange(0, len(i), 4):
                new_log_lines.append(i[m+1] + ' tag="' + i[m] + '" type="toll_activity" description="' + i[m+2] + '" toll_cost="' + i[m+3] + '"')

        elif i[0] != govia_tag:
            for m in xrange(0, len(i), 4):
                new_log_lines.append(i[m+1] + ' 12:00 doc_number="' + i[m] + '" type="payment" description="' + i[m+2] + '" payment_amount="' + i[m+3].rstrip('CR') + '"')

    # open log file and load the lines to compare what is in the new log lines_list.
    with open(transaction_log) as logged:
        old_log_lines = [line.rstrip('\n') for line in logged]

    for new_line in reversed(new_log_lines):
        if new_line not in old_log_lines:
            get_acct_balance = True
            with open(transaction_log, "a") as f:
                f.write(new_line + '\n')


    # lets get the details on the current account balance and write them to the log file ONLY if new events have been logged
    if get_acct_balance:
        acct_bal_raw = browser.find_element_by_class_name("no-space").text
        acct_bal_raw_split = acct_bal_raw.split('\n')
        acct_bal_amt_desc = acct_bal_raw_split[1].split('$')

        bal_event = time.strftime("%d/%m/%Y %H:%M") + ' type="account_balance" description="' + acct_bal_amt_desc[0].rstrip() + '" account_balance="' + acct_bal_amt_desc[1].strip('.') + '"'

        with open(transaction_log, "a") as f:
            f.write(bal_event + '\n')

if __name__ == "__main__":
    main()

