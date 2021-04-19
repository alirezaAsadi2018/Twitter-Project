<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/alirezaAsadi2018/Twitter-Project">
    <img src="images/logo.jpg" alt="Logo" width="180" height="180">
  </a>

  <h3 align="center">Twitter-Project</h3>

  <p align="center">
    This is a clone of twitter app with the capability of making tweets, retweets, liking them and creating profiles. Tweet contents can be text, image or videos(this feature is in video branch for now!) and video content is streamed online from server to the client. You can follow users and get notified when you are followed, or when your posts are liked or retweeted. 
    <br />
    <a href="https://github.com/alirezaAsadi2018/Twitter-Project"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/alirezaAsadi2018/Twitter-Project/issues">Report Bug</a>
    ·
    <a href="https://github.com/alirezaAsadi2018/Twitter-Project/issues">Request Feature</a>
  </p>
</p>

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

Home Page (user has logged in)             |  Home Page (anonymous user)
:-------------------------:|:-------------------------:
[![Twitter-Project Screen Shot 1][Twitter-Project-screenshot1]](images/screenshot1.png)  |  [![Twitter-Project Screen Shot 2][Twitter-Project-screenshot2]](images/screenshot2.png)


### Built With

* [Django](https://www.djangoproject.com/)
* [Django Templates (e.g: Jinja2)](https://docs.djangoproject.com/en/dev/topics/templates/)
* [Fomantic-ui](https://fomantic-ui.com/)
* HTML, Css, Js
* [Jquery](https://jquery.com/)



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

The requirements.txt file should list all Python libraries that your django project depends on and gradle files will contain all dependecies used by android app.

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/alirezaAsadi2018/Twitter-Project.git
   ```
2. Create virtualenv(optional) and install Pip packages
   ```sh
   pip install -r requirements.txt
   ```
3. Run django commands to start your server
   ```sh
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```
4. Open your browser on `localhost:8000` to see the glory :smile:.



<!-- MARKDOWN LINKS & IMAGES -->
[Twitter-Project-screenshot1]: images/screenshot1.png
[Twitter-Project-screenshot2]: images/screenshot2.png
