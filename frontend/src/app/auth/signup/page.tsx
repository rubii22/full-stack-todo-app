'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useAuth } from '@/hooks/useAuth';

export default function SignupPage() {
  const router = useRouter();
  const { register, error, clearError } = useAuth();
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    clearError();

    try {
      await register(name, email, password);
      router.push('/dashboard');
      router.refresh(); // Refresh to update the UI
    } catch (err) {
      // Error is handled by the auth context
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <label htmlFor="name" className="block font-medium text-gray-700 text-sm">
          Full Name
        </label>
        <div className="mt-1">
          <input
            id="name"
            name="name"
            type="text"
            autoComplete="name"
            required
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="block shadow-sm px-3 py-2 border border-gray-300 focus:border-indigo-500 rounded-md focus:outline-none focus:ring-indigo-500 w-full text-gray-700 sm:text-sm appearance-none placeholder-gray-400"
          />
        </div>
      </div>

      <div>
        <label htmlFor="email" className="block font-medium text-gray-700 text-sm">
          Email address
        </label>
        <div className="mt-1">
          <input
            id="email"
            name="email"
            type="email"
            autoComplete="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="block shadow-sm px-3 py-2 border border-gray-300 focus:border-indigo-500 rounded-md focus:outline-none focus:ring-indigo-500 w-full text-gray-700 sm:text-sm appearance-none placeholder-gray-400"
          />
        </div>
      </div>

      <div>
        <label htmlFor="password" className="block font-medium text-gray-700 text-sm">
          Password
        </label>
        <div className="mt-1">
          <input
            id="password"
            name="password"
            type="password"
            autoComplete="new-password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="block shadow-sm px-3 py-2 border border-gray-300 focus:border-indigo-500 rounded-md focus:outline-none focus:ring-indigo-500 w-full text-gray-700 sm:text-sm appearance-none placeholder-gray-400"
          />
        </div>
      </div>

      {error && (
        <div className="bg-red-50 p-4 rounded-md">
          <div className="text-red-700 text-sm">{error}</div>
        </div>
      )}

      <div>
        <button
          type="submit"
          disabled={loading}
          className="flex justify-center bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 shadow-sm px-4 py-2 border border-transparent rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 w-full font-medium text-white text-sm"
        >
          {loading ? 'Creating account...' : 'Sign up'}
        </button>
      </div>

      <div className="text-gray-600 text-sm text-center">
        Already have an account?{' '}
        <Link href="/auth/login" className="font-medium text-indigo-600 hover:text-indigo-500">
          Sign in
        </Link>
      </div>
    </form>
  );
}