*** Settings ***
Documentation    Custom steps keywords
Library          SeleniumLibrary

*** Keywords ***
Log in
    [Documentation]    Performs Login
    [Arguments]    ${USER_NAME}    ${USER_PASS}
    Wait Until Element Is Visible    login2
    Click Element    login2
    Input Text    loginusername    ${USER_NAME}
    Input Text    loginpassword    ${USER_PASS}
    Click Button    css:button[onclick="logIn()"]
    Should Be Logged As    ${USER_NAME}

Should Be Logged As
    [Documentation]    Checks If User Name Is Present In The Top Menu
    [Tags]    Screenshot
    [Arguments]    ${USER_NAME}
    Wait Until Element Is Visible    nameofuser    5
    Element Text Should Be    nameofuser    Welcome ${USER_NAME}
