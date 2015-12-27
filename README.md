#Webraid
A simple website for a small community. 

#Requirements

## Python
All python requirements are in the ```.travis.yml``` file a the root of the project :

```
language: python
sudo: false
python:
  - "2.7"

env:
  - DJANGO=1.8

install:
  pip install django-countries beautifulsoup

```
## We use less ! 

You need to install [less]( http://lesscss.org/) and [clean-css plugin](https://github.com/less/less-plugin-clean-css).
### Node.js and npm
Install ```node.js``` : get it [here](https://nodejs.org/en/).
Test: Run ```node -v```. The version should be higher than v0.10.32.
Then update npm by ```sudo npm install npm -g``` 
Test: Run ```npm -v```. The version should be higher than 1.4.28.

### Less and clean-css
Then ```less```:
```npm install -g less```
And finally ```clean-css```:
```npm install -g clean-css```
You might need to be a superuser to run the previous two commands.

Don't forget to make the ```compile_less.sh``` script executable :
```sudo chmod +x ./compile_less.sh```
And to compile the less files when making changes !
``` ./compile-less.sh ```