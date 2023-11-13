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


Open Set Up Driver And Login
    [Documentation]    Creates and configures driver, opens sut and logins
    [Arguments]    ${HOME_PAGE}    ${BROWSER}    ${USER_NAME}    ${USER_PASS}

    Open And Set Up Driver    ${HOME_PAGE}    ${BROWSER}
    Log in    ${USER_NAME}    ${USER_PASS}


Clean Up Cart
    [Documentation]    Cleans up cart

    Open Cart
    Run Keyword If    'Clean_cart' in ${TEST_TAGS}    Empty The Cart


Clean Up Cart and Close Browser
    [Documentation]    Cleans up cart

    Clean Up Cart
    Close Browser