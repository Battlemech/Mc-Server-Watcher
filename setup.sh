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
python3 -m venv server
source server/bin/activate

# install mcstatus
pip install mcstatus
