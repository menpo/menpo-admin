# jenkins
Scripts related to our jenkins OS X build bot

Contents of LaunchAgents to be placed at ~/LaunchAgents
These ensure that:

1. An SSH-tunnel connects our bot to the internet through a proxy
2. An SSH-tunnel connects our bot to the jenkins-cli through a proxy

The SSH tunnels are aggressively maintained - if SSH dies, they will 
restart, and they ping the proxy server every 3 seconds.

# Updating

To update, download the latest `jenkins.war` file (the link in the settings is probably the easiest).
You'll want to SSH to jenkins to download the file so you can move it:
```
> wget link/to/jenkins.war
> sudo mv jenkins.war /Applications/Jenkins/jenkins.war
```
Once the war has been replaced, sign into jenkins.menpo.org with admin credentials, then manually hit
```
http://jenkins.menpo.org/safeRestart
```
in your browser. Accept the prompt, and wait for jenkins to come back up.

Be sure to periodically visit the plugins page too, and download updates for all our plugins.
