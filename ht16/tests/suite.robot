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
    [Tags]    All  Login

    Wait Until Element Is Visible    login2
    Click Element    login2

    Wait Until Element Is Visible    logInModal
    Element Should Be Visible    loginusername
    Element Should Be Visible    loginpassword

    Input Text    loginusername    ${USER_NAME}
    Input Text    loginpassword    ${USER_PASS}
    Click Button    css:button[onclick="logIn()"]

    Should Be Logged As    ${USER_NAME}


Add product to cart
    [Documentation]    Add product to cart
    [Tags]    All    Clean_cart
    [Setup]    Open Set Up Driver And Login    ${HOME_PAGE}  ${BROWSER}   ${USER_NAME}  ${USER_PASS}
    [Teardown]    Clean Up Cart

    Select Category    Monitors

    Select Product With The Highest Price
    Element Text Should Be    tbodyid >> css:h2    Apple monitor 24
    Element Text Should Be    tbodyid >> css:h3    $400 *includes tax

    Click Element    tbodyid >> css:a
    Handle Alert    timeout=5s

    Open Cart

    Element Text Should Be    tbodyid >> css:td:nth-child(2)    Apple monitor 24
    Element Text Should Be    tbodyid >> css:td:nth-child(3)    400
    Element Text Should Be    totalp    400
