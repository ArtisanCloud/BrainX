import ReactMarkdown from "react-markdown";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { dark } from "react-syntax-highlighter/dist/esm/styles/prism";

const markdownText = `
# React Markdown Example

~~~js
const aJsVariable = "Test";

console.log(aJsVariable);
~~~
`;

function MarkdownComponent() {
  return (
    <section>
      <ReactMarkdown
        components={{
          code({ className, children, ...rest }) {
            const match = /language-(\w+)/.exec(className || "");
            return match ? (
              <SyntaxHighlighter
                PreTag="div"
                language={match[1]}
                style={dark}
                {...rest}
              >
                {children}
              </SyntaxHighlighter>
            ) : (
              <code {...rest} className={className}>
                {children}
              </code>
            );
          },
        }}
      >
        {markdownText}
      </ReactMarkdown>
    </section>
  );
}

export default MarkdownComponent;
