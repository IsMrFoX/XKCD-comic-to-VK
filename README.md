# XKCD to VK
This is a Python script that downloads a random XKCD comic and posts it to a VK fan group using VK API.

### How to install

Python 3 should already be installed.
Then use `pip` (or `pip3', there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```
------------------------------
### Installation

Clone the repository to your local machine

```
git clone https://github.com/IsMrFoX/XKCD-comic-to-VK.git
```

Create a VK API token with the following permissions: photos, wall, groups.\
Rename .env_sample to .env and set your VK group ID and access token in the .env file

### To get a VK API token with access rights to photos, wall and groups, you need to do the following:

Register on the website vk.com.\
Create a VK community.\
Go to the page [vk.com/dev](vk.com/dev) --> my apps --> create a Standalone application.\
After creating the application, go to the application settings and copy the "Application ID" and "Protected Key".\
Create a file .env in the project folder and add the following lines to it:\
```
VK_ACCESS_TOKEN=<your token>
VK_GROUP_ID=<your group id>
```
where "your token" is your VK API token, and "your group id" is your VK group ID.

### To get a token, follow these steps:

Go to the page [vk.com/dev/access_token](vk.com/dev/access_token ) .
Click on the "Create Token" button.
Select the necessary access rights (photos, wall, groups) and click "Create".
Copy the received token and add it to the .env file.
To get the ID of your VK group, follow these steps:

Open your group's VK page.
Copy the digital ID from the page URL.
For example, if the URL of your group's page looks like this: https://vk.com/public123456789 , then the group ID is 123456789.
Add your group ID to the .env file.

----------------
### Usage
Open a terminal and navigate to the project directory
Run the script using the following command:
```
python main.py
```
The script will download a random XKCD comic, upload it to VK, and post it to your group's wall
The script will output the post ID if the post was successfully published, otherwise it will output an error message

----------------
### Project goal
The code is written for educational purposes on an online course for web developers [dvmn.org](https://dvmn.org/).
