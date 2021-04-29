# Nutanix Python API Lab v1.3 - Complete Demo

This Python Flask demo app is designed as a complete working version of the dashboard created in the [Nutanix Python Flask and Prism REST API lab](https://www.nutanix.dev/labs/).

Rather than download this complete app and run it standalone, new users are recommended to follow the lab so that all components and concepts are appropriately communicated.

Those with Python Flask experience are welcome to download this demo and use as they see fit, of course.

## Versions

Bundled with this repo is a version that can be run using `docker-compose`:

- Ensure `git` is installed locally and available in a terminal
- Clone this repo:

  ```
  git clone https://github.com/nutanixdev/python-api-lab-demo
  ```

- [Install docker-compose](https://docs.docker.com/compose/install/) on your system (this process is beyond the scope of this repo)
- Checkout the `compose` branch:

  ```
  git checkout compose
  ```

- Launch the app:

  ```
  docker-compose up -d --build
  ```

**Notes:** The docker-compose version of this app uses host networking.  The configuration of alternative networking is also beyond the scope of this repo, although host networking has been chosen to ensure connectivity via VPN is available in our development environment.

## License

Please see the accompanying `LICENSE` file that is distributed with this repository.

## Disclaimer

Please see the `.disclaimer` file that is distributed with this repository.

