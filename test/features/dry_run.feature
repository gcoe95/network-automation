Feature: Dry Runs

Background: Initilise App
    Given I have flask app in dry run mode

Scenario: Get Interfaces - CLI
    Given I send a GET request to url
    Then I should get a successful reponse code
    And The body should contain the CLI commands

Scenario: Configure Loopback
    Given I send a POST request
    Then I should get a successful reponse code
    And The body should contain the create netconf

Scenario: Delete Loopback
    Given I send a DELETE request
    Then I should get a successful reponse code
    And The body should contain the delete netconf