#!/usr/bin/env python

import os
import csv
import argparse
import logging as log
from datetime import datetime
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


# Logging- Setup
log.basicConfig(format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
                handlers=[
                    log.FileHandler("speedtest.log"),
                    log.StreamHandler()
                ],
                level=log.DEBUG
                )

log.getLogger().setLevel(log.INFO)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--timeout", action="store",
                        dest="timeout", type=int, default=300)
    parser.add_argument("-o", "--output", action="store",
                        dest="output", default="tests")
    parser.add_argument("-d", "--debug", action="store_true", dest="debug")
    parser.add_argument("-f", "--front", action="store_true", dest="front")

    args = parser.parse_args()

    if args.debug:
        log.getLogger().setLevel(log.DEBUG)

    opts = Options()

    if not args.front:
        opts.add_argument("--headless")

    driver = webdriver.Chrome(options=opts)
    driver.implicitly_wait(args.timeout)
    log.info("Open speedtest.unitymedia.de")
    driver.get("https://speedtest.unitymedia.de/start/")
    log.info("Select cable")
    cablebtn = driver.find_element_by_id("icon-unitymedia-cable")
    cablebtn.click()
    startform = driver.find_element_by_id("speedtest-form")
    log.info("Start speedtest")
    startform.submit()

    try:
        detailsbtn = WebDriverWait(driver, args.timeout).until(
            EC.visibility_of_element_located((By.ID, "details-button"))
        )
        log.info("Checking details")
        detailsbtn.click()
        detailsbtn = driver.find_element_by_xpath("//td[@class='details'][1]")
        detailsbtn.click()

        # Get result in txt-form
        dlspd = driver.find_element_by_xpath(
            "//div[@class='download-result result']/div[@class='speed-end speed-display']").text
        upspd = driver.find_element_by_xpath(
            "//div[@class='upload-result result']/div[@class='speed-end speed-display']").text
        ping = driver.find_element_by_xpath(
            "//div[@class='ping-result result']/div[@class='speed speed-display']").text
        testanbieter = driver.find_element_by_xpath(
            "//div[@class='result-detail']/span[1]/span[@class='entry']").text
        testid = driver.find_element_by_xpath(
            "//div[@class='result-detail']/span[2]/span[@class='entry']").text
        testdate = driver.find_element_by_xpath(
            "//div[@class='result-detail']/span[@class='entry']").text

        sname = "{}/speedtest_{}.png".format(args.output,
                                             datetime.now().strftime("%Y%m%d%H%M"))

        log.info("Write result to file")
        os.makedirs(args.output, exist_ok=True)

        with open("{}/tests.csv".format(args.output), mode="a") as testlog:
            test_writer = csv.writer(
                testlog, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL)
            test_writer.writerow(
                [testid, testdate, testanbieter, dlspd, upspd, ping, sname])

        # Screenshot
        detailsview = driver.find_element_by_xpath(
            "//div[@class='result-detail'][1]")
        action = ActionChains(driver)
        action.move_to_element(detailsview)
        action.perform()
        driver.save_screenshot(sname)
        log.info("Screenshot saved under {}".format(sname))
    except Exception as e:
        log.error(e)
    finally:
        driver.quit()


if __name__ == "__main__":
    SystemExit(main())
