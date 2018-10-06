#!/usr/bin/env python
import os;
import argparse;

parser = argparse.ArgumentParser(description='Install Collinson Docker Registry')
parser.add_argument('--hosts', dest='hosts', nargs='?', const=True, default="local", required=True, help='Host file to select')
#parser.add_argument('--test', dest='test', required=False, help='Show the command to execute but not execute it')
parser.add_argument('--u', dest='user', required=False, help='User to connect to remote machine as')
#parser.add_argument('--s', dest='sudo', required=False, help='Ask for sudo password')
args = parser.parse_args()

# os.system('sudo ansible-galaxy install -r ./playbooks/requirements.txt')

command = "ansible-playbook -i ./playbooks/hosts/%s " % (args.hosts)
if args.user:
    command += "-u %s -k --ask-become-pass " % (args.user)

command += "playbooks/main.yml"
print command

#if args.test != "":
os.system(command)
