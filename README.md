# Double Shamrock   

Double Shamrock is a social website of St Patrick's Day jokes and videos. The users can create, read, edit and delete jokes on website. The site is designed to be easy to navigate and use, promoting a simple layout with minimal but effective and purposeful features.

Project Requirements:

Build an interactive front-end website that responds to user actions and alters the way the site displays data/information.

Required Technologies : HTML, CSS, JavaScript, Python+Flask, MongoDB. A live version of the site is available here.
---

## Table of Contents
1. [UX](#ux)
    - [User Stories](#user-stories)
    - [Design](#design)
    - [Wireframes](#wireframes)

2. [Features](#features)
    - [Existing Features](#existing-features)
    - [Features Left to Implement](#features-left-to-implement)

3. [**Information Architecture**](#information-architecture)
    - [**Database Choice**](#database-choice)
    - [**Data Modelling**](#data-modelling)

4. [Technologies Used](#technologies-used)
    - [**Languages**](#languages)
    - [**Libraries and Frameworks**](#libraries-and-frameworks)
    - [**Tools**](#tools)
    - [**Databases**](#databases)

5. [Testing](#testing)
    - [Manual Testing](#manual-testing)
    - [Validators](#validators)
    - [Compatibility and Responsiveness](#compatibility-and-responsiveness)

6. [Deployment](#deployment)
    - [Local Deployment](#local-deployment)
    - [Heroku Deployment](#heroku-deployment)

7. [Credits](#credits)
    - [Content](#content)
    - [Media](#media)
    - [Code](#code)
    - [Acknowledgements](#acknowledgements)

8. [**Disclaimer**](#disclaimer)

---

## UX

### User Stories
#### Common user stories (guests, new users and authenticated users)
- As a user, I expect to access the website from any device, so that I can use the website anytime and anywhere.
- As a user, I expect to easily navigate the website, so that I can quickly find what I'm looking for.
- As a user, I want to easily access social media links of the company, so that I can read more information about it.
- As a user, I want to read a summary info about the app and its features and functionality, so that I can quickly decide if it satisfies my needs.
- As a user, I want to view all the joke and videos without having to register.
#### New Users
- As a user, I want to create my own account, so that I can save, view and edit my profile details and access it any time.
#### Returning users
- As a user, I want to easily login anytime, so that I can get access to my uploaded videos and jokes.
- As a user, I want to  be able to change my password, so that I can create the stronger password (e.g.in case I published my old password somewhere) to protect my personal details.    
- As a user, I want to  be able to change my email and username, so that I can have an easier access to the website's functionality and to gain more flexibility.
- As a user, I want to add new jokes/upload new videos.
- As a user, I want to edit my jokes/videos.
- As a user, I want to delete my jokes/videos.
- As a user, I want to view a list of my jokes and videos.
- As a user, I want to delete my account and all the jokes and videos I've created.
### Design
#### Framework

#### Colour Scheme

#### Typography

#### Icons

#### Further styling decisions


### Wireframes

<div align="right">
    <b><a href="#table-of-contents">↥ Back To Top</a></b>
</div>

---

## Features
### Existing Features

### Features Left to Implement

<div align="right">
    <b><a href="#table-of-contents">↥ Back To Top</a></b>
</div>

---

## Technologies Used
### Languages
- [HTML](https://developer.mozilla.org/en-US/docs/Web/HTML)
- [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS) 
- [JavaScript](https://www.javascript.com/)
- [Python](https://www.python.org/) 
- [Jinja](https://jinja.palletsprojects.com/en/2.10.x/) - templating language for Python, to display back-end data in HTML.

### Libraries and Frameworks
- [Flask](https://flask.palletsprojects.com/en/1.1.x/) - Python framework for building the project.
- [Bootstrap](https://www.bootstrapcdn.com/) - as the front-end framework for layout and design.
- [Google Fonts](https://fonts.google.com/) - to import fonts.
- [FontAwesome](https://fontawesome.com/) - to provide icons used across the project. 
- [JQuery](https://jquery.com/) - to simplify DOM manipulation and to initialize Bootstrap functions.

### Tools
- [GitPod](https://www.gitpod.io/) and [VS Code ](https://code.visualstudio.com/)- IDEs for developing this project.
- [Git](https://git-scm.com/) - for version control.
- [GitHub](https://git-scm.com/) - for remotely storing project's code.
- [PIP](https://pip.pypa.io/en/stable/installing/) - for installation of necessary tools.
- [Heroku](https://heroku.com/) - to host the project.
- [PyMongo](https://pypi.org/project/pymongo/) - a Python distribution containing tools for working with MongoDB.
- [Balsamiq](https://balsamiq.com/) - to create wireframes.

### Databases
- [MongoDB](https://www.mongodb.com/) - NoSQL database for storing back-end data.


<div align="right">
    <b><a href="#table-of-contents">↥ Back To Top</a></b>
</div>

---

## Testing
### Manual Testing 

#### Known bugs

### Validators
#### Html

#### CSS

#### JavaScript

#### Python

### Compatibility and Responsiveness


<div align="right">
    <b><a href="#table-of-contents">↥ Back To Top</a></b>
</div>

---

## Deployment
### Local Deployment

The site was developed in GitPod and pushed to the following remote GitHub repository - here
The following GIT commands were used throughout deployment:
git status ------ used to check the status of files and any changes made / untracked.
git add -A ------ to stage files ready to commit.
git commit -m " " ------ to commit the files.
git push ------ to push the files to the master branch of the GitHub repo.

### Heroku Deployment
This site is hosted using Heroku, deployed directly from the master branch via GitHub. - LIVE SITE

The following steps were taken to complete the hosting process.
Set debug=False in the app.py file.
Created a requirements.txt file from the terminal, using pip3 freeze --local > requirements.txt, to allow Heroku to detect this project as a python app and any required package dependencies.
Created a Procfile using echo web: python app.py > Procfile from the Gitpod terminal so Heroku would be informed on which file runs the app and how to run this project.
Created a new Heroku app, my-recipe-m3 and set its region to Europe.
Automatic deployment was set up on Heroku - On the app dashboard, in the deploy menu. Connect to GitHub section. The GitHub repository was searched for and connected to the app.
In the settings tab on the app dashboard, 'Reveal Config Vars' was used to tell Heroku which variableS are required to run the app. The following config vars were added:
IP
PORT
SECRET_KEY
MONGO_URI
In GitPod, a check was completed to ensure the master branch was up to date and all commits had been pushed to GitHub, ready for Heroku to deploy.
Clicked the Enable Automatic Deploys button located in the Deploy section of Heroku to allow for automatic deploys.
Clicked the Deploy Branch button located in the Deploy section of Heroku to finally deploy this project.
Clicked the View button to launch this project's app.
The deployed site on Heroku will update automatically upon new commits to the master branch in the GitHub Repo : REPO
Cloning

To run this code locally, you can clone this repository directly into the editor of your choice by following the steps below:

Open Terminal.
Change the current working directory to the location when you want the cloned directory.
Type the following into your Terminal:
git clone insert link
Press Enter to create a local clone.
To cut ties with this GitHub repository, type git remote rm origin into the terminal.
For more information regarding cloning of a repository click here.

---

## Credits

### Content

### Code

### Acknowledgements

 
<div align="right">
    <b><a href="#table-of-contents">↥ Back To Top</a></b>
</div>

---

## Disclaimer
This website is made for **educational purposes** only as part of the Code Institute March Hackathon 2021.        


<div align="right">
    <b><a href="#table-of-contents">↥ Back To Top</a></b>
</div>
