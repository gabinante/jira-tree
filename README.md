# Jira Tree

This is a simple script intended to build a hierarchical tree visualization of a JIRA project.
It makes some assumptions about the structure of your JIRA project, namely that:
Project covers a project rather than several projects
Epics comprise a project
Stories build out epics (with Epic Links)
Tasks implement stories (with "is implemented by" // "implements" links

It would be trivial to change this script to include subtasks rather than "implements", but
JIRA is quite terrible at reporting on subtasks in general, so I tend not to use them.

## Usage
```
usage: visualize.py [-h] [-p PROJECT] [-n PROJECT_NAME] [-l LABEL] [-a ASSIGNEE]

optional arguments:
  -h, --help                                           Show this help message and exit
  -p PROJECT, --project                                The project that your epics are under
  -n PROJECT_NAME, --project_name                      A custom name for your project tree
  -l LABEL, --label LABEL                              Label to use for labelfilter
  -a ASSIGNEE, --assignee                              The current issue assignee

```

## Example
```
                                                                                         /-PHNXPROJ-47358 - Regression test - Verify that current upgrade path is not broken (New) 
                                                                                        |
                                                                                        |--PHNXPROJ-47357 - Create a Canary Server to launch deployment (New) 
                                 /PHNXPROJ-46800 - Support Phoenix Beta Deployment Tools   
                                |                                                       |--PHNXPROJ-47355 - Support multi-kernel upgrades using existing tools (Code Review) 
                                |                                                       |
                                |                                                        \PHNXPROJ-47214 - Gather Inventory information in realtime (In Progress) -create azure poller for cloud APIs
                                |
                                |                                                      /-PHNXPROJ-47205 - Test database restore Performance (In Progress) 
                                |-PHNXPROJ-46797 - Support Phoenix beta for limited GA  
                                |                                                      \-PHNXPROJ-44759 - Build Phoenix internals for multiple kernels (In Progress) 
                                |
                                |                                                                                 /-PHNXPROJ-47066 - Packer Job sometimes missing kernel updates (Waiting for Input) 
                                |-PHNXPROJ-44845 - Miscellaneous technical debt and bug fixes for Phoenix beta 1.0  
                                |                                                                                 \-PHNXPROJ-43224 - Config templates are same for different SKUs (New) 
                                |
                                |-PHNXPROJ-46803 - Monitoring and alerting for all components of Phoenix  -PHNXPROJ-47353 - Switch to pager duty and build JIRA Ticket Creation flow (New) 
                                |
                                |-PHNXPROJ-44552 - single vnet per node  -PHNXPROJ-47457 - api should acquire vnet space, peer to regional tools (In Progress) 
                                |
-Phoenix Project Beta Plan to GA                            /-PHNXPROJ-47456 - Code changes and bug fixes for Phoenix visualizations (New) 
                                |                          |
                                |                          |--PHNXPROJ-47450 - Investigation of new release system using blue/green deployments  (In Progress) 
                                |                          |
                                |                          |--PHNXPROJ-47444 - Ability to safely test new Phoenix release code (New) 
                                |                          |
                                |                          |--PHNXPROJ-47188 - Version bug with PhoenixMonitor (Code Review) 
                                |                          |
                                |                          |--PHNXPROJ-46893 - Nonprod Phoenix Provisioning (In Progress) 
                                |                          |
                                |                          |--PHNXPROJ-46882 - Jenkins Pipeline Improvements (In Progress) 
                                |                          |
                                |                          |--PHNXPROJ-46812 - Disaster recovery plan (New) 
                                |                          |
                                |                          |--PHNXPROJ-46805 - integrations with internal tools (In Progress) 
                                |                          |
                                |                          |--PHNXPROJ-46800 - Support releases of beta using current tooling (In Progress) 
                                 \Orphaned Project Issues -  
                                                           |--PHNXPROJ-46795 - Self-service tools support for customer service teams (New) 
                                                           |
                                                           |--PHNXPROJ-46793 - Secure & Maintainable Networking changes (New) 
                                                           |
                                                           |--PHNXPROJ-46792 - Multi-region support (New) 
                                                           |
                                                           |--PHNXPROJ-46791 - Upgrade existing customers to Phoenix Beta 1.0 (In Progress) 
                                                           |
                                                           |--PHNXPROJ-46758 - Refresh the beta instances with Phoenix Project changes (Dev Blocked) 
                                                           |
                                                           |--PHNXPROJ-46516 - Verify connectivity between microservices (Waiting for Input) 
                                                           |
                                                           |--PHNXPROJ-46494 - Ability to provision new nodes on-demand (Reopened) 
                                                           |
                                                           |--PHNXPROJ-45479 - customers should be able to upload their own images (Dev Blocked) 
                                                           |
                                                            \-PHNXPROJ-44552 - customers should be able to search images in the Phoenix directory (In Progress)

``` 
