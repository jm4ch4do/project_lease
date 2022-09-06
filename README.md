# Lease API Overview
The Lease API is built for a lease company that focus on selling or leasing vehicles. The company doesn’t own any vehicle but provides a platform for customers to offer their own vehicles to sell or lease and other clients to shop around.
The API is designed with Django REST API version 4.0.6, uses token authentication and is fully tested with Pytest 7.1.2 having over 300 tests for the models and the API.

## Model General Design
The model consist of 11 tables. Each User can log in into the system and he/she will have a related Customer if the user is non administrative. Each Customer can store Credit Card and Contact information. Contacts can be also created for leads which can only be accessed by administrative users.
A Customer can also create a Vehicle for which he can latter create a Trade using one of the available Services (lease or sell, although you may create other services). The Customer owning the Vehicle can latter make a Proposal for that Trade and other Customer may accept that Proposal or create a new one.
 
If the Trade is for a Service type sell, an Invoice is created after a proposal has been accepted with the amount defined in the Service. If the Trade is created for a Service type lease (which is expected to be the most common), an Invoice is created when the first proposal is submitted. This occurs before the acceptance because the vehicle’s owner is being charge for the exposure.
Finally, the customers are supposed make a Payment with a Credit Card before the due_date indicated in the Invoice. This completes the cycle around all the tables.

## Documentation
The full description of the API's Endpoints is available in the file [Lease API docs.pdf](https://github.com/jm4ch4do/project_lease/blob/main/Lease%20API%20docs.pdf) which is in the root of the project. Examples are provided for each API feature.


