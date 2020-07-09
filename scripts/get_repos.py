"""Script that generates a list of all the repos
of an organisation"""


import subprocess
import os
import json
import argparse
from helper import *


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--organisation", help="Provide the name of \
                            an organisation to get a list of its repos")
    args = parser.parse_args()
    return args


def get_repos(organisation_name):
    filename = "meta_data/" + organisation_name + ".json"
    command = "curl \"https://api.github.com/orgs/"+organisation_name+"/repos"
    pagination(command, 0, filename)
    with open(filename) as f:
        data = json.load(f)
        for repo in data:
            fob = open("meta_data/repos_list.txt", "a")
            fob.write(repo["full_name"]+"\n")
            fob.close()


if __name__ == "__main__":
    args = get_args()
    get_repos(args.organisation)
