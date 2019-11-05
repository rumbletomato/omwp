# Steps of Implementation OMWP

1. Implement naive realization of main application callable class of omwp, whose will be interact with wsgi server
2. Implement naive realization of routing service, that will be have functions:
    - register callable functions as handlers;
    - match requested path to handlers and return appropriate handler;
3. Implement common handler callable classes
4. Implement handlers for case of HTTP errors
5. Implement common result classes for unify result payload, status information as result of handler works
6. Implement decorator based opportunity to mark function based user's handlers
7. Implement global request object (like in Flask) for give some information about request for user's handlers
8. Implement support of path-based parameters (like /users/1, /products/123)
9. Implement example of application which will be used OMWP opportunities