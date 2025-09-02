import { useState, useEffect, useRef } from "react"
import Input from "./Input"
import ChatBubble from "./ChatBubble"

type BubbleProp = {
  text: string
  type: string
  sources?: string[]
}

type ResponseData = {
  text: string
  sources?: string[]
}

type QueryResponse = {
  success: boolean
  data: ResponseData
}

type queryType = string

async function fetchQuery<T= any>(query: queryType): Promise<QueryResponse | null> {
  try {
    const res = await fetch("http://localhost:5000/query", { method: "POST", body: JSON.stringify({"query":query}), headers:{"Content-Type":"application/json"} })
    if (!res.ok) throw new Error(`HTTP error! Status: ${res.status}`)
    return (await res.json()) as QueryResponse
  } catch (err) {
    console.error("Failed to fetch report:", err)
    return null
  }
}

const ChatArea = () => {
  const [query, setQuery] = useState("")
  const [bubbles, setBubbles] = useState<BubbleProp[]>([
    { text: "", type: "user-input", sources: [] },
  ])
  const lastBubbleRef = useRef<HTMLLIElement | null>(null)

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    if (query.trim().length > 0) {
      const response = await fetchQuery(query)

      setBubbles(prev => [
        ...prev,
        { text: query, type: "user-input", sources: [] },
        {
          text: response?.data?.text || "No response",
          type: "response",
          sources: response?.data?.sources || [],
        },
      ])
      setQuery("")
    }
  }

  useEffect(() => {
    lastBubbleRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [bubbles])

  
  return (
    <div className="relative w-full h-full">
        <div className="flex flex-col w-full h-full">
          {/* Scrollable chat area */}
          <ul className="flex flex-col space-y-3 h-full overflow-y-auto pb-16 w-full mb-3">
            {bubbles.map((bubble, index) => (
              <li
                key={`${index}-${bubble.text}`}
                ref={index === bubbles.length - 1 ? lastBubbleRef : null}
              >
                <ChatBubble
                  text={bubble.text}
                  type={bubble.type}
                  sources={bubble.sources}
                />
              </li>
            ))}
          </ul>

          {/* Fixed input bar */}
          <div className="absolute bottom-0 w-full">
            <Input
              handleSubmit={handleSubmit}
              setQuery={setQuery}
              query={query}
            />
          </div>
        </div>
    </div>
  )
}

export default ChatArea
