import React, { useState } from 'react';
import { Task } from '@/types/tasks';

interface TaskCardProps {
  task: Task;
  onUpdate: (updatedTask: Partial<Task>) => void;
  onDelete: () => void;
}

export default function TaskCard({ task, onUpdate, onDelete }: TaskCardProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description || '');

  const handleSave = () => {
    onUpdate({ title, description });
    setIsEditing(false);
  };

  const handleCancel = () => {
    setTitle(task.title);
    setDescription(task.description || '');
    setIsEditing(false);
  };

  const handleToggleComplete = () => {
    onUpdate({ completed: !task.completed });
  };

  return (
    <div className={`border rounded-lg p-4 mb-3 shadow-sm ${task.completed ? 'bg-green-50' : 'bg-white'}`}>
      {isEditing ? (
        <div className="space-y-3">
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="shadow-sm px-3 py-2 border border-gray-300 focus:border-indigo-500 rounded-md focus:outline-none focus:ring-indigo-500 w-full text-gray-700"
            autoFocus
          />
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="shadow-sm px-3 py-2 border border-gray-300 focus:border-indigo-500 rounded-md focus:outline-none focus:ring-indigo-500 w-full text-gray-700"
            rows={2}
          />
          <div className="flex space-x-2">
            <button
              onClick={handleSave}
              className="inline-flex items-center bg-indigo-600 hover:bg-indigo-700 shadow-sm px-3 py-1 border border-transparent rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 font-medium text-white text-sm"
            >
              Save
            </button>
            <button
              onClick={handleCancel}
              className="inline-flex items-center bg-white hover:bg-gray-50 shadow-sm px-3 py-1 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 font-medium text-gray-700 text-sm"
            >
              Cancel
            </button>
          </div>
        </div>
      ) : (
        <>
          <div className="flex items-start">
            <input
              type="checkbox"
              checked={task.completed}
              onChange={handleToggleComplete}
              className="mt-1 border-gray-300 rounded w-4 h-4 text-indigo-600"
            />
            <div className="flex-1 ml-3">
              <h3 className={`text-lg font-medium ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                {task.title}
              </h3>
              {task.description && (
                <p className={`mt-1 text-sm ${task.completed ? 'text-gray-500' : 'text-gray-600'}`}>
                  {task.description}
                </p>
              )}
              <p className="mt-2 text-gray-500 text-xs">
                Created: {new Date(task.createdAt).toLocaleDateString()}
              </p>
            </div>
          </div>
          <div className="flex justify-end space-x-2 mt-3">
            <button
              onClick={() => setIsEditing(true)}
              className="inline-flex items-center bg-white hover:bg-gray-50 shadow-sm px-3 py-1 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 font-medium text-gray-700 text-sm"
            >
              Edit
            </button>
            <button
              onClick={onDelete}
              className="inline-flex items-center bg-red-600 hover:bg-red-700 shadow-sm px-3 py-1 border border-transparent rounded-md focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 font-medium text-white text-sm"
            >
              Delete
            </button>
          </div>
        </>
      )}
    </div>
  );
}