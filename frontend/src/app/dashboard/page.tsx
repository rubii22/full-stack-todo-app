'use client';

import { useState, useEffect } from 'react';
import { useTasks } from '@/hooks/useTasks';
import TaskList from '@/components/tasks/TaskList';
import TaskForm from '@/components/tasks/TaskForm';
import TaskFilter from '@/components/tasks/TaskFilter';

export default function DashboardPage() {
  const {
    tasks,
    loading,
    error,
    createTask,
    updateTask,
    deleteTask
  } = useTasks();

  const [filter, setFilter] = useState<'all' | 'active' | 'completed'>('all');

  const filteredTasks = tasks.filter(task => {
    if (filter === 'active') return !task.completed;
    if (filter === 'completed') return task.completed;
    return true;
  });

  return (
    <div className="py-6">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
        <h1 className="text-2xl font-semibold text-gray-900">My Tasks</h1>
      </div>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
        <div className="py-4">
          <TaskForm onCreateTask={createTask} />

          <div className="mt-8">
            <TaskFilter
              currentFilter={filter}
              onFilterChange={setFilter}
              taskCount={filteredTasks.length}
            />

            {error && (
              <div className="rounded-md bg-red-50 p-4 mt-4">
                <div className="text-sm text-red-700">{error}</div>
              </div>
            )}

            {loading ? (
              <div className="flex justify-center items-center h-32">
                <p>Loading tasks...</p>
              </div>
            ) : (
              <TaskList
                tasks={filteredTasks}
                onUpdateTask={updateTask}
                onDeleteTask={deleteTask}
              />
            )}
          </div>
        </div>
      </div>
    </div>
  );
}