import React from 'react';

interface TaskFilterProps {
  currentFilter: 'all' | 'active' | 'completed';
  onFilterChange: (filter: 'all' | 'active' | 'completed') => void;
  taskCount: number;
}

export default function TaskFilter({ currentFilter, onFilterChange, taskCount }: TaskFilterProps) {
  return (
    <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between border-b border-gray-200 pb-4">
      <div className="text-sm text-gray-700 mb-2 sm:mb-0">
        Showing <span className="font-medium">{taskCount}</span> {taskCount === 1 ? 'task' : 'tasks'}
      </div>
      <div className="flex space-x-1">
        <button
          onClick={() => onFilterChange('all')}
          className={`px-3 py-1 text-sm rounded-md ${
            currentFilter === 'all'
              ? 'bg-indigo-100 text-indigo-800'
              : 'text-gray-700 hover:bg-gray-100'
          }`}
        >
          All
        </button>
        <button
          onClick={() => onFilterChange('active')}
          className={`px-3 py-1 text-sm rounded-md ${
            currentFilter === 'active'
              ? 'bg-indigo-100 text-indigo-800'
              : 'text-gray-700 hover:bg-gray-100'
          }`}
        >
          Active
        </button>
        <button
          onClick={() => onFilterChange('completed')}
          className={`px-3 py-1 text-sm rounded-md ${
            currentFilter === 'completed'
              ? 'bg-indigo-100 text-indigo-800'
              : 'text-gray-700 hover:bg-gray-100'
          }`}
        >
          Completed
        </button>
      </div>
    </div>
  );
}