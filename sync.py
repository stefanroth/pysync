#!/usr/bin/env python

import yaml
import sys
import time
from subprocess import call
from projectconfig import ProjectList


def main():
    print "Project Synchronisation Script"
    with open("./config/sync.yaml", 'r') as stream:
        try:
            config = yaml.load(stream)
            for k, v in config.items():
                if k == "Projects":
                    pl = ProjectList(v)
        except yaml.YAMLError as exc:
            print(exc)

    if len(sys.argv) < 2:
        print "What project do you want to sync?"
        print "sync <project 1> ... <project n>"
        print "Exiting."
    else:
        all_projects_are_valid = True
        projects_to_sync = []
        for i in range(1, len(sys.argv)):
            project_name = sys.argv[i]
            project = pl.find_by_name(project_name)

            if project is None:
                print "No project named", project_name, "found. Exiting."
                exit(1)

            if project.validate():
                projects_to_sync.append(project)
            else:
                all_projects_are_valid = False

        print "Number of projects to sync", len(projects_to_sync)

        for p in projects_to_sync:
            print p.name
            print "  From:    " + p.From
            print "  To:      " + p.To
            print "  Command: " + p.Command
            print ""

        print "Ctrl-C to exit"

        if len(projects_to_sync) > 0 and all_projects_are_valid:
            loop = 0
            try:
                while True:
                    loop += 1
                    if loop > 1:
                        # http://tldp.org/HOWTO/Bash-Prompt-HOWTO/x361.html
                        # - Move the cursor backward N columns:
                        #     \033[<N>D
                        sys.stdout.write("\033[" + str(len(str(loop))) + "D")
                        sys.stdout.flush()
                    for p in projects_to_sync:
                        time.sleep(0.5)
                        call(p.Command, shell=True)
                        sys.stdout.flush()
                    sys.stdout.write(str(loop))
                    sys.stdout.flush()
            except KeyboardInterrupt:
                sys.stdout.write("\033[2D")
                sys.stdout.flush()
                print "  "
                print "Exiting after " + str(loop) + " loops."
                print "Have a nice day!"
                sys.exit(0)
        print "Exiting."


if __name__ == "__main__":
    main()
