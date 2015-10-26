# menpo-admin
Collection of scripts useful for batch updating all menpo projects

### Creating a new anaconda token

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

And login: `travis login --auto`

#### 4. Bump keys across all projects

Use [bump_anaconda_key.ipynb](https://github.com/menpo/menpo-admin/blob/master/bump_anaconda_key.ipynb) to automatically go through all projects and update the key for app veyor and travis.
