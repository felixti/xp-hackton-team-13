![Hacka_13 build](https://github.com/XP-Tech-Hackathon/xp-hackathon-team-13/workflows/Deplpy%20Hacka13%20Api/badge.svg)

# XP Hackathon <small>Team 13</small>
<img src="https://github.com/XP-Tech-Hackathon/xp-hackathon-team-13/blob/main/Diagram/logo.png" alt="logo"/>

## Motivação
O objetivo deste projeto é automatizar o processo abertura de janela de manutenção no Zabbix, tendo como gatilho a aprovação de uma gmud no ServiceNow.

<img src="https://github.com/XP-Tech-Hackathon/xp-hackathon-team-13/blob/main/Diagram/TechDay.png" alt="drawing" width="1000"/>

## Getting started
### Desenvolvimento
Para o desenvolvimento existem os seguintes requerimentos:
- Azure Functions Core Tools 3
- Python 3.7+ com pip
- .net 5
- Visual Studio Code
- nodejs com npm
- estar conectado na VPN da XP

>É recomendado instalar as extensões sugeridas pelo VS Code ao iniciar o projeto

A imagem abaixo ilustra o fluxo de desenvolvimento

<img src="https://github.com/XP-Tech-Hackathon/xp-hackathon-team-13/blob/main/Diagram/hacka13_dev_flow.svg" alt="drawing" width="1000"/>

### Como desenvolver
1. Baixe o projeto para seu computador

`git clone https://github.com/XP-Tech-Hackathon/xp-hackathon-team-13.git`

2. Copiar a estrutura de configurações do `local.settings.json.example` para o seu `local.settings.json` local substituindo os respectivos valores das variáveis

3. A partir do terminal, execute: 

`pip install -r requirements.txt`

4. A partir do terminal executar o seguinte comando:

`func host start`

5. Se tudo ocorrer bem, você deverá ver um output como abaixo:
```
$ func host start
Found Python version 3.8.5 (py).

Azure Functions Core Tools
Core Tools Version:       3.0.3233 Commit hash: d1772f733802122a326fa696dd4c086292ec0171 
Function Runtime Version: 3.0.15193.0


Functions:

        Hacka13HubConnector: [POST] http://localhost:7071/api/Hacka13HubConnector

For detailed output, run func with --verbose flag.
[2021-01-31T17:43:04.044Z] Worker process started and initialized.
[2021-01-31T17:43:07.670Z] Host lock lease acquired by instance ID '000000000000000000000000153BB330'.
[2021-01-31T19:02:02.283Z] Worker process started and initialized.
[2021-01-31T19:02:06.690Z] Host lock lease acquired by instance ID '000000000000000000000000153BB330'.
```

6. No exemplo acima, foi criado o seguinte enpoint `http://localhost:7071/api/Hacka13HubConnector` onde é possível realizar a ativação da azure function, este é o endereço que deve ser chamado caso o desenvolvedor queira testa-la.

### Teste
Existe uma collection que pode ser importada para dentro da ferramenta Postman: `test/HackathonNOC.postman_collection.json`.

Essa collection substitui o ServiceNow, de maneira que nos permite testar o código de uma maneira mais simples sem depender de uma instância do ServiceNow corretamente configurada e rodando. Essa chamada basicamente simula o evento de "mudança aprovada" que é o gatilho para a criação da janela de manutenção no Zabbix.

>Devido as limitações de segurança e permissionamento em máquinas onde usário não possui privilégios elevados não conseguimos integrar o sandbox do service now com a api em desenvolvimento local, pois o ServiceNow necessita de uma url para o seu webhook. Infelizmente o uso de ferramentas que favorecem este teste são bloqueados (ngrok, localtunnel).


### Configuração da instância do ServiceNow
Visite nossa [wiki](https://github.com/XP-Tech-Hackathon/xp-hackathon-team-13/wiki) para saber mais sobre detalhes de implementação e como configurar sua instância do ServiceNow.

### Useful resources for development
**ServiceNow**
* [webhooks/outbound integration](https://community.servicenow.com/community?id=community_search&q=Calling%20external%20webhook%2FAPI%20from%20service%20now)
* [table API](https://developer.servicenow.com/dev.do#!/reference/api/quebec/rest/c_TableAPI)

**Microsoft**
* [azure templates/deploy github actions](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/deploy-github-actions)
* [azure cli](https://docs.microsoft.com/en-us/cli/azure/functionapp/config/appsettings?view=azure-cli-latest)
* [github actions](https://docs.github.com/en/actions/learn-github-actions)
* [azure storage table with python](https://github.com/Azure-Samples/storage-table-python-getting-started/blob/master/table_basic_samples.py)

**Infrastructure as Code**
* [Farmer](https://compositionalit.github.io/farmer/)
