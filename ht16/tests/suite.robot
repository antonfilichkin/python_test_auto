*** Settings ***
Documentation    Test suite
Library          SeleniumLibrary

Resource         configuration.resource
Resource         steps.resource

Test Setup       Open And Set Up Driver  ${HOME_PAGE}  ${BROWSER}
Test Teardown    Close Browser


*** Variables ***
${BROWSER}    Chrome


*** Test Cases ***
Login existing user
    [Documentation]    Login with existing user credentials
    [Tags]    Login

    Wait Until Element Is Visible    login2
    Click Element    login2

    Wait Until Element Is Visible    logInModal
    Element Should Be Visible    loginusername
    Element Should Be Visible    loginpassword

    Input Text    loginusername    ${USER_NAME}
    Input Text    loginpassword    ${USER_PASS}
    Click Button    css:button[onclick="logIn()"]

    Should Be Logged As    ${USER_NAME}
