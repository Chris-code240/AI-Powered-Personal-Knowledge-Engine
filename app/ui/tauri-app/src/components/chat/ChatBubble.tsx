import React, { useState, useEffect } from "react"

type BubbleProp = {
  text: string
  type: string
  sources: string[]
}

const ChatBubble: React.FC<BubbleProp> = ({ text, type, sources = [] }) => {
  const [displayedText, setDisplayedText] = useState(
    type === "response" ? "" : text
  )

  // Simulate streaming for "response" type
  useEffect(() => {
    if (type !== "response") return

    let index = 0
    const interval = setInterval(() => {
      if (index < text.length -1) {
        setDisplayedText((prev) => prev + text[index])
        index++
      } else {
        clearInterval(interval)
      }
    }, 30) // adjust speed (ms per character)

    return () => clearInterval(interval)
  }, [text, type])

  return (
    <div
      className={`${
        text.length < 1 ? "hidden " : ""
      } ${type === "response" ? "text-gray-400 self-start" : "ml-auto"}`}
    >
      <div className="flex flex-col w-auto">
        <div
          className={`${
            type === "response"
              ? "self-start"
              : "self-end bg-[#e9eef6] p-2 rounded-md"
          }`}
        >
          {displayedText}
          {type === "response" && displayedText.length < text.length -1 && (
            <span className="animate-pulse">|</span>
          )}
        </div>
        <ul className="text-xs text-blue-500 flex items-center flex-wrap space-x-3">
          {sources?.map((value, index) => (
            <li key={`${index}-${value}`}>
              <a href={value.toLowerCase()}>{value}</a>
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}

export default ChatBubble
