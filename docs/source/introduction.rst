Getting Started
===============

.. highlight:: sh

Overview
--------

Biosimulation Model Search Engine (BMSE) is a web-based search engine for 
finding information in biosimulation models created using CellML and stored in 
the `Physiome Repository Model (PMR) <https://models.physiomeproject.org>`_. 
Types of information include variables, mathematical equations, constants, 
components, models, images, and simulation results. This work uses Composite 
Annotation Search Using BERT (CASBERT) to represent queries and entities in 
biosimulation models :cite:p:`munarko_casbert_2022`.

Deployed Search Engine
----------------------

BMSE: `http://search.bm-se.cloud.edu.au/ <http://search.bm-se.cloud.edu.au/>`_

Documentation
-------------

*  https://bmse.readthedocs.io/en/latest/.

Requirements
------------

* `CASBERT: Composite Annotation Search using BERT <https://github.com/napakalas/casbert>`_
* `Sanic <https://sanic.dev/en/>`_
* `Nginx <https://www.nginx.com/>`_
* `Vue 2 <https://vuejs.org/>`_

Local installation using Docker
-------------------------------
  * Make sure Docker is installed
  * git clone the project
  
    .. code-block:: sh
    
      git clone https://github.com/napakalas/bmse.git
    
  * change current directory to bmse
  
    .. code-block:: sh
    
      cd bmse
    
  * build/start BMSE
  
    .. code-block:: sh
    
      make start
    
  * Now you can access bmse via web browser with
    
      `http://localhost/ <http://localhost/>`_
    
  * Check the Makefile for commands such as stop services, view container logs, etc.

How to deploy?
--------------
  
  We deploy BMSE on a cloud service by 
  `NECTAR <https://dashboard.rc.nectar.org.au/>`_. 
  Services run on an Ubuntu 18.04 LTS (Bionic) amd64 instance with 4 VCPUs and 
  8GB RAM. We utilise 'docker context' for deployment, which provides 
  flexibility in selecting deployment targets. Here are the steps:
  
  * install Docker on the target deployment instant (please adjust it for 
      other than Ubuntu 18.04 LTS (Bionic)):
  
      * Connect to the target deployment instant:
      
        .. code-block:: sh
        
          ssh ubuntu@TARGET-PUBLIC-IP
        
      * Install docker, follow [the installation instructions]
              (https://docs.docker.com/engine/install/ubuntu/) on Ubuntu.
              
      * Change docker.sock access permission
      
        .. code-block:: sh
        
          sudo chmod 666 /var/run/docker.sock
        
      * Logout from the target deployment instant:
      
        .. code-block:: sh
        
          logout
        
  * build/start BMSE on the remote server
   
    .. code-block:: sh
    
      make start-remote ip=TARGET-PUBLIC-IP
    
  * now you can access BMSE via web browser with your instance public IP
    
    .. code-block:: sh
    
      http://TARGET-PUBLIC-IP/
  
  * if you want to implement SSL on the remote server, follow this link:
      https://mindsers.blog/post/https-using-nginx-certbot-docker/    
    
Related repositories
--------------------
CASBERT: https://github.com/napakalas/casbert.git

CASBERT experiment: https://github.com/napakalas/casbert-experiment.git

CASBERT index development: https://github.com/napakalas/casbert-indexer.git