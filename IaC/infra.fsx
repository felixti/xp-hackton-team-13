#r "nuget: Farmer"

open Farmer
open Farmer.Builders

let hacka13HubConnector = functions {
    name "azfhacka13"
    storage_account_name "azsahacka13"
    use_runtime FunctionsRuntime.Python
}

let template = arm {
    location Location.BrazilSouth
    add_resource hacka13HubConnector
}

template
|> Writer.quickWrite @"azf-deploy"