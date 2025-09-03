import React, { useState } from "react";

type DatabaseType = {
  uri?: string;
  name?: string;
  user?: string;
  password?: string;
  host?: string;
  port?: number;
};

type CeleryType = {
  broker_url: string;
  result_backend: string;
  task_serializer: string;
  result_expires: number;
  concurrency: number;
  prefetch_multiplier: number;
};

type RedisType = {
  host: string;
  port: number;
  db: number;
  password?: string;
  ssl: boolean;
};

type SettingsType = {
  database: DatabaseType;
  celery: CeleryType;
  redis: RedisType;
};

const Settings: React.FC = () => {
  const [settings, setSettings] = useState<SettingsType>({
    database: {},
    celery: {
      broker_url: "redis://localhost:6379/0",
      result_backend: "redis://localhost:6379/1",
      task_serializer: "json",
      result_expires: 3600,
      concurrency: 4,
      prefetch_multiplier: 1,
    },
    redis: {
      host: "localhost",
      port: 6379,
      db: 0,
      password: "",
      ssl: false,
    },
  });

  const [obscure, setObscure] = useState(true);

  const handleChange = (
    section: keyof SettingsType,
    key: string,
    value: string | number | boolean
  ) => {
    setSettings((prev) => ({
      ...prev,
      [section]: {
        ...prev[section],
        [key]: value,
      },
    }));
  };

  const handleSave = () => {
    const db = settings.database;
    if (db.uri && db.uri.trim() !== "") {
      console.log("Safe: URI provided", settings);
    } else {
      const { name, user, password, host, port } = db;
      if (name && user && password && host && port) {
        console.log("Safe: All fields provided", settings);
      } else {
        console.log("Error: Missing required database fields", settings);
      }
    }
  };

  return (
    <div className="text-white space-y-6 overflow-scroll">
      {/* DATABASE SECTION */}
      <div className="space-y-3">
        <h2 className="text-xl font-bold">Database</h2>
        <div className="border border-[#d6d6d620] rounded-md p-3 space-y-3">
          <div>
            <span className="opacity-70">URI</span>
            <input
              onChange={(e) => handleChange("database", "uri", e.target.value)}
              value={settings.database.uri || ""}
              name="uri"
              className="focus:outline-none w-full focus:border-[#d6d6d650] p-2 rounded-md border-2 border-[#d6d6d610]"
            />
          </div>
          <div className="flex items-center space-x-1">
            <div className="w-1/3">
              <span className="opacity-70">Name</span>
              <input
                onChange={(e) =>
                  handleChange("database", "name", e.target.value)
                }
                value={settings.database.name || ""}
                className="w-full focus:outline-none p-2 rounded-md border-2 border-[#d6d6d610]"
              />
            </div>
            <div className="w-1/3">
              <span className="opacity-70">User</span>
              <input
                onChange={(e) =>
                  handleChange("database", "user", e.target.value)
                }
                value={settings.database.user || ""}
                className="w-full focus:outline-none p-2 rounded-md border-2 border-[#d6d6d610]"
              />
            </div>
            <div className="w-1/3">
              <span className="opacity-70">Password</span>
              <div className="relative">
                <input
                  type={obscure ? "password" : "text"}
                  onChange={(e) =>
                    handleChange("database", "password", e.target.value)
                  }
                  value={settings.database.password || ""}
                  className="w-full focus:outline-none p-2 rounded-md border-2 border-[#d6d6d610]"
                />
                <img
                  src={`/icons/eye-${obscure ? "closed.svg" : "opened.svg"}`}
                  className="absolute w-5 cursor-pointer right-1 top-[30%]"
                  onClick={() => setObscure(!obscure)}
                />
              </div>
            </div>
          </div>
          <div className="flex items-center space-x-1">
            <div className="w-1/3">
              <span className="opacity-70">Host</span>
              <input
                onChange={(e) =>
                  handleChange("database", "host", e.target.value)
                }
                value={settings.database.host || ""}
                className="w-full focus:outline-none p-2 rounded-md border-2 border-[#d6d6d610]"
              />
            </div>
            <div className="w-1/3">
              <span className="opacity-70">Port</span>
              <input
                type="number"
                onChange={(e) =>
                  handleChange("database", "port", Number(e.target.value))
                }
                value={settings.database.port || ""}
                className="w-full focus:outline-none p-2 rounded-md border-2 border-[#d6d6d610]"
              />
            </div>
          </div>
        </div>
      </div>

      {/* CELERY SECTION */}
      <div className="space-y-3">
        <h2 className="text-xl font-bold">Celery</h2>
        <div className="border border-[#d6d6d620] rounded-md p-3 space-y-3">
          <div>
            <span className="opacity-70">Broker URL</span>
            <input
              onChange={(e) =>
                handleChange("celery", "broker_url", e.target.value)
              }
              value={settings.celery.broker_url}
              className="w-full p-2 rounded-md border-2 border-[#d6d6d610]"
            />
          </div>
          <div>
            <span className="opacity-70">Result Backend</span>
            <input
              onChange={(e) =>
                handleChange("celery", "result_backend", e.target.value)
              }
              value={settings.celery.result_backend}
              className="w-full p-2 rounded-md border-2 border-[#d6d6d610]"
            />
          </div>
        </div>
      </div>

      {/* REDIS SECTION */}
      <div className="space-y-3">
        <h2 className="text-xl font-bold">Redis</h2>
        <div className="border border-[#d6d6d620] rounded-md p-3 space-y-3">
          <div className="flex items-center space-x-2">
            <div className="w-1/2">
              <span className="opacity-70">Host</span>
              <input
                onChange={(e) =>
                  handleChange("redis", "host", e.target.value)
                }
                value={settings.redis.host}
                className="w-full p-2 rounded-md border-2 border-[#d6d6d610]"
              />
            </div>
            <div className="w-1/2">
              <span className="opacity-70">Port</span>
              <input
                type="number"
                onChange={(e) =>
                  handleChange("redis", "port", Number(e.target.value))
                }
                value={settings.redis.port}
                className="w-full p-2 rounded-md border-2 border-[#d6d6d610]"
              />
            </div>
          </div>
        </div>
      </div>

      {/* SAVE BUTTON */}
      <button
        onClick={handleSave}
        className="cursor-pointer p-2 w-[8rem] my-3 bg-blue-700 hover:bg-blue-600 rounded-md text-white"
      >
        Save
      </button>
    </div>
  );
};

export default Settings;
