# Langchain 
**Source: https://python.langchain.com/docs**  
LangChain is a framework for developing applications powered by language models. It enables applications that:  
**Are context-aware** i.e. connect a language model to sources of context (prompt instructions, few shot examples, content to ground its response in, etc.)  
**Reason** i.e. rely on a language model to reason (about how to answer based on provided context, what actions to take, etc.)

**Other Packages:**  
* **LangServe:** A library for deploying LangChain chains as a REST API.  
* **LangSmith:** A developer platform that lets you debug, test, evaluate, and monitor chains built on any LLM framework and seamlessly integrates with LangChain.

**LangChain Libraries:**  
The LangChain libraries themselves are made up of several different packages.  
    - **langchain-core:** Base abstractions and LangChain Expression Language.  
    - **langchain-community:** Third party integrations.  
    - **langchain:** Chains, agents, and retrieval strategies that make up an application's cognitive architecture.

**LangChain Components:**
1. LangChain Expression Language
2. Modules: 
    * Model I/O: Interface with language models
    * Retrieval: Interface with application-specific data
    * Agents: Let chains choose which tools to use given high-level directives

    Additional:
    * Chains: Common, building block compositions
    * Memory: Persist application state between runs of a chain
    * Callbacks: Log and stream intermediate steps of any chain

## LangChain Expression Language (LCEL)
LangChain Expression Language, or LCEL, is a declarative way to easily compose chains together. LCEL was designed from day 1 to support putting prototypes in production, with no code changes, from the simplest “prompt + LLM” chain to the most complex chains (we’ve seen folks successfully run LCEL chains with 100s of steps in production). To highlight a few of the reasons you might want to use LCEL:  
* Streaming support
* Async support
* Optimized parallel execution
* Retries and fallbacks
* Access intermediate results
* Input and output schemas
* Seamless LangSmith tracing integration
* Seamless LangServe deployment integration

## Modules:
* **Model I/O:** The core element of any language model application is the model. LangChain gives you the building blocks to interface with any language model.
    * **Prompts:** different types of prompt templates.
    * **LLMs:** functionality related to the LLM class. This is a type of model that takes a text string as input and returns a text string.
    * **ChatModels:** functionality related to the ChatModel class. This is a type of model that takes a list of messages as input and returns a message.
    * **Output Parsers:** responsible for transforming the output of LLMs and ChatModels into more structured data.
* **Retrieval:** Many LLM applications require user-specific data that is not part of the model's training set. The primary way of accomplishing this is through Retrieval Augmented Generation (RAG). In this process, external data is retrieved and then passed to the LLM when doing the generation step.
    * **Document loaders:** load documents from many different sources. LangChain provides over 100 different document loaders as well as integrations with other major providers. LangChain provides integrations to load all types of documents (HTML, PDF, code).
    * **Text Splitting:** splitting (or chunking) a large document into smaller chunks. LangChain provides several transformation algorithms for doing this.
    * **Text embedding models:** integrations with over 25 different embedding providers and methods, from open-source to proprietary API. LangChain provides a standard interface, allowing you to easily swap between models.
    * **Vector stores:** integrations with over 50 different vector stores, from open-source local ones to cloud-hosted proprietary ones. LangChain exposes a standard interface, allowing you to easily swap between vector stores.
    * **Retrievers:** LangChain supports basic methods that are easy to get started - namely simple semantic search. However, we have also added a collection of algorithms on top of this to increase performance.
    * **Indexing:** The LangChain Indexing API syncs your data from any source into a vector store.
* **Agents:** The core idea of agents is to use a language model to choose a sequence of actions to take. In chains, a sequence of actions is hardcoded (in code). In agents, a language model is used as a reasoning engine to determine which actions to take and in which order. (Action Generation)
    * **Agent Types:** There are many different types of agents to use. 
    * **Tools:** Agents are only as good as the tools they have.
* **Chains:** refer to sequences of calls - whether to an LLM, a tool, or a data preprocessing step. The primary supported way to do this is with LCEL.

    LCEL is great for constructing your own chains, but it’s also nice to have chains that you can use off-the-shelf. There are two types of off-the-shelf chains that LangChain supports:

    * Chains that are built with LCEL. In this case, LangChain offers a higher-level constructor method. However, all that is being done under the hood is constructing a chain with LCEL.

    * [Legacy] Chains constructed by subclassing from a legacy Chain class. These chains do not use LCEL under the hood but are rather standalone classes.