# menpo-admin
Collection of scripts useful for batch updating all menpo projects

#### Creating a new anaconda token

See (here)[https://anaconda.org/organization/menpo/settings/access].
Note that we need to tell anaconda that the token belongs to the organisation, e.g.:
```
TOKEN=$(anaconda auth --create --name condaci -o menpo)
```
