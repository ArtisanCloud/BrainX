---
title: 异步执行
date: 2024-06-04
---

# 异步

在本示例中，我们将构建一个具有原生[异步](https://docs.python.org/3/library/asyncio.html)实现的[ReAct](./react.md)代理。

当聊天模型具有异步客户端时，如果您在流程图中运行并发分支或在较大的Web服务器进程中运行图，这可以为我们带来一些不错的性能改进。

一般来说，您不需要更改图中的任何内容来添加异步支持。这是[Runnables](https://python.langchain.com/v0.1/docs/expression_language/interface/)的一个优点。



**注意事项**：
> 在这个操作指南中，我们将从头开始创建我们的代理，以确保透明性（但会显得冗长）。您也可以使用 create_react_agent(model, tools=tool)（API 文档）构造函数来实现类似的功能。如果您习惯于使用 LangChain 的 AgentExecutor 类，这可能更适合您。

请参考原文的代码演示过程：https://langchain-ai.github.io/langgraph/how-tos/async/

[//]: # ()
[//]: # (## 设置)

[//]: # ()
[//]: # (安装依赖包)

[//]: # ()
[//]: # (```shell)

[//]: # (!pip install --quiet -U langgraph langchain_anthropic)

[//]: # ()
[//]: # (```)

[//]: # ()
[//]: # (接下来，我们需要设置 OpenAI（我们将使用的 LLM）和 Tavily（我们将使用的搜索工具）的 API 密钥。)

[//]: # ()
[//]: # (```python)

[//]: # (import os)

[//]: # (import getpass)

[//]: # ()
[//]: # (def _set_env&#40;var: str&#41;:)

[//]: # (    if not os.environ.get&#40;var&#41;:)

[//]: # (        os.environ[var] = getpass.getpass&#40;f"{var}: "&#41;)

[//]: # ()
[//]: # (_set_env&#40;"ANTHROPIC_API_KEY"&#41;)

[//]: # ()
[//]: # (```)

[//]: # ()
[//]: # ()
[//]: # (## 设置状态)

[//]: # ()
[//]: # (在 langgraph 中，主要的图类型是 StateGraph。这种图通过一个 State 对象进行参数化，并将其传递给每个节点。每个节点然后返回用于更新该状态的操作。这些操作可以是设置（SET）状态的特定属性（例如覆盖现有值），也可以是添加（ADD）到现有属性。是否进行设置或添加，通过你用来构建图的 State 对象的注释来表示。)

[//]: # ()
[//]: # (在这个示例中，我们将跟踪的状态只是一个消息列表。我们希望每个节点都向该列表中添加消息。因此，我们将使用一个带有一个键（messages）的 TypedDict，并对其进行注释，使得 messages 属性为“仅追加”。)

[//]: # ()
[//]: # (```python)

[//]: # ()
[//]: # (from typing_extensions import TypedDict)

[//]: # (from typing import Annotated)

[//]: # (from langgraph.graph.message import add_messages)

[//]: # ()
[//]: # (# Add messages essentially does this with more)

[//]: # (# robust handling)

[//]: # (# def add_messages&#40;left: list, right: list&#41;:)

[//]: # (#     return left + right)

[//]: # ()
[//]: # ()
[//]: # (class State&#40;TypedDict&#41;:)

[//]: # (    messages: Annotated[list, add_messages])

[//]: # (```)

[//]: # ()
[//]: # (## 设置工具)

[//]: # ()
[//]: # (首先，我们需要定义我们想要使用的工具。在这个简单的示例中，我们将创建一个占位符搜索引擎。事实上，创建你自己的工具非常容易——请参阅文档了解如何进行设置。)

[//]: # ()
[//]: # ()
[//]: # (```python)

[//]: # (from langchain_core.tools import tool)

[//]: # ()
[//]: # ()
[//]: # (@tool)

[//]: # (def search&#40;query: str&#41;:)

[//]: # (    """Call to surf the web.""")

[//]: # (    # This is a placeholder, but don't tell the LLM that...)

[//]: # (    return ["The answer to your question lies within."])

[//]: # ()
[//]: # ()
[//]: # (tools = [search])

[//]: # (```)

[//]: # ()
[//]: # (现在我们可以创建我们的工具节点[（ToolNode）]&#40;https://langchain-ai.github.io/langgraph/reference/prebuilt/?h=tool+node#create_react_agent&#41;。这个对象实际上运行了 LLM 要求使用的工具（也称为函数）。)

[//]: # ()
[//]: # ()
[//]: # (```python)

[//]: # (from langgraph.prebuilt import ToolNode)

[//]: # ()
[//]: # (tool_node = ToolNode&#40;tools&#41;)

[//]: # (```)

[//]: # ()
[//]: # (## 设置模型)

[//]: # ()
[//]: # (现在我们需要加载聊天模型来支持我们的代理。对于下面的设计，它必须满足两个条件：)

[//]: # ()
[//]: # (* 它应该能够处理消息（因为我们的状态包含一系列聊天消息）)

[//]: # (* 它应该能够处理工具调用。)

[//]: # ()
[//]: # (> 注意：这些模型要求并不是使用 LangGraph 的通用要求 - 它们只是这个示例的要求。)

[//]: # ()
[//]: # (```python)

[//]: # (from langchain_openai import ChatOpenAI)

[//]: # ()
[//]: # (temperature = 0.5)

[//]: # (streaming = False)

[//]: # ()
[//]: # (# We will set streaming=True so that we can stream tokens)

[//]: # (# See the streaming section for more information on this.)

[//]: # (llm_name = 'gpt-3.5-turbo')

[//]: # (OPENAI_API_BASE="https://api.chatanywhere.tech")

[//]: # (OPENAI_API_KEY="YOU_OPENAPI_KEY")

[//]: # ()
[//]: # (model = ChatOpenAI&#40;)

[//]: # (        model=llm_name,)

[//]: # (        temperature=temperature,)

[//]: # (        streaming=streaming,)

[//]: # (        base_url=OPENAI_API_BASE,)

[//]: # (        api_key=OPENAI_API_KEY,)

[//]: # (    &#41;)

[//]: # (```)

[//]: # ()
[//]: # (在完成这些操作后，我们应确保模型知道它可以调用这些工具。)

[//]: # ()
[//]: # (我们可以通过将 LangChain 工具转换为适用于 OpenAI 函数调用的格式，然后将它们绑定到模型类来实现这一点)

[//]: # ()
[//]: # (```python)

[//]: # (model = model.bind_tools&#40;tools&#41;)

[//]: # ()
[//]: # (```)

[//]: # ()
[//]: # (## 定义节点)

[//]: # ()
[//]: # (我们现在需要在我们的图中定义几个不同的节点。在 langgraph 中，一个节点可以是一个函数或一个可运行的对象。我们需要的两个主要节点是：)

[//]: # ()
[//]: # (1. 代理：负责决定是否采取行动。)

[//]: # (2. 用于调用工具的函数：如果代理决定采取行动，这个节点将执行该行动。)

[//]: # ()
[//]: # ()
[//]: # (我们还需要定义一些边缘（edges）。其中一些边缘可能是有条件的。这些边缘之所以是有条件的，是因为根据一个节点的输出，可能会采取几条路径中的一条。选择哪条路径要等到节点运行时（由 LLM 决定）才能知道。)

[//]: # ()
[//]: # (有条件的边缘：在调用代理后，我们应该采取以下步骤：)

[//]: # (a. 如果代理决定采取行动，那么就调用工具执行的函数。)

[//]: # (b. 如果代理表示已完成，则应结束执行。)

[//]: # ()
[//]: # (普通边缘：在调用工具后，应该总是返回到代理来决定下一步的动作。)

[//]: # ()
[//]: # (让我们定义这些节点，以及一个决定如何选择有条件边缘的函数。)

[//]: # ()
[//]: # (## 修改)

[//]: # ()
[//]: # (我们将每个节点定义为异步函数。)

[//]: # ()
[//]: # (```python)

[//]: # (from typing import Literal)

[//]: # ()
[//]: # ()
[//]: # (# Define the function that determines whether to continue or not)

[//]: # (def should_continue&#40;state: State&#41; -> Literal["end", "continue"]:)

[//]: # (    messages = state["messages"])

[//]: # (    last_message = messages[-1])

[//]: # (    # If there is no tool call, then we finish)

[//]: # (    if not last_message.tool_calls:)

[//]: # (        return "end")

[//]: # (    # Otherwise if there is, we continue)

[//]: # (    else:)

[//]: # (        return "continue")

[//]: # ()
[//]: # ()
[//]: # (# Define the function that calls the model)

[//]: # (async def call_model&#40;state: State&#41;:)

[//]: # (    messages = state["messages"])

[//]: # (    response = await model.ainvoke&#40;messages&#41;)

[//]: # (    # We return a list, because this will get added to the existing list)

[//]: # (    return {"messages": [response]})

[//]: # (```)

[//]: # ()
[//]: # ()
[//]: # (## 定义图)

[//]: # ()
[//]: # (现在我们可以将所有内容整合起来，定义图！)

[//]: # ()
[//]: # ()
[//]: # (```python)

[//]: # (from langgraph.graph import StateGraph, END)

[//]: # ()
[//]: # (# Define a new graph)

[//]: # (workflow = StateGraph&#40;State&#41;)

[//]: # ()
[//]: # (# Define the two nodes we will cycle between)

[//]: # (workflow.add_node&#40;"agent", call_model&#41;)

[//]: # (workflow.add_node&#40;"action", tool_node&#41;)

[//]: # ()
[//]: # (# Set the entrypoint as `agent`)

[//]: # (# This means that this node is the first one called)

[//]: # (workflow.set_entry_point&#40;"agent"&#41;)

[//]: # ()
[//]: # (# We now add a conditional edge)

[//]: # (workflow.add_conditional_edges&#40;)

[//]: # (    # First, we define the start node. We use `agent`.)

[//]: # (    # This means these are the edges taken after the `agent` node is called.)

[//]: # (    "agent",)

[//]: # (    # Next, we pass in the function that will determine which node is called next.)

[//]: # (    should_continue,)

[//]: # (    # Finally we pass in a mapping.)

[//]: # (    # The keys are strings, and the values are other nodes.)

[//]: # (    # END is a special node marking that the graph should finish.)

[//]: # (    # What will happen is we will call `should_continue`, and then the output of that)

[//]: # (    # will be matched against the keys in this mapping.)

[//]: # (    # Based on which one it matches, that node will then be called.)

[//]: # (    {)

[//]: # (        # If `tools`, then we call the tool node.)

[//]: # (        "continue": "action",)

[//]: # (        # Otherwise we finish.)

[//]: # (        "end": END,)

[//]: # (    },)

[//]: # (&#41;)

[//]: # ()
[//]: # (# We now add a normal edge from `tools` to `agent`.)

[//]: # (# This means that after `tools` is called, `agent` node is called next.)

[//]: # (workflow.add_edge&#40;"action", "agent"&#41;)

[//]: # ()
[//]: # (# Finally, we compile it!)

[//]: # (# This compiles it into a LangChain Runnable,)

[//]: # (# meaning you can use it as you would any other runnable)

[//]: # (app = workflow.compile&#40;&#41;)

[//]: # (```)

[//]: # ()
[//]: # (```python)

[//]: # (from IPython.display import Image, display)

[//]: # ()
[//]: # (display&#40;Image&#40;app.get_graph&#40;&#41;.draw_mermaid_png&#40;&#41;&#41;&#41;)

[//]: # (```)

[//]: # ()
[//]: # (## 使用它！)

[//]: # ()
[//]: # (现在我们可以使用它！它现在暴露了与所有其他 LangChain 可运行对象相同的接口。)

[//]: # ()
[//]: # ()
[//]: # (```python)

[//]: # (from langchain_core.messages import HumanMessage)

[//]: # ()
[//]: # (inputs = {"messages": [HumanMessage&#40;content="what is the weather in sf"&#41;]})

[//]: # (await app.ainvoke&#40;inputs&#41;)

[//]: # (```)

[//]: # ()
[//]: # (这可能需要一点时间——它在幕后进行了一些调用。为了在它们发生时开始看到一些中间结果，我们可以使用流式传输——请参阅下面获取更多信息。)

[//]: # ()
[//]: # ()
[//]: # (## 流式传输)

[//]: # ()
[//]: # (LangGraph 支持几种不同类型的流式传输。)

[//]: # ()
[//]: # (## 流式传输节点输出)

[//]: # ()
[//]: # (使用 LangGraph 的一个好处是可以轻松地将每个节点产生的输出作为流进行传输)

[//]: # ()
[//]: # ()
[//]: # (```python)

[//]: # (inputs = {"messages": [HumanMessage&#40;content="what is the weather in sf"&#41;]})

[//]: # (async for output in app.astream&#40;inputs, stream_mode="updates"&#41;:)

[//]: # (    # stream_mode="updates" yields dictionaries with output keyed by node name)

[//]: # (    for key, value in output.items&#40;&#41;:)

[//]: # (        print&#40;f"Output from node '{key}':"&#41;)

[//]: # (        print&#40;"---"&#41;)

[//]: # (        print&#40;value["messages"][-1].pretty_print&#40;&#41;&#41;)

[//]: # (    print&#40;"\n---\n"&#41;)

[//]: # (```)

[//]: # ()
[//]: # (## 流式传输 LLM 令牌)

[//]: # ()
[//]: # (您还可以在每个节点产生时访问 LLM 令牌。在这种情况下，只有 "agent" 节点会产生 LLM 令牌。为了使其正常工作，您必须使用支持流式传输的 LLM，并在构建 LLM 时设置它（例如 ChatOpenAI&#40;model="gpt-3.5-turbo-1106", streaming=True&#41;）。)

[//]: # ()
[//]: # (```python)

[//]: # (inputs = {"messages": [HumanMessage&#40;content="what is the weather in sf"&#41;]})

[//]: # (async for output in app.astream_log&#40;inputs, include_types=["llm"]&#41;:)

[//]: # (    # astream_log&#40;&#41; yields the requested logs &#40;here LLMs&#41; in JSONPatch format)

[//]: # (    for op in output.ops:)

[//]: # (        if op["path"] == "/streamed_output/-":)

[//]: # (            # this is the output from .stream&#40;&#41;)

[//]: # (            ...)

[//]: # (        elif op["path"].startswith&#40;"/logs/"&#41; and op["path"].endswith&#40;)

[//]: # (            "/streamed_output/-")

[//]: # (        &#41;:)

[//]: # (            # because we chose to only include LLMs, these are LLM tokens)

[//]: # (            print&#40;op["value"].content, end="|"&#41;)

[//]: # (```)

[//]: # ()
