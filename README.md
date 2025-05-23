This integration was supposed to grab strings for a RAG engine using ChromaDB and multiple virtual agents. The problem I ran into was that ChromaDB does not have a finished API for remote connections and our use case. This example code is not meant to bash ChromaDB because I think it has great potential as a Docker container for local instances of things like RAG, it's just not ready for what I was working on and I want to leave behind the cautionary tale and example code to help others.

  ChromaDB isn’t ready for multi-agent, high-throughput, production-grade vector memory. Our old implementation required a seprate Docker container for each agent.

Based on our architecture (many agents, each with complex group/user memory interactions and aging/archival needs), ChromaDB breaks down because:

    ❌ Single-threaded bottlenecks in local DuckDB backends

    ❌ No real auth or tenancy

    ❌ Poor support for nested metadata queries (e.g., filtering on user_ids in groups)

    ❌ No separation of RAM vs disk I/O or tuning of cache behavior

    ❌ API fragmentation: many “documented” features are marked as TODO or incomplete

It’s fine for local dev/test, or small agents running on edge devices, but not for memory orchestration across fleets of semi-persistent agents. You'll need to do some total rewriting to get this to handle your SQL database query to fit the schema. Credentials are stored in the .env file. This program ran well for testing in our environment, connecting using POST across the network. Unfortunately ChromaDB isn't good for remote.
