"use client";

import { createContext, useContext, useEffect, useState, ReactNode } from "react";
import { useRouter } from "next/navigation";
import { api, getErrorMessage, STORAGE_KEY } from "@/lib/api";
import { User } from "@/types";
import toast from "react-hot-toast";

interface AuthCtx {
  user: User | null;
  loading: boolean;
  login: (identifier: string, password: string) => Promise<void>;
  register: (data: RegisterData) => Promise<void>;
  logout: () => void;
}

interface RegisterData {
  email: string;
  username: string;
  password: string;
  full_name?: string;
}

const AuthContext = createContext<AuthCtx | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const token = typeof window !== "undefined" ? localStorage.getItem(STORAGE_KEY) : null;
    if (!token) {
      setLoading(false);
      return;
    }
    api
      .get("/auth/me")
      .then((res) => setUser(res.data.user))
      .catch(() => {
        localStorage.removeItem(STORAGE_KEY);
        setUser(null);
      })
      .finally(() => setLoading(false));
  }, []);

  const login = async (identifier: string, password: string) => {
    try {
      const res = await api.post("/auth/login", {
        email: identifier,
        password,
      });
      localStorage.setItem(STORAGE_KEY, res.data.token);
      setUser(res.data.user);
      toast.success(`Welcome back, ${res.data.user.username}!`);
      router.push("/dashboard");
    } catch (err) {
      toast.error(getErrorMessage(err));
      throw err;
    }
  };

  const register = async (data: RegisterData) => {
    try {
      const res = await api.post("/auth/register", data);
      localStorage.setItem(STORAGE_KEY, res.data.token);
      setUser(res.data.user);
      toast.success("Account created successfully!");
      router.push("/dashboard");
    } catch (err) {
      toast.error(getErrorMessage(err));
      throw err;
    }
  };

  const logout = () => {
    localStorage.removeItem(STORAGE_KEY);
    setUser(null);
    toast.success("Logged out successfully");
    router.push("/");
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used inside AuthProvider");
  return ctx;
}
