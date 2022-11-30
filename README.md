# MemoMood

![Unittest](https://github.com/MemoMood/MemoMood/actions/workflows/test-python-app.yml/badge.svg)
[![codecov](https://codecov.io/gh/MemoMood/MemoMood/branch/ci/graph/badge.svg?token=VKCG86MQLC)](https://codecov.io/gh/MemoMood/MemoMood)

Web application for everyone who wants to keep track of their mental health by recording the data regularly and discover relevant behavior, event, and environment factors that can influence a user’s mood.

## Project Documents

All project documents are in the [Project Wiki](../../wiki/Home)

- [User stories](https://github.com/MemoMood/MemoMood/wiki/User-stories)
- [Iteration 1 Plan](https://github.com/MemoMood/MemoMood/wiki/Iteration-1-Plan)
- [Iteration 2 Plan](https://github.com/MemoMood/MemoMood/wiki/Iteration-2-Plan) | [Iteration 2 Task Board](https://github.com/orgs/MemoMood/projects/2/views/2)
- [Iteration 3 Plan](https://github.com/MemoMood/MemoMood/wiki/Iteration-3-Plan) | [Iteration 3 Task Board](https://github.com/orgs/MemoMood/projects/2/views/3)
- [Iteration 4 Plan](https://github.com/MemoMood/MemoMood/wiki/Iteration-4-Plan) | [Iteration 4 Task Board](https://github.com/orgs/MemoMood/projects/2/views/5)
- [Iteration 5 Plan](https://github.com/MemoMood/MemoMood/wiki/Iteration-5-Plan) | [Iteration 5 Task Board](https://github.com/orgs/MemoMood/projects/2/views/6)
- [Iteration 6 Plan](https://github.com/MemoMood/MemoMood/wiki/Iteration-6-Plan) | [Iteration 6 Task Board](https://github.com/orgs/MemoMood/projects/2/views/7)
- [Iteration 7 Plan](https://github.com/MemoMood/MemoMood/wiki/Iteration-7-Plan) | [Iteration 7 Task Board](https://github.com/orgs/MemoMood/projects/2/views/8)

## Installation and Run

1. Clone this repository into your local machine by using the command:
    ```sh
    $ git clone https://github.com/MemoMood/MemoMood.git
    ```
2. Open the directory where you cloned the repository:
    ```sh
    $ cd MemoMood
    ```
3. Create a virtual environment:
    ```sh
    $ python -m venv env
    ```
4. then run to activate a virtual environment.
    - For Mac/Linux use this command:
        ```sh
        $ . env/bin/activate  
        ```
    - For Windows use this command:
        ```sh
        $ . env/Scripts/activate
        ```
5. Download the requirements to virtual environment using:
    ```sh
    $ pip install -r requirements.txt
    ```
6. Create a ```.env``` file in the project directory by using ```sample.env``` as example that provided in the project directory. 
To generate a secret key you can go to [djecrety.ir](https://djecrety.ir/) or using:
    ```
    $ python manage.py shell
    >>> from django.core.management.utils import get_random_secret_key
    >>> print(get_random_secret_key())
    ```
    use ```clt+d``` to stop shell.
7. Then, create database by using:
    ```sh
    $ python manage.py migrate
    ```
9. Create superuser by using:
    ```sh
    $ python manage.py createsuperuser
    ```
8. Run the server:
    ```sh
    $ python manage.py runserver
    ```
10. If you want to use Google authentication please follow:
    - Go to ```http://127.0.0.1:8000/admin``` and login with superuser.
    - Follow this [guide](https://www.section.io/engineering-education/django-google-oauth/) to add google to your app.
11. If you want to stop server using ```ctl+d```
12. To exit the environment:
    ```sh
    $ deactivate
    ```
    