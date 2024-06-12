# uninstall java 11
sudo yum remove java-11-amazon-corretto-headless -y

# install java 8
sudo yum install java-8-amazon-corretto-headless -y

# install wget
sudo yum install wget -y

# download server pack, unzip and remove zip
wget https://mediafilez.forgecdn.net/files/5128/918/IER%20Serverpack%204.3.1.zip
unzip "IER Serverpack 4.3.1.zip"
rm "IER Serverpack 4.3.1.zip"

# install pip
sudo yum install python3-pip -y
# update pip
pip3 install --upgrade pip

# create virtual python environment
python3 -m venv venvServer
source venvServer/bin/activate

# install mcstatus
pip install mcstatus

# deactivate virtual python environment
deactivate

# ensure "start.sh" is executable
chmod +x start.sh

# install screen
sudo yum install screen -y

# create service file, using template at ./McServer.service
sudo cp McServer.service /etc/systemd/system/McServer.service

# enable service
sudo systemctl enable McServer

# start service
sudo systemctl start McServer

# check status
sudo systemctl status McServer