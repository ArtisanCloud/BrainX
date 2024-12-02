import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkBreaks from "remark-breaks";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import {dracula} from "react-syntax-highlighter/dist/esm/styles/prism";


const markdownTextTest = `
# React Markdown Example

- Some text
- Some other text

## Subtitle

### Additional info

This is a [link](https://github.com/remarkjs/react-markdown)

# React Markdown Example

~~~js
const aJsVariable = "Test";

console.log(aJsVariable);
~~~

`;

function MarkdownPreview({ markdownText }: { markdownText: string }) {
  return (
    <section>
      <ReactMarkdown
        remarkPlugins={[remarkGfm, remarkBreaks]}
        components={{
          code({ className, children, ...rest }) {
            const match = /language-(\w+)/.exec(className || "");
            const content = String(children).replace(/\n$/, '');

            return match ? (
              <SyntaxHighlighter
                PreTag="div"
                language={match[1]}
                style={dracula}
              >
                {content}
              </SyntaxHighlighter>
            ) : (
              <code {...rest} className={className}>
                {children}
              </code>
            );
          },
        }}
      >
        {/*{markdownTextTest}*/}
        {markdownText}
      </ReactMarkdown>
    </section>
  );
}

export default MarkdownPreview;
