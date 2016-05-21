menpo-admin
===========
A collection of scripts and manuals required to successfully manage all menpo projects managed by our in-house `condaci` Continuous Integration (CI) build system.

Overview
--------
We currently use three systems for CI:

1. [Travis CI](https://travis-ci.org/menpo/) (Hosted, Linux). Configuration based on `.travis.yml` in the root of each project. Private keys stored using the Travis API.
2. [AppVeyor](https://ci.appveyor.com/projects) (Hosted, Windows). Configuration based on `appveyor.yml` in the root of each project. Private keys are encoded using the AppVeyor website --- the encoded versions are the stored in plain text in the `appveyor.yml` file.
3. [Jenkins](jenkins.menpo.org) (On premise, OS X). Configuration stored in per-project XML records, editable through the Jenkins interface. However, we **never manually edit project settings in this way**. Instead, we maintain a set of template projects, and use the Jenkins API to programmatically update all projects at once. Private keys stored in Jenkins centralized vault for all projects.

Our unified build system for all CI operations is [condaci](https://github.com/menpo/condaci). Broadly speaking, our CI approach is this:

1. Set up the right build matrix (Python 2.7/3.4/3.5, 32bit/64bit) on a given platform CI system.
2. Ensure the CI has access to the required credentials to upload builds (for now, our [anaconda.org](https://anaconda.org/menpo/dashboard) API key).
3. Acquire a particular version of the condaci scipt.
4. Run the condaci script, which will take care of the rest.

Tasks that need automating
--------------------------

With this framework in mind, there are some admin jobs that we need to perform from time to time that are a pain to do manually:

1. **Updating our API key for anaconda.org**. Every now and then this expires for security reasons - we then need to update the key across all projects across all CI platforms.
2. **Bumping the version of condaci**. Every now and then, underlying changes in the ecosystem mean that we need to update `condaci` with breaking changes (i.e., the way condaci is invoked is altered). Requires a change to the build scripts across all projecs and all platforms.
3. **Altering the build matrix for one project**. If we add support for a new version of Python (or drop support for one) that means updating all three build systems to reflect the change.
4. **Creating a new project that will be managed by condaci**. Entails making new build configurations for all three platforms, and enabling support in the various CI's systems.


This repository contains scripts, notebooks, and guides for all of the above jobs. It also contains the master configuration information - a list of all Menpo projects that use condaci, along with configuration parameters such as what Python builds are required.


### Creating/bumping our anaconda.org token

#### 1. Create the new token from anaconda:

See [here](https://anaconda.org/organization/menpo/settings/access).
Note that we need to tell anaconda that the token belongs to the organisation, e.g.:
```
TOKEN=$(anaconda auth --create --name condaci -o menpo)
```

#### 2. Encryt the token for AppVeyor:
Head here:
https://ci.appveyor.com/tools/encrypt

And paste in the token.

#### 3. Install [travis CLI](https://github.com/travis-ci/travis.rb)

And login: `travis login --auto` should work if you are logged in with GitHub.

#### 4. Bump key for Jenkins

Login to the Jenkins interface, as an admin, and go to the vault settings. You should be able to update the key to the new one.

#### 5. Bump key for AppVeyor/Travis CI

Use [bump_anaconda_key.ipynb](https://github.com/menpo/menpo-admin/blob/master/bump_anaconda_key.ipynb) to automatically go through all projects and update the key for AppVeyor and Travis CI.

### Bumping the version for condaci

#### 1. Bump condaci version for Jenkins

ssh into Jenkins, and download the latest file:
```
wget https://github.com/menpo/condaci/blob/v0.N.x/condaci.py
```
where `N` is the latest version branch.

Ensure it is stored at `~/condaci.py` as this is where all projects will look for loading condaci.

#### 2. Bump condaci version for AppVeyor/Travis CI

Use [bump_condai.ipynb](https://github.com/menpo/menpo-admin/blob/master/bump_master.ipynb) to automatically go through all projects and update the version for condaci.



curl -iL -e https://jenkins.menpo.org/jenkins/manage \
   https://jenkins.menpo.org/jenkins/administrativeMonitor/hudson.diagnosis.ReverseProxySetupMonitor/test
