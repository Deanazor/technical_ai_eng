# Engineering Knowledge AI Agent Test

## 1. Describe differences between REST API, MCP in the context of AI.

### REST API
Is more general and we need to know what endpoint should we use.
For different AI Agent usecase we may or may not create a tool for the API (depends on the design).
Is not stateful and we need to (again, depend on the design) manually create a stateful tool for the API.

### MCP
Is usually full of "toolset" that the AI can choose without the user need to do "discovery" of the endpoint-equivalent of a tool capabilities.
Is more standardized for many AI Agent to use so that we can use the same MCP tp other AI Agent.
Is stateful by design but we can always create our own state.

## 2. How REST API, MCP, can improve the AI use case.

Context Enrichment. I think in this case it's a bit more general than RAG because if we're saying RAG people expectation are in vector databases while if you're enriching model context from REST API/MCP it's still retrieval-augmented nontheless (in a more literal way).
But yeah the spirit is the same, AI Agent could be limited by it's knowledge (like depend on what kind of data are it being trained to) hence adding additonal relevant data from REST API or MCP can help the AI Agent to answer more accurately.

## 3. How do you ensure that your AI agent answers correctly?

- RAG/Context Enrichment, as previously answered in the previous question, we can (and probably should) give the model relevant information and ensure updated knowledge.
- Persona/System Prompt (Prompt Engineering), broadly speaking this will control how the AI Agent behave but more specifically the benefit is:
    - Make the AI Agent more "honest", we can make them to not make up facts or not doing something in different order
    - Planning, we can breakdown the tasks into smaller and easier steps which we can also validate, for example:
        - Use case: AC Technician
        - Problem: AC broken
        - Steps:
            - Identify which part is broken
            - Refer to manual (by RAG) to understand the broken and how to fix
            - Summarize relevant fix that needs to be done for the broken part
- Formatted Response, we can make the Agent to give response in a structured format to ensure that the relevant information we require are being returned.
- Feedback Loop, can be either from human, or a smaller agent in the pipeline to "fact check" or see if the answer is consistent with the given information.

## 4. Describe what can you do with Docker / Containerize environment in the context of AI

- Dependency Isolation, often we found an AI Project have many dependencies and more of than not, they're brawling at each other, if in one machine we need to run many different AI application, by containerizing we can isolate each other environment without them interfering at each other.
- Reproducibility, by capturing all the dependencies, environment, etc in a container, we can make sure that if we run in another machine/environment we can replicate and get a similar outcome.
- Automation (especially in shipping to production), if we can make sure both previous point, we can then automate the deployment of our application after we ensure that the result of the application is has met the expectation.
- Scaling (especially in production environemt), since likely we'll be using orchestrator like Kubernetes we can easily scale up on-demand depends on the incoming traffic if we containerize the application.

## 5. How do you finetune the LLM model from raw ?

1. We need data. This is actually the core process because if we feed low quality data into the LLM then it will result in a more sophisticated low quality LLM. So defintely what we need to do is:
    - Make sure the data source is high quality and relevant, in this step more often than not we need some sort of domain expert to sanitize the data.
    - Cleaning and filtering data from which is irrelevant, duplicates, or if there are any sensitive information that may exist in the datase (like PII, or copyright)
    - Structuring into the format where the LLM can consume, for LLM case typically in a conversational or instruction manner.
2. After we have data then we can fine tune. In this step what's crucial is selecting the base model and fine tuning strategy, such as using LoRA which is a Parameter-Efficient Fine-Tuning (PEFT), where basically we don't realy train the whole model but create additional, smaller number of parameter. And last but not least to monitor the accuray and loss for every epochs.
3. Evaluate performance. We need to define relevant quantitative metrics for the use case of the model, or we can also introduce the human-in-the-loop on evaluation where we can have experts to help evaluate the model.
