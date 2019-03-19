from jira import JIRA
import os
from ete3 import Tree, NodeStyle, TreeStyle
import argparse

# Initialize JIRA connection
def initialize_jira():
    try:
        username = os.environ.get('JIRA_USERNAME')
        password = os.environ.get('JIRA_PASSWORD')
        host = os.environ.get('JIRA_HOST')
        options = { 'server': '{}'.format(host)}
    except Exception as e:
        print("Failed to load credentials from environment! Please ensure that JIRA_USERNAME and JIRA_PASSWORD are exported! {}".format(e))
    try:
        jira = JIRA(options, basic_auth=(username, password))
    except Exception as e:
        print("JIRA Connection failed! {}".format(e))
        exit(1)

    return jira

def run():
    epic_list = gather_epics(args.project)
    autoinc = 0
    for epic_issue in epic_list:
        epic_obj = jira.issue(epic_issue)
        epic_children = gather_children(epic_issue)
        if len(epic_children) == 0:
            print('{} has no unresolved issues, popping it from the tree...'.format(epic_issue))
        else:
            epic = tree.add_child(name="{} - {}  ".format(epic_issue, epic_obj.fields.summary))

        for issue in epic_children:
            issue_links = gather_links(issue)
            issue = epic.add_child(name="{} - {} ({}) ".format(issue, issue.fields.summary, issue.fields.status))

            for subtask in issue_links:
                subtask = issue.add_child(name=subtask)
    orphans = tree.add_child(name="Orphaned issues  ")
    orphan_issues = gather_orphans()
    for issue in orphan_issues:
        orphans.add_child(name="{} - {} ({}) ".format(issue, issue.fields.summary, issue.fields.status))
    print(tree.get_ascii(show_internal=True))

# Gather all epics in the specified project
def gather_epics(project: str) -> list:
    epic_issue_list = []
    epic_issues = jira.search_issues('project = {} AND issuetype = "Epic"'.format(project))
    for issue in epic_issues:
        epic_issue_list.append(issue)
    return epic_issue_list


# Gather all stories with a link to this epic
def gather_children(epic: str) -> list:
    epic_children = []
    epic_child_issues = jira.search_issues('"Epic Link" = "{}" AND resolution = Unresolved'.format(epic))
    for issue in epic_child_issues:
        # issue.fields.assignee = "unassigned" if issue.fields.assignee is None else issue.fields.assignee
        if args.label or args.assignee:
            if args.label and args.assignee and issue.fields.assignee and (args.label in issue.fields.labels and args.assignee in issue.fields.assignee.name):
                epic_children.append(issue)
            if not args.label and issue.fields.assignee and (args.assignee in issue.fields.assignee.name):
                epic_children.append(issue)
            if not args.assignee and (args.label in issue.fields.labels):
                epic_children.append(issue)
        else:
            epic_children.append(issue)
    return epic_children

# Gather all tasks which implement the story
def gather_links(issue: str) -> list:
    issue_links = []
    linked_issues = jira.search_issues('issue in linkedIssues({},"is implemented by") AND resolution = Unresolved'.format(issue))
    for issue in linked_issues:
        issue_links.append(issue.fields.summary)
    return issue_links

# Gather orphaned issues that have our label of choice
def gather_orphans() -> list:
    orphan_links = []
    orphaned_issues = jira.search_issues('issuetype != "Epic" AND "Epic Link" = Null AND Project = "{}" AND resolution = Unresolved{}{}'.format(project, labelquery, assigneequery))
    for issue in orphaned_issues:
        orphan_links.append(issue)
    return orphan_links

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='A simple tree visualization tool for JIRA Projects. You must have the following environment variables exported: JIRA_HOST JIRA_USERNAME JIRA_PASSWORD')
    parser.add_argument("-p", "--project", help="the project that your epics are under", type=str, required=True)
    parser.add_argument("-n", "--project_name", help="A custom name for your project tree", type=str)
    parser.add_argument("-l", "--label", help="label to use for labelfilter", type=str)
    parser.add_argument("-a", "--assignee", help="the current issue assignee", type=str)
    args = parser.parse_args()
    if args.label:
        labelquery = " AND labels IN ('{}')".format(args.label)
    else:
        labelquery = ""
    if args.project_name:
        project_name = args.project_name
    else:
        project_name = args.project

    project = args.project

    if args.assignee:
        assigneequery = " AND assignee = '{}'".format(args.assignee)
    else:
        assigneequery = ""

    # Create an empty tree
    tree = Tree(name=project_name, format=3)


    # Initialize our connection to JIRA
    jira = initialize_jira()

    # Go time!
    run()
