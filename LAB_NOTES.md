# Lab Notes

> [!NOTE]
> For this lab, I used a RasberryPi with a Linux Enviornment. However, a personal RaspberryPi is not necessary as users can utilize a laptop, virtual machine, or cloud server so long as it's environment is linux-based.

## RaspberryPi Setup

User's may set up their enviornments in any way they prefer. Here are the quick step guides to my specific steps. For more information and detailed guides, refer to the official [RaspberryPi Documentation](https://www.raspberrypi.com/documentation/computers/getting-started.html#install).

1. __Flash the Pi__: Dowload and use the [RasberryPi Imager](https://www.raspberrypi.com/software/operating-systems/) to flash the operating system onto the microSD card.

    - *Tip*: Configuring SSH and user credentials beforehand directly inside the Imager settings for headless access.

2. __Setup Firewall__: Firewall configurations are needed in order to *SSH* into the RasberryPI. This step is only needed if you have *headless mode*. Must first attach a keyboard and monitor to the system, then start-up the Pi. After configuring the *uncomplicated firewall*, users may execute the next steps to utilize the `ssh` command.

    - *Firewall Cmd*: Must execute the commands in the following order. Then check the status message to make sure *SSH* is enabled.

    - *SSH Cmd*: Required to have a systems connected to the same internet service. Run the `hostname` command on the Pi terminal to get IP Address, then run `ssh` command on personal system.

    - *Passwords*: When entering a password, be aware that the terminal never displays key strokes.

    ```bash
    # Firewall
    sudo ufw allow ssh
    sudo ufw enable
    sudo ufw status

    # IP Address
    hostname -I

    # SSH
    ssh <user>@<IP Address>
    ```

3. __System Updates__: After connecting to the RasberryPi by directly connecting it to a monitor (if needed), or by SSH. Run the follwoing commands to update system.

    ```bash
    # Update System
    sudo apt update && sudo apt upgrade -y
    ```

4. __Clone Repository__: Find appropriate directory to install the project repository onto the Rasberry Pi and to sync with local development machine.

    - *Tip*: To navigate the file system in the pi, users can use the following commands: `cd <Directory/>`, `cd ..`

    ```bash
    git clone <HTTPS>
    ```
