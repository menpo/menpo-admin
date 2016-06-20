menpo-admin
===========
A collection of scripts and manuals required to successfully manage all menpo projects managed by our in-house `condaci` Continuous Integration (CI) build system.

Overview
--------
We currently use two systems for CI:

1. [Travis CI](https://travis-ci.org/menpo/) (Hosted, Linux). Configuration based on `.travis.yml` in the root of each project. Private keys stored using the Travis API.
2. [Jenkins](jenkins.menpo.org) (On premise, macOS & Windows). Configuration stored in per-project XML records, editable through the Jenkins interface. However, we **never manually edit project settings in this way**. Instead, we maintain a set of template projects, and use the Jenkins API to programmatically update all projects at once. Private keys stored in Jenkins centralized vault for all projects.

Our unified build system for all CI operations is [condaci](https://github.com/menpo/condaci). Broadly speaking, our CI approach is this:

1. Set up the right build matrix (Python 2.7/3.4/3.5, 32bit/64bit) on a given platform CI system.
2. Ensure the CI has access to the required credentials to upload builds (for now, our [anaconda.org](https://anaconda.org/menpo/dashboard) API key).
3. Acquire a particular version of the condaci scipt.
4. Run the condaci script, which will take care of the rest.


Adding a new repository
-----------------------

1. Create the repo using the github website. In general, prefer a 3-clause BSD licence.
2. Ask an owner (@jabooth or @patricksnape) to add our [CI bot team as admins on the new repo](https://github.com/orgs/menpo/teams/bots/repositories). This is needed for Jenkins to be able to function.
3. Copy the current [menpofit/.travis.yml](https://github.com/menpo/menpofit/blob/master/.travis.yml) and augment it to suit the new repo. (We use this as a template as menpo itself has some extra fluff in there that doesn't apply generally).
4. Go to the [Travis CI](https://travis-ci.org/profile/menpo) interface and enable the new project.
5. Visit the settings page for the newly enabled travis CI project. Add a new secure environment variable. The key is `BINSTAR_KEY`. The value can be found by visiting the [anaconda.org admin UI](https://anaconda.org/menpo/settings/access), for menpo. Copy and paste the current access token as the value, and clear your clipboard immediately.
6. Add the new project to this repo and re-run the notebook to create a new Jenkins settings page for the new project.


Tasks that need automating
--------------------------

With this framework in mind, there are some admin jobs that we need to perform from time to time that are a pain to do manually:

1. **Updating our API key for anaconda.org**. Every now and then this expires for security reasons - we then need to update the key across all projects and both CI platforms.
2. **Bumping the version of condaci**. Every now and then, underlying changes in the ecosystem mean that we need to update `condaci` with breaking changes (i.e., the way condaci is invoked is altered). Requires a change to the build scripts across all projects and all platforms.
3. **Altering the build matrix for one project**. If we add support for a new version of Python (or drop support for one) that means updating both CI systems to reflect the change.
4. **Creating a new project that will be managed by condaci**. Entails making new build configurations for both Jenkins and Travis.

This repository contains scripts, notebooks, and guides for all of the above jobs. It also contains the master configuration information - a list of all Menpo projects that use condaci, along with configuration parameters such as what Python version builds are required.


### Creating/bumping our anaconda.org token

#### 1. Create the new token from anaconda:

See [here](https://anaconda.org/organization/menpo/settings/access).
Note that we need to tell anaconda that the token belongs to the organisation, e.g.:
```
TOKEN=$(anaconda auth --create --name condaci -o menpo)
```

#### 2. Install [travis CLI](https://github.com/travis-ci/travis.rb)

And login: `travis login --auto` should work if you are logged in with GitHub.

#### 3. Bump key for Jenkins

Login to the Jenkins interface, as an admin, and go to the vault settings. You should be able to update the key to the new one.

#### 4. Bump key for Travis CI

Use [bump_anaconda_key.ipynb](https://github.com/menpo/menpo-admin/blob/master/bump_anaconda_key.ipynb) to automatically go through all projects and update the key for Travis CI.

### Bumping the version for condaci

#### 1. Bump condaci version for Jenkins

ssh into Jenkins, and download the latest file:
```
wget https://github.com/menpo/condaci/blob/v0.N.x/condaci.py
```
where `N` is the latest version branch.

Ensure it is stored at `~/condaci.py` as this is where all projects will look for loading condaci. Check with @patricksnape as to how to update the Windows build box.

#### 2. Bump condaci version for Travis CI

Use [bump_condai.ipynb](https://github.com/menpo/menpo-admin/blob/master/bump_master.ipynb) to automatically go through all projects and update the version for condaci.


curl -iL -e https://jenkins.menpo.org/jenkins/manage \
   https://jenkins.menpo.org/jenkins/administrativeMonitor/hudson.diagnosis.ReverseProxySetupMonitor/test
