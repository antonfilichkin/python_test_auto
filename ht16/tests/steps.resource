*** Settings ***
Documentation    Custom steps keywords
Library          SeleniumLibrary

*** Keywords ***
Log in
    [Arguments]  ${USER_NAME}  ${USER_PASS}
    Wait Until Element Is Visible    login2
    Click Element    login2
    Input Text    loginusername    ${USER_NAME}
    Input Text    loginpassword    ${USER_PASS}
    Click Button    css:button[onclick="logIn()"]
    Should Be Logged As    ${USER_NAME}

Should Be Logged As
    [Arguments]  ${USER_NAME}
    Wait Until Element Is Visible  nameofuser  2
    Element Text Should Be  nameofuser  Welcome ${USER_NAME}
