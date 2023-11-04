*** Settings ***
Documentation    Test configuration
Library          SeleniumLibrary

*** Variables ***
${HOME_PAGE}    https://www.demoblaze.com
${USER_NAME}    Name27102023
${USER_PASS}    Name27102023

*** Keywords ***
Open And Set Up Driver
    [Arguments]  ${HOME_PAGE}  ${BROWSER}
    Open Browser  ${HOME_PAGE}  ${BROWSER}
    Maximize Browser Window
    Set Selenium Implicit Wait    5 seconds
