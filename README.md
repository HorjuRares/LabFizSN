# MyProject

This project is set up to run inside a Linux environment. Follow the instructions below to set up **WSL** (Windows Subsystem for Linux) and **Docker** inside WSL for development and testing purposes.

## Requirements

- A machine running **Windows 10/11**.
- **WSL 2** installed on your Windows machine.
- **Docker** installed inside WSL.

---

## Table of Contents

- [Install WSL](#install-wsl)
- [Install Docker in WSL](#install-docker-in-wsl)
- [Setting up Docker Permissions](#setting-up-docker-permissions)
- [Testing Docker](#testing-docker)
- [Conclusion](#conclusion)

---

## Install WSL

To install **Windows Subsystem for Linux (WSL)**, follow the steps below:

1. Open **PowerShell** as Administrator.
2. Run the following command to enable WSL and set the default version to WSL 2:
   ```powershell
   wsl --set-default-version 2
   wsl --install
   ```

3. Restart your computer if prompted.

4. Install a Linux distribution of your choice (e.g., Ubuntu) from the **Microsoft Store**.

Once installed, open your distribution from the Start menu and complete the initial setup.

---

## Install Docker in WSL

Now that WSL is installed, you can install Docker inside your WSL environment.

1. First, update your package list:
   ```bash
   sudo apt-get update
   ```

2. Install the necessary dependencies for Docker:
   ```bash
   sudo apt-get install \
   ca-certificates \
   curl \
   gnupg \
   lsb-release
   ```

3. Add Docker’s official GPG key:
   ```bash
   sudo mkdir -p /etc/apt/keyrings
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
   ```

4. Set up the stable repository:
   ```bash
   echo \
   "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   ```

5. Install Docker Engine, CLI, and containerd:
   ```bash
   sudo apt-get update
   sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
   ```

---

## Setting up Docker Permissions

To avoid needing to use `sudo` every time you run Docker commands, follow these steps:

1. Create the **docker** group:
   ```bash
   sudo groupadd docker
   ```

2. Add your user to the **docker** group:
   ```bash
   sudo usermod -aG docker $USER
   ```

3. Apply the new group membership without needing to log out and log back in:
   ```bash
   newgrp docker
   ```

4. Start the Docker service (or restart your WSL instance):
   ```bash
   sudo service docker start
   ```

5. Verify that Docker can be run without `sudo`:
   ```bash
   docker run hello-world
   ```

   If the installation is successful, you should see a message indicating that Docker is running properly.

---

## Testing Docker

Run the following command to verify Docker is installed and working correctly:
```bash
docker --version
```

You should see the Docker version printed on the terminal.

To run a test container, use the following command:
```bash
docker run hello-world
```

---

## Conclusion

You have successfully installed **WSL**, **Docker**, and configured the proper permissions to use Docker without `sudo`. You're now ready to run your containers inside WSL!

For further instructions and configuration, check the official Docker and WSL documentation:

- [WSL Documentation](https://docs.microsoft.com/en-us/windows/wsl/)
- [Docker Documentation](https://docs.docker.com/engine/install/ubuntu/)
