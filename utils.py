import os
import subprocess
from subprocess import CalledProcessError
from functools import partial

# all projects using condaci
PROJECTS = [
            'menpofit',
            'menpodetect',
            'menpobench',
            'conda-boost',
            'conda-cherrypy',
            'conda-dlib',
            'conda-eigen',
            'conda-enum',
            'conda-ffmpeg',
            'conda-flann',
            'conda-freeimage',
            'conda-imageio',
            'conda-joblib',
            'conda-mayavi',
            'conda-menpo-pyvrml97',
            'conda-opencv',
            'conda-opencv3',
            'conda-pathlib',
            'conda-vlfeat',
            'conda-vtk',
            'cyassimp',
            'cyffld2',
            'cypico',
            'cyrasterize',
            'cyvlfeat',
            'landmarkerio-server',
            'menpo',
            'menpo3d',
            'vrml97']


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
    for project in PROJECTS:
        os.chdir(working_dir)
        try:
            clone_repo(project)
        except CalledProcessError:
            pass


def apply_to_all_projects(working_dir, f, clone=True):
    if clone:
        clone_all_repos(working_dir)
    for project in PROJECTS:
        repo_dir = os.path.join(working_dir, project)
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
