# kiwi

Kiwi is a prototype-implementation of the architecture proposed in the research paper "Individual recommendations based on minimal user input" by Felix Lange, Martin Essig and Henry Müssemann.
Furthermore it contains all necessary code for the ionic application that was used to collect the data contained in the dataset "upic" that was also presented in the above mentioned research paper.

## Structure of the repository

The repository contains the following folders:

### Application-specific services and folders

* **`kiwi-mobile-frontend`**
  * The `kiwi-mobile-frontend` folder contains the ionic project that can be used to build the frontend that was used to generate the upic dataset.

* **`kiwi-entry`**
  * The `kiwi-entry` folder contains the Service API. It provides an API for all possible actions for one setup of the architecture. It will forward all requests to the respective services.

* **`kiwi-user-manager`**
  * The `kiwi-user-manager` folder contains a service that manages the minimal user-data. It provides endpoints for saving and validating usernames. In the paper this service is referred to as the User Manager.

* **`kiwi-content-crawler`**
  * The `kiwi-content-crawler` folder contains a service that crawls data from imgur when requested and saves that crawled data. In the paper this service is referred to as the Crawler.

* **`kiwi-tester-service`**
  * The `kiwi-tester-service` contains an executable python file that can be used for testing the architecture using self-defined test cases.

### Architectural services

* **`kiwi-engine-selector`**
  * The `kiwi-engine-selector` contains an implementation of the proposed "Recommender Switcher" (as referred to in the paper), the main heart of the architecture. It will decide which recommendation engine to use for a given scenario.

The following folders are implementations for recommendation engines that can be used within the `kiwi-engine-selector`.

* **`kiwi-latest`**
  * The `kiwi-latest` folder contains an implementation for the latest-recommender. It provides recommendations based on the primary id of an item (new items that have a high primary id will be recommended first).

* **`kiwi-random`**
  * The `kiwi-random` folder contains an implementation of the random-recommender. It randomly recommends an item to a user.

* **`kiwi-surprise`**
  * The `kiwi-surprise` folder can be used to build a service for any algorithm that the [Surprise framework](http://surpriselib.com/) offers. The service will automatically have all necessary REST-API-endpoints implemented. This makes it easier to deploy surprise algorithms as separate recommender engines and reduces duplicated code.

* **`kiwi-content`**
  * The `kiwi-content` folder contains an implementation of a content-based recommender. It is a custom-made prototype implementation.

## Deploying for testing purposes

To test the architecture on your system you will need to have docker installed in a manner that the `docker-compose` command will work on your machine.
A good tutorial for installing docker can be found [here](https://docs.docker.com/install/) and for installing docker-compose you can take a look at [this tutorial](https://docs.docker.com/compose/install/).

We recommend starting the architecture using a docker-compose-file that is adapted to your specific needs. You don't always have to start all services, sometimes you might for example want to use a custom and performance-optimized database server and so on.
But to get you started the repository delivers a working docker-compose-file that can be used for development purposes. It is called `docker-compose-upic-dev.yml`.

To start your docker-compose using that file just navigate to the kiwi folder within your terminal and type in:

```
 > sudo docker-compose -f docker-compose-upic-dev.yml build
 > sudo docker-compose -f docker-compose-upic-dev.yml up
```

Your engine service will now provide the REST-API for all necessary architectural endpoints at `http://localhost:8000/`.
To find out how to deploy a fully functioning application containing the Crawler, Service-API and User Manager you can take a look at the `docker-compose.yml` in the main folder.

## Starting a test-case

To start a test-case you will have to first navigate to the `kiwi-tester-service` folder within your terminal.
There you can install all necessary python packages contained within the `requirements.txt`. We recommend to install all python packages within a virtual environment (e.g. [venv](https://docs.python.org/3/library/venv.html)).
The kiwi-tester-service supports python v3 as well as python v2.

```
 > pip install -r requirements.txt
```

As soon as your backend-application is running and all databases were found and connected to, you can run your test-case using the following command:

```
 > python app.py <test_case> <statistic_output_file>
```

where `test_case` defines the test-case to use (a folder name that is contained within `kiwi-tester-service/kiwi_tester/test_cases/`) and `statistic_output_file` defines an absolute path to save the statistic file to.

## Building the U:Pic Frontend (`kiwi-mobile-frontend`)

To build the U:Pic application you will need to have ionic installed on your machine.
To install ionic just follow [these](https://ionicframework.com/docs/intro/installation/) guidelines.

To start the application within your browser in debug mode just type in:

```
 > ionic serve
```

Alternatively, if you want to build or deploy the app somehow you might want to follow the [official instructions by ionic](https://ionicframework.com/docs/v1/guide/publishing.html).
All necessary files for deploying the app as a web-app can be found in the `www` folder. You can start the app by opening the index.html.
Once the www/ folder exists, using the docker-compose-deploy.yml, can also start the webapp in a docker container, using 
`docker-compose -f docker-compose-deploy.yml up --build`
