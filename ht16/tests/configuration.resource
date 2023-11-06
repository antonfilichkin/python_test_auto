*** Settings ***
Documentation    Test configuration
Library          SeleniumLibrary
Library          ../libs/ScreenshotListener.py

*** Variables ***
${HOME_PAGE}    https://www.demoblaze.com
${USER_NAME}    Name27102023
${USER_PASS}    Name27102023

*** Keywords ***
Open And Set Up Driver
    [Documentation]    Creates and configures driver and opens sut
    [Arguments]    ${HOME_PAGE}    ${BROWSER}

    Open Browser    ${HOME_PAGE}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Implicit Wait    5s


Clean Up Cart Teardown
    [Teardown]
    [Documentation]    Cleans up cart

    Open Cart

    IF    ${TEST_TAGS} contains Clean_cart
        Run Keyword and Ignore Error    Empty The Cart
    END