# Simian-codegen-context

Teach AI codegen about Simian.

Using AI code generation tools can be a massive boost to your productivity.
When the number of hallucinations is not too high, that is.

To reduce the number of hallucinations it is advised to provide context to your prompts.
Your AI model will use the context to give better suggestions.

To teach your AI model about how to build Simian web apps, we have prepared a Python context file that contains all the major features.
Provide it a context to your prompts and the suggestions you get should markedly improve.

## Copilot + VS Code

In your settings add the following field to add the `SimianContext.py` file as standard context to your prompts.

```json
    "github.copilot.chat.codeGeneration.instructions": [
            {"file": "SimianContext.py"}
    ]
```
