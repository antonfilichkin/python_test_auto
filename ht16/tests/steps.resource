*** Settings ***
Documentation    Custom steps keywords
Library          SeleniumLibrary
Library          String
Library          ../libs/SeleniumCustom.py

*** Keywords ***
Log in
    [Documentation]    Performs login
    [Arguments]    ${USER_NAME}    ${USER_PASS}

    Wait Until Element Is Visible    login2
    Click Element    login2
    Input Text    loginusername    ${USER_NAME}
    Input Text    loginpassword    ${USER_PASS}
    Click Button    css:button[onclick="logIn()"]
    Should Be Logged As    ${USER_NAME}


Should Be Logged As
    [Documentation]    Checks if user name is present in the top menu
    [Tags]    Screenshot
    [Arguments]    ${USER_NAME}

    Wait Until Element Is Visible    nameofuser    5s
    Element Text Should Be    nameofuser    Welcome ${USER_NAME}


Select Category
    [Documentation]    Clicks on a side menu category and waits until page loads
    [Tags]    Screenshot
    [Arguments]    ${CATEGORY}

    Assign Id To Element    class:card    firstCardElement
    Click Element    xpath://div[@class='list-group']/a[text()='${CATEGORY}']
    Wait Until Element Is Not Visible    firstCardElement
    Wait Until Element Is Visible    class:card


Select Product With The Highest Price
    [Documentation]    Clicks on a product card with maximum price and waits for product page to load
    [Tags]    Screenshot

    ${CURRENT_ELEMENT_INDEX}=    Set Variable    0
    ${MAX_PRICE}=    Set Variable    0
    ${CARD_PRICE_WEBELEMENTS}=    Get WebElements    class:card-block h5

    FOR    ${CARD_PRICE}    IN    @{CARD_PRICE_WEBELEMENTS}
        ${CURRENT_ELEMENT_INDEX}=    Evaluate    ${CURRENT_ELEMENT_INDEX} + 1
        ${PRICE_AS_TEXT}=    Get Text    ${CARD_PRICE}
        ${PRICE_WITHOUT_CURRENCY_SIGN}=    Get Substring    ${PRICE_AS_TEXT}    1
        ${PRICE}=    Convert To Number    ${PRICE_WITHOUT_CURRENCY_SIGN}
        IF 	  ${PRICE} > ${MAX_PRICE}
            ${MAX_PRICE}=    Set Variable    ${PRICE}
            ${MAX_PRICE_ELEMENT_INDEX}=    Set Variable    ${CURRENT_ELEMENT_INDEX}
        END
    END

    Click Element    tbodyid >> class:card-block a:nth-child(${MAX_PRICE_ELEMENT_INDEX})


Open Cart
    [Documentation]    Opens cart
    [Arguments]    ${FAIL_EMPTY}=False

    Click Element    cartur
    IF    ${FAIL_EMPTY}
        Wait Until Element Is Visible    tbodyid >> css:tr td    5s
    ELSE
        Run Keyword And Ignore Error    Wait Until Element Is Visible    tbodyid >> css:tr td    5s
    END


Empty The Cart
    [Documentation]    Delete all the cart entries

    ${FIRST_ROW_DELETE_BUTTON_LOCATOR}=    Set Variable    tbodyid >> css:tr td a
    ${CART_ENTRIES_COUNT}=    Get Element Count    ${FIRST_ROW_DELETE_BUTTON_LOCATOR}

    WHILE    ${CART_ENTRIES_COUNT} > 0
        Log    Found records in cart - deleting the first one
        ${WEB_ELEMENT}=    Get WebElement    ${FIRST_ROW_DELETE_BUTTON_LOCATOR}
        Click Element    ${WEB_ELEMENT}
        Wait Until Element Is Stale    ${WEB_ELEMENT}    5s    1s
        ${CART_ENTRIES_COUNT}=    Get Element Count    ${FIRST_ROW_DELETE_BUTTON_LOCATOR}
    END
