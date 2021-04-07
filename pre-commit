#!/usr/bin/python
"""
Referencing current branch in github readme.md[1]

This pre-commit hook[2] updates the README.md file's
to point to the nbviewer link for the current branch.

[1] http://stackoverflow.com/questions/18673694/referencing-current-branch-in-github-readme-md
[2] http://www.git-scm.com/book/en/v2/Customizing-Git-Git-Hooks
"""
import subprocess

# Hard-Coded for your repo (ToDo: get from remote?)
GITHUB_USER="cerminar"
REPO="plot-drawing-tools"

print "Starting pre-commit hook..."

BRANCH=subprocess.check_output(["git",
                                "rev-parse",
                                "--abbrev-ref",
                                "HEAD"]).strip()

print 'on branch: {}'.format(BRANCH)

# Output String with Variable substitution
new_link="[Notebook Viewer (NBViewer)](https://nbviewer.jupyter.org/github/{GITHUB_USER}/{REPO}/tree/{BRANCH}/)".format(BRANCH=BRANCH,
                                                                                                     GITHUB_USER=GITHUB_USER,
                                                                                                     REPO=REPO)

sentinel_str="[Notebook Viewer (NBViewer)]"

readmelines=open("README.md").readlines()
with open("README.md", "w") as fh:
    for aline in readmelines:
        if sentinel_str in aline and new_link != aline:
            # print "Replacing:\n\t{aline}\nwith:\n\t{new_link}".format(
            #        aline=aline,
            #        new_link=new_link)
            fh.write(new_link)
        else:
            fh.write(aline)

subprocess.check_output(["git", "add", "README.md" ])

print "pre-commit hook complete."
