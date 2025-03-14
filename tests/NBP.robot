*** Settings ***
Documentation        This is some basic info about the whole suite
Library              SeleniumLibrary

# Run the script
# robot -d results tests/crm.robot
*** Variables ***


*** Test Cases ***
Should be able to check currencies value
    [Documentation]        This test checks if the gold page correctly displays currencies rate table.
    [Tags]                 1001    Smoke    Currencies

    # Initialize Selenium
    Set Selenium Speed     .2s
    Set Selenium Timeout   10s

    # Open the browser
    log                    Starting the test case
    open browser           http://127.0.0.1:5000    chrome

    # Resize browser window
    Set Window Size        width=2560    height=1440

    Page Should Contain    Displays information about various currencies and gold prices

    Click Link             id=Currencies
    Page Should Contain    Currencies

    sleep                  3s
    close browser


Should be able to check gold value
    [Documentation]        This test checks if the gold page correctly displays gold rate table.
    [Tags]                 1002    Smoke    Gold

    # Initialize Selenium
    Set Selenium Speed     .2s
    Set Selenium Timeout   10s

    # Open the browser
    log                    Starting the test case
    open browser           http://127.0.0.1:5000    chrome

    # Resize browser window
    Set Window Size        width=2560    height=1440

    Click Link             id=Gold
    Page Should Contain    Gold

    sleep                  3s
    close browser


Should be able to check calculator function
    [Documentation]        This test verifies that the currency calculator correctly converts 1 USD to PLN.

    [Tags]                 1003    Functional    Calculator

    # Initialize Selenium
    Set Selenium Speed     .2s
    Set Selenium Timeout   10s

    # Open the browser
    log                    Starting the test case
    open browser           http://127.0.0.1:5000    chrome

    # Resize browser window
    Set Window Size        width=2560    height=1440

    Click Link             id=Calculator
    Page Should Contain    Calculator

    # Check calculator function
    Select From List By Value   id=code    USD
    Input Text                  name=amount   1
    Click Button                Calculate
    Wait Until Page Contains    3.85

    sleep                  3s
    close browser


Should be able to check charts function
    [Documentation]        This test checks if the charts page correctly displays exchange rate history.
    [Tags]                 1004    Functional    Charts

    # Initialize Selenium
    Set Selenium Speed     .2s
    Set Selenium Timeout   10s

    # Open the browser
    log                    Starting the test case
    open browser           http://127.0.0.1:5000    chrome

    # Resize browser window
    Set Window Size        width=2560    height=1440

    Click Link             id=Charts
    Page Should Contain    Course chart from last 30 days

    # Check calculator function
    Select From List By Value   name=code    USD
    Click Button                Submit
    Wait Until Page Contains    date

    sleep                  3s
    close browser

*** Keywords ***

