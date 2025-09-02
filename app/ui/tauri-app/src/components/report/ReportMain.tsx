import React, { useEffect, useState } from "react"
import {
  LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, Tooltip, XAxis, YAxis, CartesianGrid, ResponsiveContainer, Legend, Treemap
} from "recharts"

type IngestionOverTime = { date: string; count: number }
type TopSource = { source: string; count: number }
type ChunkSize = { label: string; avgSize: number }
type EmbeddingCoverage = { status: string; percentage: number }
type TagDistribution = { tag: string; count: number }
type ModelUsage = { model: string; count: number }
type ErrorsOverTime = { date: string; errors: number }

const COLORS = ["#0088FE", "#00C49F", "#FFBB28", "#FF8042", "#A020F0"]

type ReportResponse<T = any> = {
  success: boolean;
  data: T;
};

async function fetchReport<T = any>(): Promise<ReportResponse<T> | null> {
  try {
    const res = await fetch("http://localhost:5000/report");
    if (!res.ok) throw new Error(`HTTP error! Status: ${res.status}`);
    return await res.json() as ReportResponse<T>;
  } catch (err) {
    console.error("Failed to fetch report:", err);
    return null;
  }
}


const ReportMain: React.FC = () => {
  const [ingestionOverTime, setIngestionOverTime] = useState<IngestionOverTime[]>([])
  const [topSources, setTopSources] = useState<TopSource[]>([])
  const [chunkSizes, setChunkSizes] = useState<ChunkSize[]>([])
  const [embeddingCoverage, setEmbeddingCoverage] = useState<EmbeddingCoverage[]>([])
  const [tagDistribution, setTagDistribution] = useState<TagDistribution[]>([])
  const [untaggedDocs, setUntaggedDocs] = useState<number>(0)
  const [modelUsage, setModelUsage] = useState<ModelUsage[]>([])
  const [errorsOverTime, setErrorsOverTime] = useState<ErrorsOverTime[]>([])

  useEffect(() => {
    const fetchData = async () => {
      const report = await fetchReport()
      if (report?.success) {
        const data = report.data
        setIngestionOverTime(data.ingestionOverTime || [])
        setTopSources(data.topSources || [])
        setChunkSizes(data.chunkSizes || [])
        setEmbeddingCoverage(data.embeddingCoverage || [])
        setTagDistribution(data.tagDistribution || [])
        setUntaggedDocs(data.untaggedDocs || 0)
        setModelUsage(data.modelUsage || [{ model: 'Spacy', count: 1 }, { model: 'Phi-3-mini', count: 3 }])
        setErrorsOverTime(data.errorsOverTime || [])
      }
    }
    fetchData()
  }, [])


  return (
    <div className="grid grid-cols-2 gap-6 p-4 overflow-scroll w-full h-full">
      {/* Ingestion Over Time */}
      <div className="border hover:border-[#fafafa] border-[#fafafa60] rounded-xl shadow p-4">
        <h2 className="text-lg font-bold mb-2 text-white font-thin">Number of Documents Over Time</h2>
        <ResponsiveContainer width="100%" height={250}>
          <LineChart data={ingestionOverTime}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="count" stroke="#8884d8" strokeWidth={2} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Top Sources */}
      <div className="border rounded-xl shadow p-4 hover:border-[#fafafa] border-[#fafafa60]">
        <h2 className="text-lg font-bold mb-2 text-white font-thin">Top Sources</h2>
        <ResponsiveContainer width="100%" height={250}>
          <BarChart data={topSources} layout="vertical">
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis type="number" />
            <YAxis dataKey="source" type="category" />
            <Tooltip />
            <Bar dataKey="count" fill="#82ca9d" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Average Chunk Size */}
      <div className="border rounded-xl shadow p-4 hover:border-[#fafafa] border-[#fafafa60]">
        <h2 className="text-lg font-bold mb-2 text-white font-thin">Average Chunk Size</h2>
        <ResponsiveContainer width="100%" height={250}>
          <BarChart data={chunkSizes}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="label" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="avgSize" fill="#8884d8" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Embedding Coverage */}
      <div className="border rounded-xl shadow p-4 hover:border-[#fafafa] border-[#fafafa60]">
        <h2 className="text-lg font-bold mb-2 text-white font-thin">Embedding Coverage</h2>
        <ResponsiveContainer width="100%" height={250}>
          <PieChart>
            <Pie
              data={embeddingCoverage}
              dataKey="percentage"
              nameKey="status"
              outerRadius={80}
              fill="#8884d8"
              label
            >
              {embeddingCoverage.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>

      {/* Tags Distribution */}
      <div className="border rounded-xl shadow p-4 hover:border-[#fafafa] border-[#fafafa60]">
        <h2 className="text-lg font-bold mb-2 text-white font-thin">Tags Distribution</h2>
        <ResponsiveContainer width="100%" height={250}>
          <Treemap
            data={tagDistribution.map(t => ({ name: t.tag, size: t.count }))}
            dataKey="size"
            stroke="#fff"
            fill="#82ca9d"
          />
        </ResponsiveContainer>
      </div>

      {/* Documents Without Tags */}
      <div className="border rounded-xl shadow p-4 flex flex-col items-center justify-center hover:border-[#fafafa] border-[#fafafa60]">
        <h2 className="text-lg font-bold mb-2 text-white font-thin">Documents Without Tags</h2>
        <p className="text-3xl font-bold text-red-600">{untaggedDocs}</p>
      </div>

      {/* Embedding Model Usage */}
      <div className="border rounded-xl shadow p-4 hover:border-[#fafafa] border-[#fafafa60]">
        <h2 className="text-lg font-bold mb-2 text-white font-thin">Embedding Model Usage</h2>
        <ResponsiveContainer width="100%" height={250}>
          <PieChart>
            <Pie
              data={modelUsage}
              dataKey="count"
              nameKey="model"
              outerRadius={80}
              label
            >
              {modelUsage.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>

      {/* Error Logs Over Time */}
      <div className="border rounded-xl shadow p-4 hover:border-[#fafafa] border-[#fafafa60]">
        <h2 className="text-lg font-bold mb-2 text-white font-thin">Error Logs Over Time</h2>
        <ResponsiveContainer width="100%" height={250}>
          <LineChart data={errorsOverTime}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="errors" stroke="#ff4d4f" strokeWidth={2} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}

export default ReportMain
