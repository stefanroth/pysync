import os


class ProjectList:
    def __init__(self, projects):
        self.projects = []
        self.read(projects)

    def read(self, projects):
        for p in projects:
            for pn, pconfig in p.items():
                self.projects.append(ProjectConfig(pn, pconfig))

    def find_by_name(self, name):
        for p in self.projects:
            if p.name == name:
                return p


class ProjectConfig:
    def __init__(self, name, project):
        self.name = name
        self.From = ""
        self.To = ""
        self.Command = "rsync -a %(From) %(To)"
        self.read(project)

    def read(self, project):
        for entry in project:
            for k, v in entry.items():
                if k == "From":
                    self.From = v
                if k == "To":
                    self.To = v
                if k == "Command":
                    self.Command = v

        self.interpolate_command()

        return self

    def interpolate_command(self):
        self.Command = str.replace(self.Command, "%(From)", self.From)
        self.Command = str.replace(self.Command, "%(To)", self.To)
        return self

    def validate(self):
        result = True
        if not os.path.isdir(self.From):
            result = False
            print self.name, "From-path not found:", self.From
        if not os.path.isdir(self.To):
            result = False
            print self.name, "To-path not found:", self.To
        return result
