# User interface for monitoring and performance analysis of resources in Kubernetes environments
This user interface represents the state of a Kubernetes cluster as realistically as possible. Benchmarks can be executed self-controlled on specific cluster nodes and
thus their performance with respect to their available resources can be viewed and compared by
scoring.

> ⚠️ In `../backend` there is a third-party developed backend with a deployment for a Kubernetes cluster.
> **Use it for the demonstration of the frontend**
## Setup frontend
### Dependencies
* Node v16 as runtime
* npm v8.5

First, all packages must be loaded with the following command

```
$ npm install
```

After that, the application can already be started.
The following command compiles the application and enables hot-reloads for development.
```
$ npm run serve
```

After starting, the application runs by default on port 8080.
To specify a diffrent port you can use the following.

```
$ npm run serve -- --port <replace_with_port>
```

In `./src/services/benchmark-service.ts` you can specify a backend host, which will be connected with the frontend.
By default it is `http://localhost:8000`, where the backend developed by third party runs after its startup.
### Build
To build a minimized runnable application for production use the following command
```
$ npm run build
```
It generates a ``dist`` directory with a production build, which can be used for deployment.
For this the ``/dist/index.html`` must be served.

