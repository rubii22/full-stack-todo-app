import React, { useState } from 'react';
import { CreateTaskRequest } from '@/types/tasks';

interface TaskFormProps {
  onCreateTask: (taskData: CreateTaskRequest) => void;
}

export default function TaskForm({ onCreateTask }: TaskFormProps) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!title.trim()) {
      setError('Title is required');
      return;
    }

    onCreateTask({ title: title.trim(), description: description.trim() });

    // Reset form
    setTitle('');
    setDescription('');
    setError('');
  };

  return (
    <div className="bg-white shadow p-6 sm:rounded-md overflow-hidden">
      <h2 className="mb-4 font-medium text-gray-900 text-lg">Create New Task</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        {error && (
          <div className="bg-red-50 p-4 rounded-md">
            <div className="text-red-700 text-sm">{error}</div>
          </div>
        )}

        <div>
          <label htmlFor="title" className="block font-medium text-gray-700 text-sm">
            Title *
          </label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => {
              setTitle(e.target.value);
              if (error) setError(''); // Clear error when user starts typing
            }}
            className="block shadow-sm mt-1 px-3 py-2 border border-gray-300 focus:border-indigo-500 rounded-md focus:outline-none focus:ring-indigo-500 w-full text-gray-700 sm:text-sm"
            placeholder="What needs to be done?"
          />
        </div>

        <div>
          <label htmlFor="description" className="block font-medium text-gray-700 text-sm">
            Description
          </label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={3}
            className="block shadow-sm mt-1 px-3 py-2 border border-gray-300 focus:border-indigo-500 rounded-md focus:outline-none focus:ring-indigo-500 w-full text-gray-700 sm:text-sm"
            placeholder="Add details about this task..."
          />
        </div>

        <div>
          <button
            type="submit"
            className="inline-flex items-center bg-indigo-600 hover:bg-indigo-700 shadow-sm px-4 py-2 border border-transparent rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 font-medium text-white text-sm"
          >
            Add Task
          </button>
        </div>
      </form>
    </div>
  );
}