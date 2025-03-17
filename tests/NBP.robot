*** Settings ***
Documentation        Automated tests created to test the NBP app
Library              SeleniumLibrary

# Run the script
# robot -d results tests/NBP.robot
Suite Setup       Open My Browser
Suite Teardown    Close Browser

*** Variables ***
${URL}                 http://127.0.0.1:5000
${BROWSER}             chrome
${WINDOW_WIDTH}        2560
${WINDOW_HEIGHT}       1440

*** Keywords ***
Open My Browser
    Open Browser          ${URL}    ${BROWSER}
    Set Window Size       ${WINDOW_WIDTH}    ${WINDOW_HEIGHT}
    Set Selenium Speed    .2s
    Set Selenium Timeout  10s


*** Test Cases ***
Should be able to check currencies value
    [Documentation]        This test checks if the currencies page correctly displays currencies rate table.
    [Tags]                 1001    Smoke    Currencies

    Page Should Contain    Displays information about various currencies and gold prices
    Click Link             id=Currencies
    Page Should Contain    Currencies
    Click Button           id=backButton


Should be able to check gold value
    [Documentation]        This test checks if the gold page correctly displays gold rate table.
    [Tags]                 1002    Smoke    Gold
    
    Click Link             id=Gold
    Page Should Contain    Gold
    Click Button           id=backButton


Should be able to check calculator function
    [Documentation]        This test verifies that the currency calculator correctly converts 1 USD to PLN.
    [Tags]                 1003    Functional    Calculator

    Click Link                   id=Calculator
    Page Should Contain          Calculator
    Select From List By Value    id=code    USD
    Input Text                   name=amount    1
    Click Button                 xpath=//input[@type='submit']
    Wait Until Page Contains     3.85
    Click Button                 id=backButton


Should be able to check charts function
    [Documentation]        This test checks if the charts page correctly displays exchange rate history.
    [Tags]                 1004    Functional    Charts

    Click Link                  id=Charts
    Page Should Contain         Course chart from last 30 days
    Select From List By Value   name=code    USD
    Click Button                xpath=//button[@type='submit']
    Wait Until Page Contains    date

