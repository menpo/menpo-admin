import os
import subprocess
from subprocess import CalledProcessError
from functools import partial
from collections import namedtuple

Project = namedtuple('Project', ['name', 'versions'])

# all projects using condaci along with the Python version they
# need. Note that for non-python projects we can choose any single
# python version.
PROJECTS = [Project(*x) for x in
            [('menpo', (2, 34, 35)),
             ('menpodetect', (2, 34, 35)),
             ('menpofit', (2, 34, 35)),
             ('menpo3d', (2, 34, 35)),
             ('menpocli', (2, 34, 35)),
             ('menpowidgets', (2, 34, 35)),
             
             ('landmarkerio-server', (2,)),
             ('menpobench', (2,)),


             ('cyassimp', (2, 34, 35)),
             ('cyrasterize', (2, 34, 35)),
             ('cyvlfeat', (2, 34, 35)),
             ('cyffld2', (2, 34, 35)),
             ('cypico', (2, 34, 35)),
             
             ('conda-boost', (2, 34, 35)),
             ('conda-cherrypy', (2, 34, 35)),
             ('conda-dlib', (2, 34, 35)),
             ('conda-opencv3',  (2, 34, 35)),
             ('conda-ffmpeg', (2, 34, 35)),
             ('conda-freeimage', (2, 34, 35)),
             ('conda-imageio', (2, 34, 35)),
             ('conda-joblib', (2, 34, 35)),
             
             # Python 2 only
             ('conda-menpo-pyvrml97', (2,)),
             ('conda-pathlib', (2,)),
             
             ('conda-vtk', (2, 34, 35)),
             ('conda-traits', (2, 34, 35)),
             ('conda-envisage', (2, 34, 35)),
             ('conda-pyface', (2, 34, 35)),
             ('conda-apptools', (2, 34, 35)),
             ('conda-traitsui', (2, 34, 35)),
             ('conda-mayavi', (2, 34, 35)),
             
             # Non-Python projects
             ('vrml97', (2,)),
             ('conda-flann', (2,)),
             ('conda-eigen', (2,)),
             ('conda-enum',  (2,)),
             ('conda-vlfeat',  (35,)),

             ('conda-opencv',  (35,))
            
            ]]

PROJECT_NAMES = [p.name for p in PROJECTS]


def load_file(fpath):
    with open(fpath, 'rt') as f:
        text = f.read()
    return text


def save_file(fpath, string):
    with open(fpath, 'wt') as f:
        f.write(string)


def repo_url(project_name):
    return 'git@github.com:menpo/{}'.format(project_name)


def clone_repo(project_name):
    repo_url = 'git@github.com:menpo/{}'.format(project_name)
    print('cloning {}'.format(repo_url))
    subprocess.check_output(['git', 'clone', repo_url])


def clone_all_repos(working_dir):
    if not os.path.isdir(working_dir):
        print('creating path at {}'.format(working_dir))
        os.mkdir(working_dir)
    for project in PROJECT_NAMES:
        os.chdir(working_dir)
        try:
            clone_repo(project)
        except CalledProcessError:
            pass


def apply_to_all_projects(working_dir, f, clone=True):
    if clone:
        clone_all_repos(working_dir)
    for project in PROJECT_NAMES:
        repo_dir = os.path.join(working_dir, project)
        print('processing {}...'.format(project))
        f(repo_dir)


def perform_operation_on_file(filename, operation, repo_dir):
    filepath = os.path.join(repo_dir, filename)
    old_text = load_file(filepath)
    new_text = operation(old_text)
    if old_text != new_text:
        save_file(filepath, new_text)
        return True
    else:
        return False


def replace_str(old, new, text):
    return text.replace(old, new)


appveyor_op = partial(perform_operation_on_file, 'appveyor.yml')
travis_op = partial(perform_operation_on_file, '.travis.yml')
