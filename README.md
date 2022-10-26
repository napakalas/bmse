# Biosimulation Model Search Engine (BMSE)
BMSE is a web-based search engine for finding information in biosimulation models created using CellML and stored in the [Physiome Repository Model (PMR)](https://models.physiomeproject.org). Types of information include variables, mathematical equations, constants, components, models, images, and simulation results.

BMSE is a web-based search engine for finding information in biosimulation models created using CellML and stored in the [Physiome Repository Model (PMR)](https://models.physiomeproject.org). Types of information include variables, mathematical equations, constants, components, models, images, and simulation results.

BMSE is built using the following technologies:
- [Composite Annotation Search using BERT (CASBERT)](https://github.com/napakalas/casbert)
- [Sanic](https://sanic.dev/en/)
- [Nginx](https://www.nginx.com/)
- [Vue 2](https://vuejs.org/)

## How to run?
  - git clone the project
    ```
    git clone https://github.com/napakalas/bmse.git
    ```
  - change current directory to bmse
    ```
    cd bmse
    ```
  - build/start BMSE
    ```
    make start
    ```
  - Now you can access bmse via web browser with
    [http://localhost/](http://localhost/)
    
:bulb: Check the Makefile file for commands such as stop services, view container logs, etc.

## How to deploy?
We deploy BMSE on a cloud service by [NECTAR](https://dashboard.rc.nectar.org.au/). Services run on an Ubuntu 18.04 LTS (Bionic) amd64 instance with 4 VCPUs and 8GB RAM. We utilise 'docker context' for deployment, which provides flexibility in selecting deployment targets. Here are the steps:
- Install Docker on the target deployment instant (please adjust it for other than Ubuntu 18.04 LTS (Bionic)):
    - Connect to the target deployment instant:
      ```
      ssh ubuntu@TARGET-PUBLIC-IP
      ```
    - Install docker, follow [the installation instructions](https://docs.docker.com/engine/install/ubuntu/) on Ubuntu.
    - Change docker.sock access permission
      ```
      sudo chmod 666 /var/run/docker.sock
      ```
    - Logout from the target deployment instant:
      ```
      logout
      ```
- Create docker context (in this case the contex is named to remote_bmse)
  ```
  docker context create --docker host=ssh://ubuntu@TARGET-PUBLIC-IP remote_bmse
  ```
- Use remote_bmse
  ```
  docker context use remote_bmse
  ```
- Build the containers in the target deployment instant:
  ```
  docker compose --context remote_bmse build
  ```
- Run the containers in the VM:
  ```
  docker compose --context remote_bmse up -d
  ```
- Now you can access bmse via web browser with your instance public IP
  http://TARGET-PUBLIC-IP/
