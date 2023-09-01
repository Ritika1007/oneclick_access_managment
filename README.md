# OneClick Access Management

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
>
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white) ![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white) ![Jenkins](https://img.shields.io/badge/jenkins-%232C5263.svg?style=for-the-badge&logo=jenkins&logoColor=white) ![HTML](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white) ![CSS](https://img.shields.io/badge/-CSS-1572B6?style=for-the-badge&logo=css3&logoColor=white) ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E) ![Jira](https://img.shields.io/badge/jira-%230A0FFF.svg?style=for-the-badge&logo=jira&logoColor=white)

> Simplify access management with ease.

[Flow Diagram](#OneClick-Flow) | [Features](#features) | [Technologies Used](#technologies-used) | [Installation](#installation) | [Screenshots](#Project-Screenshots)


>
## OneClick-Flow
![oneclick](https://github.com/Ritika1007/oneclick_access_managment/assets/72782573/a98c3f30-4c93-4c7b-9642-581009cc1ac0)


## Features

🚀 Easy and intuitive user interface for managing access permissions.

🔒 LDAP integration for secure authentication.

⚡ Background task processing using Celery(Celery Backend: Redis for efficient access provisioning.

🔐 Access to EC2 servers, Vault databags, Vault databases, and Jenkins jobs.

🔗 Jira integration for seamless collaboration and issue tracking.

📬 Approval workflow with email notifications to managers and users.

## Technologies Used

⚙️ Django - Web framework for rapid development.

🌐 HTML, CSS, JavaScript - Frontend technologies for an interactive user interface.

🔑 LDAP - Integration for secure authentication.

🌱 Celery - Distributed task queue for background task processing.

🔧 Jenkins - Automation server for continuous integration and deployment.

🐘 PostgreSQL - Robust and scalable relational database.

🔧 Ansible - Configuration management and deployment automation tool.

🔧 Redis - In-memory data structure store used as a Celery backend for efficient task processing.

🔗 Jira - Issue tracking and project management tool for seamless collaboration.

## Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/Ritika1007/oneclick_access_managment.git
   cd oneclick_access_managment
   pip install -r requirements.txt
   
2. Configure the LDAP settings in the settings.py file. Also, configure email backend, postgres creds and databse name, and redis.

3. For maintaining secrets create a .env file in your project root directory where your settings.py file is located.

4. Run database migrations:
   ```shell
   python manage.py migrate

5. Start the Django development server:
   ```shell
   python manage.py runserver

6. Open your web browser and navigate to http://localhost:8000.



## Project-Screenshots
> 
> Login using Ldap
![image](https://github.com/Ritika1007/oneclick_access_managment/assets/72782573/514cb3ed-3ee3-406e-8367-ffebe7428455)
>
> ![image](https://github.com/Ritika1007/oneclick_access_managment/assets/72782573/6fe8523e-e253-4c1b-9bb2-3bf681b8d292)

> Home page
> 
![image](https://github.com/Ritika1007/oneclick_access_managment/assets/72782573/0cabeae2-3724-4df2-9b58-dee47da77f38)
> Mail to manager for access request
> 
![image](https://github.com/Ritika1007/oneclick_access_managment/assets/72782573/2e29b4b1-9cda-469e-9128-e2d2510699a1)
>Mail to Requester including details
>
![image](https://github.com/Ritika1007/oneclick_access_managment/assets/72782573/463bdd39-6798-42fd-822c-c39eec552138)
>
>Logout Screen
>![image](https://github.com/Ritika1007/oneclick_access_managment/assets/72782573/32fdf235-f5d0-4620-983a-f12d2e105141)


