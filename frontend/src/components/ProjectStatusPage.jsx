import React, { useState } from "react";
import axios from "axios";

export default function ProjectStatusPage() {
  const [projectId, setProjectId] = useState("");
  const [status, setStatus] = useState(null);
  const [error, setError] = useState("");

  const fetchProjectStatus = async () => {
    setError("");
    setStatus(null);
    if (!projectId.trim()) {
      setError("Project ID is required");
      return;
    }
    try {
      const response = await axios.get(
        `http://localhost:8000/shecodes/projectstatus?projectid=${projectId}`
      );
      setStatus(response.data);
    } catch (err) {
      setError(
        err.response?.data?.message || "Something went wrong while fetching data"
      );
    }
  };

  return (
    <div className="p-8">
      <h2 className="text-2xl font-bold text-center mb-6">Project Hardware Status</h2>

      <div className="max-w-md mx-auto">
        <label className="block text-sm font-semibold mb-2">Project ID:</label>
        <input
          type="text"
          value={projectId}
          onChange={(e) => setProjectId(e.target.value)}
          className="w-full border border-gray-300 rounded px-3 py-2 mb-4"
        />
        <button
          onClick={fetchProjectStatus}
          className="w-full bg-purple-600 text-white font-semibold py-2 px-4 rounded hover:bg-purple-700"
        >
          Fetch Status
        </button>

        {error && <p className="text-red-600 mt-4 text-center">{error}</p>}

        {status && (
          <div className="mt-6 border-t pt-4">
            <div className="mb-4">
              <label className="block font-semibold mb-1">Checked Out Quantity:</label>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm">Hardware SET 1</label>
                  <input
                    readOnly
                    value={status.checkedOut[0]}
                    className="w-full border rounded px-3 py-1"
                  />
                </div>
                <div>
                  <label className="block text-sm">Hardware SET 2</label>
                  <input
                    readOnly
                    value={status.checkedOut[1]}
                    className="w-full border rounded px-3 py-1"
                  />
                </div>
              </div>
            </div>

            <div>
              <label className="block font-semibold mb-2">Hardware Check Out Feature:</label>
              <div className="grid grid-cols-4 gap-4 text-sm font-medium mb-1">
                <span>Hardware</span>
                <span>Capacity</span>
                <span>Available</span>
                <span>Request</span>
              </div>
              {status.inventory.map((hw, index) => (
                <div key={hw.hardwareid} className="grid grid-cols-4 gap-4 mb-2">
                  <span className="pt-1 font-semibold">{hw.hardwareid.toUpperCase()}</span>
                  <input readOnly value={hw.capacity} className="border rounded px-2 py-1" />
                  <input readOnly value={hw.available} className="border rounded px-2 py-1" />
                  <input placeholder="Enter quantity" className="border rounded px-2 py-1" />
                </div>
              ))}

              <div className="flex justify-end space-x-4 mt-4">
                <button className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
                  Check In
                </button>
                <button className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
                  Check Out
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
