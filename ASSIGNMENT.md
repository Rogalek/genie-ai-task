## Backend Developer Challenge

Your task is to set the foundations for the bookkeeping module. The objective is to design and implement a GraphQL
endpoint for a front-end application to display trades. Consider the requirements below.

* The front-end application will display trades in a table. Each row of the table corresponds to a single trade. The
following information should be displayed:
   * a base asset symbol and amount purchased,
   * a quote asset symbol and the price paid,
   * a fee paid and as well as its currency,
   * time of the transaction,
   * list of key value pairs (i.e., labels) assigned to the trade.
* The system will store information about thousands of trades. It is not feasible to present all of them on a single page.
Propose and implement a solution that will enable a user of the FE application to browse the result set of trades.
* The front-end should support single-select filtering on the base asset symbol.
* The front-end application should display the total number of trades that match the filtering criterion.

We did our best to make the assignment as smooth as possible. We hope you find this helpful.

* The sample project is implemented in `Python 3.10` using the FAST Api framework. We manage dependencies using `poetry`
and provide a pre-commit pipeline for static code analysis.
* Database entities are implemented in SQL Alchemy. The database model is complete, and there is no need to change it.
* The project contains a `docker-compose` that will spawn a Docker container with Postgres database.
* The database tables will be created and filled with sample data during the start of the application.
* GraphQL API is implemented using the Strawberry framework. We implemented the integration with SQL Alchemy and provide a
working example of GraphQL API for getting a list of assets registered in the system.

Once you start the application, navigate to the page `http://localhost:8080/graphql` in a web browser. A
website `Strawberry GraphiQL` should open.

To list assets, please run the GraphQL query:

    ```
    query Query {
      management {
       assets {
         name,
         symbol
       }
      }
    }
    ```

Grading Tips
* Please focus on the core objective of the assignment. We are not expecting you to implement tests, improve the docker
files, change the postgres driver to asyncpg, implement filters for fields other than the base asset symbol etc.
* Please make sure your solution makes reasonable use of database and application resources and does not put application security at risk.
