import { useState, useEffect } from 'react';
import { Task, CreateTaskRequest, UpdateTaskRequest } from '@/types/tasks';
import { apiClient } from '@/lib/api';

interface UseTasksReturn {
  tasks: Task[];
  loading: boolean;
  error: string | null;
  createTask: (taskData: CreateTaskRequest) => void;
  updateTask: (id: string, updatedTask: UpdateTaskRequest) => void;
  deleteTask: (id: string) => void;
}

export function useTasks(): UseTasksReturn {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Mock data for demonstration purposes
  useEffect(() => {
    // In a real application, this would fetch from an API
    // loadTasks();

    // For demo purposes, using mock data
    setTimeout(() => {
      setTasks([
        {
          id: '1',
          title: 'Sample Task',
          description: 'This is a sample task to get you started',
          completed: false,
          userId: 'user1',
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
        },
        {
          id: '2',
          title: 'Another Task',
          description: 'This is another sample task',
          completed: true,
          userId: 'user1',
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
        }
      ]);
      setLoading(false);
    }, 500);
  }, []);

  const loadTasks = async () => {
    try {
      setLoading(true);
      setError(null);
      // const data: Task[] = await apiClient.get('/tasks');
      // setTasks(data);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  const createTask = async (taskData: CreateTaskRequest) => {
    try {
      setLoading(true);
      setError(null);
      // const newTask: Task = await apiClient.post('/tasks', taskData);
      // setTasks([newTask, ...tasks]);

      // For demo purposes, creating a mock task
      const newTask: Task = {
        id: Date.now().toString(),
        title: taskData.title,
        description: taskData.description,
        completed: false,
        userId: 'user1',
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      };
      setTasks([newTask, ...tasks]);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  const updateTask = async (id: string, updatedTask: UpdateTaskRequest) => {
    try {
      setLoading(true);
      setError(null);
      // const updated: Task = await apiClient.put(`/tasks/${id}`, updatedTask);
      // setTasks(tasks.map(task => task.id === id ? updated : task));

      // For demo purposes, updating mock task
      setTasks(tasks.map(task =>
        task.id === id
          ? { ...task, ...updatedTask, updatedAt: new Date().toISOString() }
          : task
      ));
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  const deleteTask = async (id: string) => {
    try {
      setLoading(true);
      setError(null);
      // await apiClient.delete(`/tasks/${id}`);
      // setTasks(tasks.filter(task => task.id !== id));

      // For demo purposes, deleting mock task
      setTasks(tasks.filter(task => task.id !== id));
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  return {
    tasks,
    loading,
    error,
    createTask,
    updateTask,
    deleteTask,
  };
}