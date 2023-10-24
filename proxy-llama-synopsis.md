# RFC for MITM Proxy Implementation Targeting OSX

## Introduction

This RFC proposes an implementation for a Man in the Middle (MITM) proxy targeting OSX platforms. The objective is to develop a system that intercepts and relays browser communications, particularly those sent through HTTPS, and inject JavaScript that will route all page requests to a local instance of https://ollama.ai/library for summarization.

### MITM Proxy & Injection of JavaScript

A MITM proxy will be designed to monitor, intercept, and forward the transmitted data between the client and the server. Additionally, a JavaScript code will be injected into the web pages routed through the proxy. This script will send all page requests to a local instance of https://ollama.ai/library for subsequent processing.

## Implementation

The proposed implementation details include:

- Development of a proxy server to intercept and manage HTTPS traffic.
- Injection of a JavaScript code in the HTML pages routed through the proxy.
- The injected JavaScript code will reroute all page requests to https://ollama.ai/library.

## Project Repository Scaffold

A project repository will be created with the following structure:

- Client - Holds the client-side JavaScript for HTML pages.
- Server - Contains the server-side code for the proxy server.
- Persistence - Incorporates the codebase for data storage and retrieval.

## Flow Diagram

A flow diagram illustrating the flow of data can be visualized in Graphviz dot as below:

```
digraph flow {
    Client -> Proxy [label="HTTPS Request"]
    Proxy -> Server [label="Intercept/Forward"]
    Server -> Proxy [label="HTTPS Response"]
    Proxy -> Client [label="Inject JS & Respond"]
    Client -> LocalOllamaAI [label="Page Request"]
    LocalOllamaAI -> Client [label="Summarized Page"]
}
```

## Use Case: Summarizing https://wal.sh/

User visits https://wal.sh/ . The request passes through the MITM proxy, which intercepts the request, forwards it to the wal.sh server. The server responds, and the proxy intercepts the response. The proxy then injects JavaScript into the HTML response. This script then sends page requests to a local instance of https://ollama.ai/library which summarizes the page and displays the summarized version to the user.

## Project Name Suggestions

1. proxy-llama-synopsis
2. mitm-page-summarizer
3. osx-request-interceptor
4. page-summarizing-interceptor
5. osx-llama-summarizer
6. intercept-summarize-display
7. request-summary-proxy
8. https-summarizer-osx
9. intelligent-browser-interceptor
10. smart-page-digest-interceptor

---

The above proposal only mentions a high-level overview of the project. More concrete implementation details, such as technology stack, specific methods for JavaScript injection, handling of edge cases etc., will need to be further clarified.
The model `"gpt-4"C` does not exist

