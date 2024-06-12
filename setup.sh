# install java
sudo amazon-linux-extras enable corretto8
sudo yum install java-21-openjdk-devel -y

# install wget
sudo yum install wget -y

# download server pack, unzip and remove zip
wget https://mediafilez.forgecdn.net/files/5128/918/IER%20Serverpack%204.3.1.zip
unzip "IER Serverpack 4.3.1.zip"
rm "IER Serverpack 4.3.1.zip"
