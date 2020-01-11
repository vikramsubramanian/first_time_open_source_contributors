"""This script takes a .txt file with list of GitHub users as input.
For each user given as input->
1.Get a list of repos all the repos this user is a part of.
2.Get the first forked repo amongst that list
3.Check if that repo has a commit -> first pull request
    If not, get next forked repo and repeat.
"""

import json
import os
import argparse
import subprocess
from helper import *
from operator import itemgetter

exceeded = 0

def get_date(iterable):
    return iterable["commit"]["author"]["date"]
def get_date_pull(iterable):
    return iterable["created_at"]


def get_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("--names", help="Provide path to a .txt with \
                            a list of github users")
    parser.add_argument(
        "--auth", help="Provide authentication token for Github")
    args = parser.parse_args()
    return args


def get_repos(name):
    try:
        """Get a list of all the repos of a user, save it in a file and
        and pass it to get_first_repo() """

        command = run_command(["users", name, "repos"], [], authentication)
        exceeded = pagination(command, 0, ("meta_data/"+name + ".json"))

        lines = []
        filen = open("meta_data/"+name + ".json")
        try:
            json_obj = json.load(filen)
            lines.append(json_obj)
            lines = sorted(json_obj, key=itemgetter('created_at'))

            fob = open("meta_data/"+name + ".json", "w")
            json.dump(lines, fob)
            fob.close()
        except:
            print("no repos for this user!")
    except:
        pass


def get_first_commit(filename, owner_name):

    fob = open("meta_data/first_commit.json", "w")
    fob.close()
    
    parent=""    
    commits=[]
    comit_s=""
    commit_file = ("data/commit_"+owner_name+".json")
    pull_file = ("data/pull_"+owner_name+".json")
    
    f = open(filename, "r")
    text = f.read(4)

    if text != "[\n\n]" and text:

        fob = open("meta_data/iter4.json", "w")
        fob.close()

        f = open(filename, "r")
        repo_list = json.load(f)
        owner_name = owner_name.strip("\n").strip()

        for i in range(len(repo_list)):

            if repo_list[i]["fork"] == True:

                command = run_command(["repos", str(owner_name), repo_list[i]["name"], "commits"], [
                                    str("author=" + owner_name)], authentication)
                exceeded = pagination(command, 1, "meta_data/inter3.json")

                print(repo_list[i]["name"])

                f = open("meta_data/inter3.json", "r")
                text = f.read(4)
                f.close()

                if text != "[\n\n]" and text:

                    command = run_command(
                        ["repos", str(owner_name), repo_list[i]["name"]], [], authentication)
                    command += "\" > meta_data/inter2.json"
                    print(command)
                    subprocess.run(command, shell=True)

                    fob = open("meta_data/inter2.json")
                    commit = json.load(fob)
                    parent = commit["parent"]["full_name"]

                    command = run_command(["repos", parent, "commits"], [
                        str("author=" + owner_name)], authentication)
                    exceeded = pagination(
                        command, 1, "meta_data/inter3.json")

                    f = open("meta_data/inter3.json", "r")
                    text = f.read(4)
                    f.close()
                    
                    if text != "[\n\n]" and text:
                        fob = open("meta_data/inter3.json")
                        commit = json.load(fob)
                        fob.close()
                        
                        command = run_command(
                            ["repos", parent, "commits", str(commit[-1]["sha"])], [], authentication)
                        command = str(command) + \
                            "\" > meta_data/iter4.json"
                        print(command)
                        subprocess.run(command, shell=True)
                        fb=open("meta_data/iter4.json")
                        commit=json.load(fb)
                        commits.append(commit)
        
        if exceeded==0:
            commits.sort(key=get_date)
            if len(commits) > 0:
                for i in range(len(commits)):
                    comit_s=commits[i]["sha"]
                    command = "curl -H \"Accept: application/vnd.github.groot-preview+json\" -H \"Authorization: token f916538bf03120b6272b2329284d618f96308a79\" \"" +commits[i]["url"]+ "/pulls" 
                    command += "\" > " + "meta_data/iter5.json"
                    print(command)
                    subprocess.run(command, shell=True)
                    fob = open("meta_data/iter5.json","r")
                    text = fob.read(4)
                    if text != "[\n\n]" and text and text != "{\n  ": 
                        fob=open(pull_file,"w")
                        fob.close()
                        fb=open(commit_file,"w")
                        json.dump(commits[i],fb)
                        command = "curl -H \"Accept: application/vnd.github.groot-preview+json\" -H \"Authorization: token f916538bf03120b6272b2329284d618f96308a79\" \"" +commits[i]["url"]+ "/pulls" 
                        command += "\" > " + pull_file
                        print(command)
                        subprocess.run(command, shell=True)
                        break


        



def main():
    """Main entry point into the script"""

    fob=open(args.names, "r")
    names=fob.readlines()
    fob.close()
    for name in names:
        try:
            name=name.strip("\n")
            get_repos(name)
            get_first_commit(("meta_data/"+name+".json"), name)
            print("put this block in a try block for ideal performance")
        except:
            pass


if __name__ == "__main__":
    args=get_args()
    authentication=args.auth
    main()
