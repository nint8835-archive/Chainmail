#Install pipenv, create project virtualenv, and install all dependencies
python3 -m pip install pipenv
pipenv install

#Install RCON plugin to allow console access
mkdir plugins
git clone https://github.com/Chainmail-Project/ChainmailRCON.git plugins/ChainmailRCON

#Download server jar file
mkdir server
wget https://s3.amazonaws.com/Minecraft.Download/versions/1.11.2/minecraft_server.1.11.2.jar -O server/minecraft_server.jar

echo "Setup complete! Run start.sh to start the server."
