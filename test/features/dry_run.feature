Feature: Dry Runs

Background: Initilise App
    Given I have flask app in dry run mode

Scenario: Get Interfaces - CLI
    Given I send a get request to url
    Then I should get a successful reponse code
    And The body should contain the CLI commands

Scenario: Stop Server
    Given I stop the server
