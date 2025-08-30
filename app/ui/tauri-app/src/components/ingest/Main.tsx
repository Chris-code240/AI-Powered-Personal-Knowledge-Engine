import React, { useState, useRef, useEffect, DragEvent, ClipboardEvent } from "react"

const IngestMain: React.FC = () => {
  const [dragActive, setDragActive] = useState(false)
  const [droppedItem, setDroppedItem] = useState<string | null>(null)
  const dropRef = useRef<HTMLDivElement | null>(null)

  // Handle Drag & Drop
  const handleDragOver = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    setDragActive(true)
  }

  const handleDragLeave = () => setDragActive(false)

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    setDragActive(false)

    const textData = e.dataTransfer.getData("text")
    if (textData) {
      setDroppedItem(textData)
      return
    }

    const file = e.dataTransfer.files[0]
    if (file) {
      setDroppedItem(file.name)
    }
  }

  // Handle Paste
  const handlePaste = (e: ClipboardEvent<HTMLDivElement>) => {
    const pastedText = e.clipboardData.getData("text")
    if (pastedText) {
      setDroppedItem(pastedText)
      return
    }

    const file = e.clipboardData.files[0]
    if (file) {
      setDroppedItem(file.name)
    }
  }

  // Focus area for paste when clicked
  useEffect(() => {
    if (dropRef.current) {
      dropRef.current.focus()
    }
  }, [])

  return (
    <div className="w-full h-full flex items-center justify-center" 
        onPaste={handlePaste}>
      <div
        ref={dropRef}
        tabIndex={0}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={`w-3/4 h-64 border-2 border-dashed rounded-2xl flex flex-col items-center justify-center transition-colors cursor-pointer outline-none ${
          dragActive
            ? "border-blue-500 bg-blue-100/30"
            : "border-gray-400 bg-white/60"
        }`}
        
      >
        <p className="text-gray-700 text-lg">
          {droppedItem
            ? `Received: ${droppedItem}`
            : "Drag, Drop, or Paste a link or media file"}
        </p>
        <span className="text-gray-500 text-sm mt-2">
          Supports: URLs, images, videos, audio
        </span>
      </div>
    </div>
  )
}

export default IngestMain
