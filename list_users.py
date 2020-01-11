"""This script gets a list of repos as input.
For each repo, it gets a list of all the contrbutors and
filters out the 2nd quartile and saves their GitHub ID in names_list.txt """


import subprocess
import os
import json
from pprint import pprint
from helper import *


def get_names(repos_list):
    """Gets a list of contributors for all the repos in names_list,
       saves them and calls get_user_data() to process the data"""

    fob = open(repos_list, "r")
    repos = fob.readlines()
    fob.close()

    for repo in repos:
        filename = repo.split("/")
        filename = filename[1].strip()
        repo = str(repo).strip()
        command = "curl -H \"Authorization: token " + authentication + \
            "\" \"https://api.github.com/repos/"+repo+"/contributors"
        pagination(command, 0, ("meta_data/"+filename + ".json"))
        get_user_data("meta_data/"+filename+".json")


def get_user_data(filename):
        """Sorts users based on no of commits and saves
           the 2nd highest quartile to names_list.txt """
        try:
            users_unsorted={}
            with open(filename) as f:
                    data = json.load(f) 
                    for user in data:
                            if user["login"] in users_unsorted.keys():
                                    users_unsorted[user["login"]] += 1
                            else:
                                    users_unsorted[user["login"]] = 1
                    users_sorted = sorted(users_unsorted.items(), key=lambda kv: kv[1])
                    max=int(len(users_sorted)*1)
                    min=int(len(users_sorted)*0)
                    while min < max:
                            fob=open("names_list.txt","a")
                            fob.write(users_sorted[min][0]+"\n")
                            min += 1
                            fob.close()
        except:
            pass


def unique(filename):
    fob = open(filename, "r")
    names = fob.read()
    fob.close()
    fob = open(filename, "w")
    names = names.split('\n')
    unique_names = []
    for i in names:
        if i not in unique_names:
            unique_names.append(i)
            fob.write(i+"\n")


if __name__ == "__main__":
    get_names("meta_data/repos_list.txt")
    unique("names_list.txt")
