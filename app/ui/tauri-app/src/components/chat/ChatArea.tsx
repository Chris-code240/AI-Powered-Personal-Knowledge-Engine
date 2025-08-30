import React from "react"
import { useState, useEffect, useRef } from "react"
import Input from "./Input"
import ChatBubble from "./ChatBubble"

interface Bubble {
  text: string;
  type: "user-input" | "ai-response";
  sources: string[];
}

const ChatArea: React.FC = () =>{
  const [query, setQuery] = useState<string>('')
  const [bubbles, setBubbles] = useState<Bubble[]>([])

  const endRef = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [bubbles, bubbles.length]);

  return (
    <div className="w-full flex flex-col justify-between overflow-hidden">
      <ul className="h-[90vh] flex flex-col space-y-3 overflow-y-auto">
        {bubbles.map((bubble, index) => (
          <li className="w-auto" key={`${index}-${bubble.text}`}>
            <ChatBubble text={bubble.text} type={bubble.type} sources={bubble.sources} />
          </li>
        ))}
        <div ref={endRef} />
      </ul>

      <div className="w-full">
        <Input   query={query}  setQuery={setQuery}  bubbles={bubbles}  setBubbles={setBubbles}/>
      </div>
    </div>
  )
}

export default ChatArea

